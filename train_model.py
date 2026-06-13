import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import datasets, transforms, models
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import seaborn as sns
import json
import os
from tqdm import tqdm
import time
import sys
from PIL import Image

sys.path.append('.')
from data_preparation import DatasetPreparation


# ─────────────────────────────────────────────────────────────────────────────
# 1.  Safe ImageFolder – scans and skips corrupt files before training starts
# ─────────────────────────────────────────────────────────────────────────────
class SafeImageFolder(datasets.ImageFolder):
    """
    Drop-in replacement for ImageFolder.
    Before training begins it verifies every file with PIL.Image.verify()
    and removes any that cannot be opened, so the DataLoader never crashes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._validate_samples()

    def _validate_samples(self):
        print(f"  Scanning for corrupt files in '{self.root}' … ", end="", flush=True)
        valid, bad = [], []
        for path, label in self.samples:
            try:
                with Image.open(path) as img:
                    img.verify()          # lightweight structural check
                valid.append((path, label))
            except Exception:
                bad.append(path)

        if bad:
            print(f"\n  ⚠  Removed {len(bad)} corrupt file(s):")
            for p in bad[:10]:
                print(f"       {p}")
            if len(bad) > 10:
                print(f"       … and {len(bad) - 10} more.")
        else:
            print("all OK.")

        self.samples = valid
        self.imgs    = valid   # torchvision internal alias

    def __getitem__(self, index):
        """Load with a black-image fallback so no single file can crash training."""
        path, target = self.samples[index]
        try:
            sample = self.loader(path)
        except Exception:
            sample = Image.new("RGB", (224, 224), 0)
        if self.transform:
            sample = self.transform(sample)
        if self.target_transform:
            target = self.target_transform(target)
        return sample, target


# ─────────────────────────────────────────────────────────────────────────────
# 2.  Offline-safe pretrained weight loader
# ─────────────────────────────────────────────────────────────────────────────
LOCAL_WEIGHTS = {
    'resnet18':  'resnet18_imagenet.pth',
    'resnet50':  'resnet50_imagenet.pth',
    'resnet101': 'resnet101_imagenet.pth',
}


def _load_weights_safe(model_fn, weights_enum, base_model, local_path=None):
    """Try internet → local file → random init (in that order)."""
    # Stage 1 – internet
    try:
        m = model_fn(weights=weights_enum)
        print("  ✓ Pretrained ImageNet weights loaded from internet.")
        return m
    except Exception as err:
        print(f"  ⚠  Download failed: {err}")

    # Stage 2 – local file
    if local_path and os.path.isfile(local_path):
        try:
            state = torch.load(local_path, map_location='cpu')
            if 'model_state_dict' in state:
                state = state['model_state_dict']
            base_model.load_state_dict(state, strict=False)
            print(f"  ✓ Weights loaded from {local_path}")
            return base_model
        except Exception as err:
            print(f"  ⚠  Local file failed: {err}")

    # Stage 3 – random init
    print("\n" + "!"*70)
    print("  WARNING: Training from RANDOM WEIGHTS.")
    print("  Model will still train but needs more epochs to converge.")
    print("!"*70 + "\n")
    return base_model


# ─────────────────────────────────────────────────────────────────────────────
# 3.  Main detector class
# ─────────────────────────────────────────────────────────────────────────────
class ImageForgeryDetector:
    def __init__(self, model_name='resnet18', data_dir='dataset',
                 quick_mode=True, target_minutes=60):
        self.device         = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")

        self.model_name     = model_name
        self.data_dir       = data_dir
        self.quick_mode     = quick_mode
        self.target_minutes = target_minutes

        self.verify_dataset_structure()

        # CPU vs GPU defaults
        if self.device.type == 'cpu':
            self.batch_size        = 32
            self.num_workers       = 0
            self.subset_percentage = 1.0 #if quick_mode else 1.0
            self._max_epochs       = 50  #if quick_mode else 12
        else:
            self.batch_size        = 64
            self.num_workers       = 4
            self.subset_percentage = 0.7 if quick_mode else 1.0
            self._max_epochs       = 50

        self.num_epochs    = self._max_epochs
        self.learning_rate = 0.0003

        self.train_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomRotation(10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        self.test_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.model            = None
        self.train_losses     = []
        self.val_losses       = []
        self.train_accuracies = []
        self.val_accuracies   = []

    # ── Dataset check ─────────────────────────────────────────────────────────
    def verify_dataset_structure(self):
        dirs = [os.path.join(self.data_dir, s, c)
                for s in ('train', 'val', 'test')
                for c in ('authentic', 'forged')]
        missing = []
        for d in dirs:
            if not os.path.exists(d):
                missing.append(d)
            else:
                n = len([f for f in os.listdir(d)
                         if os.path.isfile(os.path.join(d, f))])
                print(f"✓ {d}: {n} images")
        if missing:
            print("\nERROR – missing directories:")
            for d in missing:
                print(f"  ✗ {d}")
            sys.exit(1)
        print("\n✓ Dataset structure verified successfully!")

    # ── Data loading ──────────────────────────────────────────────────────────
    def load_data(self):
        print("\n" + "="*70)
        print("LOADING DATASETS  (corrupt files skipped automatically)")
        print("="*70)

        train_ds = SafeImageFolder(os.path.join(self.data_dir, 'train'),
                                   transform=self.train_transform)
        val_ds   = SafeImageFolder(os.path.join(self.data_dir, 'val'),
                                   transform=self.test_transform)
        test_ds  = SafeImageFolder(os.path.join(self.data_dir, 'test'),
                                   transform=self.test_transform)

        if self.subset_percentage < 1.0:
            t_idx = np.random.choice(len(train_ds),
                                     int(len(train_ds)*self.subset_percentage),
                                     replace=False)
            v_idx = np.random.choice(len(val_ds),
                                     int(len(val_ds)*self.subset_percentage),
                                     replace=False)
            train_ds = Subset(train_ds, t_idx)
            val_ds   = Subset(val_ds,   v_idx)
            print(f"\n  Using {self.subset_percentage*100:.0f}% of data for speed.")

        self.train_loader = DataLoader(train_ds, batch_size=self.batch_size,
                                       shuffle=True,  num_workers=self.num_workers)
        self.val_loader   = DataLoader(val_ds,   batch_size=self.batch_size,
                                       shuffle=False, num_workers=self.num_workers)
        self.test_loader  = DataLoader(test_ds,  batch_size=self.batch_size,
                                       shuffle=False, num_workers=self.num_workers)

        # Auto-calibrate epoch count to fit inside time budget
        bpe = len(self.train_loader)
        spb = {'resnet18': 1.2, 'resnet50': 2.2, 'resnet101': 3.5}
        sec_per_epoch = bpe * spb.get(self.model_name, 2.0)
        budget_sec    = self.target_minutes * 60 * 0.88   # 12% margin for test/plots
        self.num_epochs = min(self._max_epochs,
                              max(5, int(budget_sec / sec_per_epoch)))

        print(f"\nDataset Statistics:")
        print(f"  Train samples:      {len(train_ds):,}")
        print(f"  Validation samples: {len(val_ds):,}")
        print(f"  Test samples:       {len(test_ds):,}")
        print(f"  Batches / epoch:    {bpe}")
        print(f"  Est. min / epoch:   {sec_per_epoch/60:.1f}")
        print(f"  Auto epoch count:   {self.num_epochs}  "
              f"(budget = {self.target_minutes} min)")
        print("="*70)

        base = train_ds.dataset if isinstance(train_ds, Subset) else train_ds
        return base.class_to_idx

    # ── Model building ────────────────────────────────────────────────────────
        # ── Model building ────────────────────────────────────────────────────────
    def build_model(self):

        print("\n" + "="*70)
        print(f"BUILDING {self.model_name.upper()} MODEL")
        print("="*70)

        local = LOCAL_WEIGHTS.get(self.model_name)

        # Load base model safely
        if self.model_name == 'resnet18':
            base = models.resnet18(weights=None)
            self.model = _load_weights_safe(
                models.resnet18,
                models.ResNet18_Weights.IMAGENET1K_V1,
                base,
                local
            )

        elif self.model_name == 'resnet50':
            base = models.resnet50(weights=None)
            self.model = _load_weights_safe(
                models.resnet50,
                models.ResNet50_Weights.IMAGENET1K_V1,
                base,
                local
            )

        else:  # resnet101
            base = models.resnet101(weights=None)
            self.model = _load_weights_safe(
                models.resnet101,
                models.ResNet101_Weights.IMAGENET1K_V1,
                base,
                local
            )

        # Replace classifier
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)

        # Freeze all layers
        for param in self.model.parameters():
            param.requires_grad = False

        
        # Unfreeze layer3
        for param in self.model.layer3.parameters():
            param.requires_grad = True

        # Unfreeze layer4
        for param in self.model.layer4.parameters():
            param.requires_grad = True

        # Unfreeze classifier
        for param in self.model.fc.parameters():
            param.requires_grad = True

        # Stats
        total = sum(p.numel() for p in self.model.parameters())
        trainable = sum(p.numel() for p in self.model.parameters() if p.requires_grad)

        print(f"\nTotal params:     {total:,}")
        print(f"Trainable params: {trainable:,} ({trainable/total*100:.1f}%)")

        # Move to device
        self.model = self.model.to(self.device)

        # Mixed precision
        self.scaler = torch.cuda.amp.GradScaler() if self.device.type == 'cuda' else None

        print(f"\n✓ Model ready on {self.device}")
        print("="*70)   
    # ── Training ──────────────────────────────────────────────────────────────
        # ── Training ──────────────────────────────────────────────────────────────
    def train(self):

        # Handle class imbalance safely
        train_dataset = self.train_loader.dataset

        # If using Subset, extract original dataset
        if isinstance(train_dataset, torch.utils.data.Subset):
            train_dataset = train_dataset.dataset

        targets = [label for _, label in train_dataset.samples]

        class_counts = np.bincount(targets)

        class_weights = 1. / torch.tensor(class_counts, dtype=torch.float)
        class_weights = class_weights / class_weights.sum()
        class_weights = class_weights.to(self.device)
        self.class_weights = class_weights
        criterion = nn.CrossEntropyLoss(weight=class_weights)

        optimizer = optim.AdamW(
            filter(lambda p: p.requires_grad, self.model.parameters()),
            lr=self.learning_rate,
            weight_decay=0.01
        )

        scheduler = optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='max',
            factor=0.5,
            patience=3
        )

        best_val_acc   = 0.0
        patience_limit = 15
        patience_cnt   = 0
        wall_start     = time.time()
        budget_sec     = self.target_minutes * 60

        print("\n" + "="*70)
        print("STARTING TRAINING")
        print("="*70)
        print(f"  Device: {self.device} | Model: {self.model_name}")
        print(f"  Max epochs: {self.num_epochs} | Budget: {self.target_minutes} min")
        print("="*70 + "\n")

        for epoch in range(self.num_epochs):

            ep_start = time.time()

            self.model.train()

            t_loss = 0.0
            t_correct = 0
            t_total = 0

            pbar = tqdm(self.train_loader,
                        desc=f"Epoch {epoch+1}/{self.num_epochs}",
                        ncols=90)

            for inputs, labels in pbar:

                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                optimizer.zero_grad()

                if self.scaler:

                    with torch.cuda.amp.autocast():
                        outputs = self.model(inputs)
                        loss = criterion(outputs, labels)

                    self.scaler.scale(loss).backward()
                    self.scaler.step(optimizer)
                    self.scaler.update()

                else:

                    outputs = self.model(inputs)
                    loss = criterion(outputs, labels)

                    loss.backward()
                    optimizer.step()

                t_loss += loss.item()

                _, pred = torch.max(outputs.data, 1)

                t_total += labels.size(0)
                t_correct += (pred == labels).sum().item()

                pbar.set_postfix(loss=f"{loss.item():.4f}")

            t_loss /= len(self.train_loader)
            t_acc = 100 * t_correct / t_total

            v_loss, v_acc = self.evaluate(self.val_loader)

            old_lr = optimizer.param_groups[0]['lr']
            scheduler.step(v_acc)
            new_lr = optimizer.param_groups[0]['lr']

            if new_lr != old_lr:
                print(f"  📉 LR reduced: {old_lr:.6f} → {new_lr:.6f}")

            self.train_losses.append(t_loss)
            self.val_losses.append(v_loss)

            self.train_accuracies.append(t_acc)
            self.val_accuracies.append(v_acc)

            ep_time = time.time() - ep_start

            print(f"\nEpoch {epoch+1}/{self.num_epochs} ({ep_time/60:.1f} min)")
            print(f"  Train Loss: {t_loss:.4f} | Train Acc: {t_acc:.2f}%")
            print(f"  Val Loss:   {v_loss:.4f} | Val Acc:   {v_acc:.2f}%")

            if v_acc > best_val_acc:

                best_val_acc = v_acc

                self.save_model(
                    f'models/best_{self.model_name}_model.pth'
                )

                print(f"  ✓ Best model saved ({v_acc:.2f}%)")

                patience_cnt = 0

            else:

                patience_cnt += 1

                print(f"  No improvement ({patience_cnt}/{patience_limit})")

            if patience_cnt >= patience_limit:

                print("\n⚠ Early stopping triggered")

                break

        total_time = time.time() - wall_start

        print("\n" + "="*70)
        print("TRAINING COMPLETE")
        print(f"Total time: {total_time/60:.1f} minutes")
        print(f"Best validation accuracy: {best_val_acc:.2f}%")
        print("="*70)

    # ── Evaluation ────────────────────────────────────────────────────────────
    def evaluate(self, loader):
        self.model.eval()
        total_loss, correct, total = 0.0, 0, 0
        criterion = nn.CrossEntropyLoss(weight=self.class_weights)
        with torch.no_grad():
            for inputs, labels in loader:
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                if self.scaler:
                    with torch.cuda.amp.autocast():
                        outputs = self.model(inputs)
                        loss    = criterion(outputs, labels)
                else:
                    outputs = self.model(inputs)
                    loss    = criterion(outputs, labels)
                total_loss += loss.item()
                _, pred = torch.max(outputs.data, 1)
                total   += labels.size(0)
                correct += (pred == labels).sum().item()
        return total_loss / len(loader), 100 * correct / total

    # ── Testing ───────────────────────────────────────────────────────────────
    def test(self):
        print("\n" + "="*70)
        print("TESTING MODEL")
        print("="*70)

        self.model.eval()
        preds, labels_all, probs_all = [], [], []

        with torch.no_grad():
            for inputs, labels in tqdm(self.test_loader, desc="Testing", ncols=80):
                inputs = inputs.to(self.device)
                if self.scaler:
                    with torch.cuda.amp.autocast():
                        outs = self.model(inputs)
                else:
                    outs = self.model(inputs)
                probs = torch.nn.functional.softmax(outs, dim=1)
                _, p  = torch.max(outs.data, 1)
                preds.extend(p.cpu().numpy())
                labels_all.extend(labels.numpy())
                probs_all.extend(probs.cpu().numpy())

        from sklearn.metrics import (accuracy_score, precision_score,
                                     recall_score, f1_score, roc_auc_score)

        acc  = accuracy_score(labels_all, preds) * 100
        prec = precision_score(labels_all, preds, zero_division=0) * 100
        rec  = recall_score(labels_all, preds, zero_division=0) * 100
        f1   = f1_score(labels_all, preds, zero_division=0) * 100
        cm   = confusion_matrix(labels_all, preds)
        tn, fp, fn, tp = cm.ravel()
        spec = tn / (tn + fp) * 100 if (tn + fp) > 0 else 0

        try:
            auc = roc_auc_score(labels_all, np.array(probs_all)[:, 1]) * 100
        except Exception:
            auc = 0.0

        print("\n" + "="*70)
        print("TEST RESULTS")
        print("="*70)
        print(f"  Accuracy:    {acc:.2f}%")
        print(f"  Precision:   {prec:.2f}%")
        print(f"  Recall:      {rec:.2f}%")
        print(f"  Specificity: {spec:.2f}%")
        print(f"  F1-Score:    {f1:.2f}%")
        print(f"  AUC-ROC:     {auc:.2f}%")
        print(f"\n  TP={tp}  TN={tn}  FP={fp}  FN={fn}")
        print("="*70)

        metrics = {self.model_name: {
            'accuracy': float(acc), 'precision': float(prec),
            'recall':   float(rec), 'specificity': float(spec),
            'f1_score': float(f1),  'auc': float(auc)
        }}

        os.makedirs('models', exist_ok=True)
        mf = 'models/metrics.json'
        if os.path.exists(mf):
            with open(mf) as fh:
                old = json.load(fh)
            old.update(metrics); metrics = old
        with open(mf, 'w') as fh:
            json.dump(metrics, fh, indent=4)
        print(f"\n✓ Metrics → {mf}")

        self._plot_confusion(cm)
        self._plot_history()
        return metrics

    def _plot_confusion(self, cm):
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Authentic', 'Forged'],
                    yticklabels=['Authentic', 'Forged'])
        plt.title(f'Confusion Matrix – {self.model_name.upper()}')
        plt.ylabel('True'); plt.xlabel('Predicted')
        plt.tight_layout()
        path = f'models/confusion_matrix_{self.model_name}.png'
        plt.savefig(path, dpi=150); plt.close()
        print(f"✓ Saved {path}")

    def _plot_history(self):
        fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 5))
        ep = range(1, len(self.train_losses) + 1)
        a1.plot(ep, self.train_losses,    'b-o', label='Train')
        a1.plot(ep, self.val_losses,      'r-s', label='Val')
        a1.set(title='Loss', xlabel='Epoch', ylabel='Loss')
        a1.legend(); a1.grid(alpha=0.3)
        a2.plot(ep, self.train_accuracies,'b-o', label='Train')
        a2.plot(ep, self.val_accuracies,  'r-s', label='Val')
        a2.set(title='Accuracy', xlabel='Epoch', ylabel='Accuracy (%)')
        a2.legend(); a2.grid(alpha=0.3)
        plt.tight_layout()
        path = f'models/training_history_{self.model_name}.png'
        plt.savefig(path, dpi=150); plt.close()
        print(f"✓ Saved {path}")

    def save_model(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({
            'model_state_dict':  self.model.state_dict(),
            'model_name':        self.model_name,
            'train_losses':      self.train_losses,
            'val_losses':        self.val_losses,
            'train_accuracies':  self.train_accuracies,
            'val_accuracies':    self.val_accuracies,
        }, path)


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def main():
    print("="*70)
    print("IMAGE FORGERY DETECTION – MODEL TRAINING  (1-hour optimised)")
    print("="*70)

    ds = DatasetPreparation()
    if not ds.verify_dataset():
        print("⚠  Dataset not ready. Run data_preparation.py first.")
        sys.exit(1)

    print("\nTime Budget:")
    print("  1. ~1 hour  (recommended for CPU)")
    print("  2. ~4 hours (full training)")
    budget = input("\nSelect (1 or 2): ").strip()
    target_minutes = 60 if budget != '2' else 240

    print("\nModel Selection:")
    print("  1. ResNet-18  ← FASTEST  (~85-88% acc)  ✓ best choice for 1 hr on CPU")
    print("  2. ResNet-50  (good accuracy, ~2× slower)")
    print("  3. ResNet-101 (best accuracy, ~3× slower)")
    mc = input("\nSelect (1, 2 or 3): ").strip()
    model_name = {'1': 'resnet18', '2': 'resnet50', '3': 'resnet101'}.get(mc, 'resnet18')

    quick_mode = (target_minutes <= 60)

    print("\n" + "="*70)
    print(f"  Model:  {model_name.upper()}")
    print(f"  Budget: {target_minutes} minutes")
    print("="*70)

    detector = ImageForgeryDetector(
        model_name=model_name,
        quick_mode=quick_mode,
        target_minutes=target_minutes
    )

    class_to_idx = detector.load_data()
    print(f"\nClass mapping: {class_to_idx}")

    detector.build_model()
    detector.train()
    detector.test()

    print("\n" + "="*70)
    print("✓ PIPELINE COMPLETED")
    print("="*70)
    print(f"  models/best_{model_name}_model.pth")
    print(f"  models/training_history_{model_name}.png")
    print(f"  models/confusion_matrix_{model_name}.png")
    print("  models/metrics.json")
    print("\nRun:  python app.py")
    print("="*70)


if __name__ == '__main__':
    main()