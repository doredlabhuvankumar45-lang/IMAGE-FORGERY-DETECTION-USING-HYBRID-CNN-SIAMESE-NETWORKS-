# IMAGE-FORGERY-DETECTION-USING-HYBRID-CNN-SIAMESE-NETWORK
pring Boot Todo Management App

A full-stack Todo Management Application built using Spring Boot, Java 21, HTML, CSS, and JavaScript. This application helps users organize, track, and manage daily tasks efficiently through a responsive web interface and RESTful backend APIs. It supports user authentication, task creation, updating, deletion, filtering, priority management, and due-date tracking.

Features
User Registration and Login
Create, Read, Update, and Delete (CRUD) Tasks
Task Priority Management (High, Medium, Low)
Due Date Tracking
Task Completion Status Toggle
Search Functionality
Filter Tasks by Status and Priority
Responsive UI for Desktop, Tablet, and Mobile
RESTful API Integration
User-Specific Task Management
Secure Data Isolation

Tech Stack
Frontend
HTML5
CSS3
JavaScript (ES6)
Font Awesome
Google Fonts
Backend
Java 21
Spring Boot 3.5.11
Spring Data JPA
Hibernate ORM
H2 Database
Lombok
Maven
Development Tools
IntelliJ IDEA
Visual Studio Code
Postman
MySQL Workbench

Project Architecture
Frontend (HTML/CSS/JS)
        |
        | REST API Calls
        v
Spring Boot Backend
        |
        v
Service Layer
        |
        v
Repository Layer
        |
        v
H2/MySQL Database

The application follows a layered architecture consisting of:

Controller Layer
Service Layer
Repository Layer
DTO Layer
Database Layer

Database Design

The application uses five normalized tables:

Users
Todos
Priorities
Categories
Task History

Relationships:

One User → Many Todos
One Priority → Many Todos
One Category → Many Todos
One Todo → Many Task History Records

REST API Endpoints
Authentication
POST /api/auth/register
POST /api/auth/login
Todo Operations
GET    /api/todos/user/{userId}
GET    /api/todos/user/{userId}/status
GET    /api/todos/user/{userId}/priority/{priorityId}
GET    /api/todos/user/{userId}/due
POST   /api/todos/user/{userId}
PUT    /api/todos/{todoId}
PATCH  /api/todos/{todoId}/toggle
DELETE /api/todos/{todoId}

Project Structure
src
├── main
│   ├── java
│   │   ├── controller
│   │   ├── service
│   │   ├── repository
│   │   ├── model
│   │   ├── dto
│   │   └── TodoManagementApplication.java
│   │
│   └── resources
│       ├── application.properties
│       └── data.sql
│
└── frontend
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── styles.css
    └── app.js
Installation & Setup
Clone Repository
git clone https://github.com/your-username/spring-boot-todo-management-app.git
cd spring-boot-todo-management-app
Build Project
mvn clean install
Run Application
mvn spring-boot:run

Backend Server:

http://localhost:8080

Frontend:

Open index.html in a browser or serve using a local web server.

Functionalities
User Management
Register New User
Login Authentication
Session Management
Task Management
Add New Tasks
Edit Existing Tasks
Delete Tasks
Mark Tasks as Completed
Assign Priority Levels
Set Due Dates
Filtering & Search
Filter by Status
Filter by Priority
Search by Title or Description

Testing

The application has been tested for:

Unit Testing
Integration Testing
UI Testing
Functional Testing
Performance Testing
Error Handling Testing

Results confirmed successful authentication, task CRUD operations, filtering, search, and responsive behavior across major browsers.

Future Enhancements
JWT Authentication
BCrypt Password Encryption
Email Notifications
File Attachments
Recurring Tasks
Team Collaboration
Mobile Applications
Dark Mode
Cloud Deployment
Real-Time Synchronization
Calendar Integration
AI-Powered Task Scheduling
Docker Support
Swagger API Documentation

Learning Outcomes
Full Stack Web Development
Spring Boot REST API Development
Database Design & Normalization
Frontend–Backend Integration
Git Version Control
Software Documentation Practices

Author

K. Sharoon
Roll No: 22NE1A0460

License

This project is developed for educational and academic purposes.

complete read me
📝 Spring Boot Todo Management App

A modern Full-Stack Todo Management Application developed using Spring Boot, Java 21, Spring Data JPA, Hibernate, H2 Database, HTML5, CSS3, and JavaScript. The application enables users to efficiently manage daily tasks through a responsive interface while providing secure authentication, task prioritization, due-date tracking, filtering, and search functionality.

📌 Project Overview

Managing personal and professional tasks effectively is essential in today's fast-paced world. This project provides a centralized platform where users can create, organize, prioritize, update, and monitor tasks in real time.

The application follows a client-server architecture with a responsive frontend and a robust Spring Boot backend connected through RESTful APIs.

