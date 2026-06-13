# IMAGE-FORGERY-DETECTION-USING-HYBRID-CNN-SIAMESE-NETWORK
🖼️ Image Forgery Detection Using Hybrid CNN–Siamese Networks
📌 Project Overview

Image Forgery Detection Using Hybrid CNN–Siamese Networks is a deep learning-based forensic system designed to identify manipulated or forged digital images. The system combines the feature extraction capabilities of Convolutional Neural Networks (CNNs) with the similarity-learning power of Siamese Networks to detect image tampering such as copy-move forgery, image splicing, object removal, and retouching. The trained model is deployed through a Flask-based web application, allowing users to upload images and instantly determine whether they are authentic or forged.

🚀 Features
Detection of Forged and Authentic Images
Hybrid CNN–Siamese Network Architecture
Copy-Move Forgery Detection
Image Splicing Detection
Deep Learning-Based Feature Extraction
Similarity Learning for Duplicate Region Detection
Flask-Based Web Interface
Real-Time Prediction System
Image Upload and Analysis
Confidence-Based Classification
User-Friendly Interface
High Accuracy Image Verification
🎯 Objectives
Improve robustness of image forgery detection.
Detect multiple types of image manipulation.
Extract deep spatial and statistical image features.
Compare image regions using Siamese Networks.
Evaluate performance under real-world distortions.
Provide a practical web-based forgery detection system.
🛠️ Technology Stack
Programming Language
Python 3.x
Deep Learning Frameworks
TensorFlow
Keras
PyTorch
Image Processing Libraries
OpenCV
NumPy
PIL (Python Imaging Library)
Data Handling
Pandas
Scikit-Learn
Visualization
Matplotlib
Seaborn
Web Development
Flask
HTML5
CSS3
JavaScript
Development Environment
Visual Studio Code
Google Colab
Jupyter Notebook
🏗️ System Architecture
Input Image
      │
      ▼
Image Preprocessing
      │
      ▼
CNN Feature Extraction
      │
      ▼
Siamese Similarity Learning
      │
      ▼
Model Training
      │
      ▼
Model Evaluation
      │
      ▼
Flask Deployment
      │
      ▼
Prediction Result

The architecture combines CNN-based feature extraction with Siamese similarity comparison to identify manipulated image regions and classify images as authentic or forged.

📂 Project Structure
Image-Forgery-Detection/
│
├── dataset/
│   ├── authentic/
│   ├── forged/
│
├── models/
│   ├── cnn_model.py
│   ├── siamese_model.py
│   └── trained_model.h5
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── result.html
│
├── app.py
├── train.py
├── evaluate.py
├── requirements.txt
└── README.md
📊 Dataset Description

The project utilizes benchmark image forgery datasets:

CASIA v2.0
12,000+ Authentic Images
7,000+ Manipulated Images
Supports Splicing Detection
CoMoFoD
Designed for Copy-Move Forgery Detection
Includes Noise and Compression Variations
NC2016
NIST Forensic Dataset
Contains Realistic Image Manipulations
Used for Robustness Evaluation

These datasets contain multiple forgery types such as copy-move, splicing, object insertion, and object removal.

⚙️ Working Methodology
Step 1: Data Collection
Collect authentic and forged images.
Gather images from benchmark datasets.
Organize images based on manipulation categories.
Step 2: Image Preprocessing
Resize images.
Normalize pixel values.
Remove noise.
Perform data augmentation.
Rotation
Flipping
Scaling
Cropping
Step 3: CNN Feature Extraction

CNN automatically learns:

Edges
Textures
Noise Patterns
Structural Information

These extracted features help identify image tampering.

Step 4: Siamese Similarity Learning

The Siamese Network:

Compares image patches.
Measures feature similarity.
Detects duplicated regions.
Identifies copy-move manipulations.

Step 5: Model Training
Split Dataset
Training Set
Validation Set
Testing Set
Train Hybrid CNN-Siamese Model
Optimize Hyperparameters
Step 6: Model Evaluation

Performance metrics:

Accuracy
Precision
Recall
Specificity
F1-Score
Step 7: Deployment

Deploy trained model using Flask.

Users upload images through the web interface and receive instant authenticity predictions.

📈 Performance Results
Metric	ResNet18
Accuracy	96.9%
Precision	98.6%
Recall	98.6%
Specificity	96.9%
F1-Score	97.8%
Confusion Matrix Results
TP = 1207
TN = 1180
FP = 17
FN = 10

Performance demonstrates strong capability in distinguishing forged images from authentic ones.

🌐 Web Application

The Flask web application provides:

User Features
Upload Image
Analyze Image
Receive Prediction
View Confidence Score
Compare Original and Suspicious Images
Prediction Results
Authentic Image
Forged Image
Similarity Analysis
Confidence Percentage

The web interface enables real-time forgery detection through a browser-based platform.

🔍 Types of Forgeries Detected
Copy-Move Forgery

Duplicating one image region and pasting it elsewhere in the same image.

Image Splicing

Combining regions from multiple images.

Object Removal

Removing important objects from images.

Retouching

Altering image appearance without changing overall content.

AI-Generated Manipulations

Deepfake-like image modifications.

🧪 Installation
Clone Repository
git clone https://github.com/yourusername/Image-Forgery-Detection.git
cd Image-Forgery-Detection
Install Dependencies
pip install -r requirements.txt
Train Model
python train.py
Run Application
python app.py
Open Browser
http://127.0.0.1:5000
📱 Applications
Digital Forensics
Criminal Investigations
Evidence Verification
Journalism
News Image Authentication
Social Media
Fake Content Detection
Misinformation Prevention
Cybersecurity
Fraud Detection
Identity Verification
Insurance
Claim Verification
E-Commerce
Product Image Authentication

🔒 Advantages
High Detection Accuracy
Automated Forgery Detection
Reduced Human Intervention
Real-Time Analysis
User-Friendly Interface
Scalable Architecture
Supports Multiple Forgery Types
Easy Deployment
Efficient Feature Learning
Robust Against Image Manipulations

🔮 Future Enhancements
Detection of AI-Generated Images
Deepfake Video Detection
Blockchain-Based Image Verification
Explainable AI Visualization
Region Highlighting of Forged Areas
Federated Learning Integration
Mobile Application Development
Cloud Deployment
Real-Time Monitoring Systems

👨‍💻 Team Members
G. Pujitha (22NE1A0439)
D. Bhuvan Kumar (22NE1A0429)
B. Divya (22NE1A0418)
G. Venu (22NE1A0440)

Project Guide: Mrs. G. Suseelamma, M.Tech., (Ph.D.), Associate Professor

📄 License

This project is developed for academic and research purposes. It can be used for educational learning, experimentation, and digital image forensic studies.