Key Objectives
Develop a responsive task management system.
Implement secure user authentication.
Enable task CRUD operations.
Support task prioritization and categorization.
Provide filtering and search capabilities.
Maintain normalized database design.
Ensure scalability and maintainability through layered architecture.
🚀 Features
👤 User Management
User Registration
User Login
Session Management
User-specific Task Access
Authentication Validation
✅ Task Management
Create New Tasks
View All Tasks
Update Existing Tasks
Delete Tasks
Mark Tasks as Completed
Toggle Completion Status
📅 Task Organization
Due Date Tracking
Priority Levels (High, Medium, Low)
Category Assignment
Task History Tracking
🔍 Search & Filter
Filter by Status
Filter by Priority
Search by Title
Search by Description
📊 Dashboard
Total Tasks Count
Completed Tasks Count
Pending Tasks Count
Real-Time Updates
📱 Responsive Design
Desktop Support
Tablet Support
Mobile Support
🛠️ Technology Stack
Frontend
Technology	Purpose
HTML5	Page Structure
CSS3	Styling & Layout
JavaScript ES6	Client-Side Logic
Font Awesome	Icons
Google Fonts	Typography
Backend
Technology	Purpose
Java 21	Programming Language
Spring Boot 3.5.11	Backend Framework
Spring Data JPA	Data Access Layer
Hibernate ORM	Object Relational Mapping
H2 Database	Development Database
Lombok	Boilerplate Reduction
Maven	Dependency Management
Development Tools
IntelliJ IDEA
Visual Studio Code
Postman
MySQL Workbench
Git & GitHub
🏗️ System Architecture
+--------------------+
|     Frontend       |
| HTML CSS JavaScript|
+---------+----------+
          |
          | REST API
          v
+--------------------+
|   Spring Boot API  |
+---------+----------+
          |
          v
+--------------------+
|   Service Layer    |
+---------+----------+
          |
          v
+--------------------+
| Repository Layer   |
+---------+----------+
          |
          v
+--------------------+
| H2 / MySQL Database|
+--------------------+
📂 Project Structure
todo-management-app
│
├── src
│   ├── main
│   │   ├── java
│   │   │   ├── controller
│   │   │   ├── service
│   │   │   ├── repository
│   │   │   ├── model
│   │   │   ├── dto
│   │   │   └── TodoManagementApplication.java
│   │   │
│   │   └── resources
│   │       ├── application.properties
│   │       └── data.sql
│   │
│   └── test
│
├── frontend
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── style.css
│   └── app.js
│
├── pom.xml
└── README.md
🗄️ Database Design

The database follows Third Normal Form (3NF) and consists of five related tables.

Users

Stores account information.

Column
id
username
email
password
full_name
created_at
updated_at
Priorities

Stores predefined priority levels.

Column
priority_id
level
value
color_code
Categories

Stores task categories.

Column
category_id
name
description
color_code
user_id
Todos

Stores task information.

Column
todo_id
title
description
due_date
completed
user_id
category_id
priority_id
Task History

Maintains audit logs.

Column
history_id
todo_id
user_id
action_type
changed_at
🔗 REST API Endpoints
Authentication APIs
Register User
POST /api/auth/register
Login User
POST /api/auth/login
Todo APIs
Get User Tasks
GET /api/todos/user/{userId}
Filter by Status
GET /api/todos/user/{userId}/status
Filter by Priority
GET /api/todos/user/{userId}/priority/{priorityId}
Get Tasks Due Between Dates
GET /api/todos/user/{userId}/due
Create Task
POST /api/todos/user/{userId}
Update Task
PUT /api/todos/{todoId}
Toggle Status
PATCH /api/todos/{todoId}/toggle
Delete Task
DELETE /api/todos/{todoId}
⚙️ Installation Guide
Clone Repository
git clone https://github.com/yourusername/todo-management-app.git
cd todo-management-app
Build Project
mvn clean install
Run Application
mvn spring-boot:run

Backend runs at:

http://localhost:8080
Access H2 Database Console
http://localhost:8080/h2-console

Default configuration:

JDBC URL: jdbc:h2:mem:testdb
Username: sa
Password:
🖥️ Application Screens
Landing Page
Application Introduction
Feature Highlights
Registration & Login Navigation
Login Page
Email Authentication
Form Validation
Session Creation
Registration Page
User Account Creation
Password Validation
Terms Acceptance
Dashboard
Task Creation
Task Listing
Filtering
Statistics
Edit Modal
🔄 Application Workflow
Authentication Flow
User Login
     ↓
Frontend Validation
     ↓
POST Request
     ↓
Spring Boot Authentication
     ↓
Database Verification
     ↓
Session Creation
     ↓
Dashboard Access
Task Creation Flow
Create Task
     ↓
Frontend Validation
     ↓
POST API Request
     ↓
Backend Validation
     ↓
Database Storage
     ↓
Response Returned
     ↓
Dashboard Updated
🧪 Testing
Unit Testing
Form Validation
Search Functions
Date Formatting
Integration Testing
API Endpoints
Authentication Flow
CRUD Operations
UI Testing
Chrome
Firefox
Edge
Functional Testing
Registration
Login
Task Creation
Task Editing
Task Deletion
Filtering
Search
Performance Testing
Fast API Response
Efficient Task Rendering
🔒 Security Features
User-specific Data Access
Authentication Validation
Form Validation
Input Sanitization
Error Handling
Data Integrity Constraints
📈 Future Enhancements
Short-Term
JWT Authentication
BCrypt Password Encryption
Email Notifications
File Attachments
Custom Categories
Medium-Term
Recurring Tasks
Team Collaboration
Mobile Applications
CSV/PDF Export
Dark Mode
Long-Term
Cloud Deployment
Real-Time Synchronization
AI Task Suggestions
Google Calendar Integration
Analytics Dashboard
Technical Improvements
Unit Test Coverage
Swagger Documentation
Docker Containerization
Redis Caching
Performance Optimization
🎯 Learning Outcomes

Through this project, the following skills were developed:

Full Stack Web Development
Spring Boot Development
REST API Design
Database Modeling
Hibernate ORM
Frontend Development
Debugging & Testing
Git Version Control
Software Documentation
👨‍💻 Author

K. Sharoon
Roll No: 22NE1A0460

📄 License

This project is developed for academic and educational purposes. Feel free to use and modify it for learning and research purposes.

⭐ If you found this project useful, give it a star on GitHub!

batch 7.pdf
PDF
Presentation 7_35.pptx
Presentation
readme
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
