# Yoga Motion AI

## An Artificial Intelligence Based Real-Time Yoga Posture Analysis and Correction System Using Computer Vision

Yoga Motion AI is an AI-powered web application that analyzes yoga poses in real time using a webcam. It combines computer vision, MediaPipe pose landmarks, feature engineering, and a Random Forest machine learning classifier to recognize yoga poses and provide posture feedback.

The system is developed as a Project Exhibition-I project for the Integrated M.Tech Artificial Intelligence program at VIT Bhopal University.

---

## Project Overview

Yoga practitioners, especially beginners, may find it difficult to determine whether their posture is correct while exercising without continuous guidance from an instructor.

Yoga Motion AI addresses this problem by using a normal webcam to:

- Detect the user's body pose in real time.
- Extract human body landmarks using MediaPipe Pose.
- Convert landmarks into numerical features.
- Classify the performed yoga pose using a trained Random Forest model.
- Analyze posture for supported poses.
- Provide real-time corrective feedback.
- Generate a 30-second session summary.

No specialized wearable sensor or additional hardware is required.

---

## Key Features

- Real-time webcam-based yoga pose detection.
- MediaPipe-based human pose landmark extraction.
- 33 body landmarks.
- 132 numerical pose features.
- Machine learning-based pose classification.
- Random Forest classifier with 200 estimators.
- 10 trained yoga pose classes.
- Real-time posture feedback.
- Confidence estimation for pose predictions.
- Uncertain-pose handling.
- 30-second session analysis.
- Posture score calculation.
- Most detected pose identification.
- Average confidence calculation.
- React + Vite frontend.
- FastAPI backend.
- Automated Python tests.
- GitHub-ready project structure.

---

## System Pipeline

```text
User
  ↓
Webcam
  ↓
React Frontend
  ↓
Frame Capture
  ↓
FastAPI Backend
  ↓
MediaPipe Pose Detection
  ↓
33 Body Landmarks
  ↓
132 Numerical Features
  ↓
Random Forest Classifier
  ↓
Pose Prediction + Confidence
  ↓
Posture Analysis
  ↓
Corrective Feedback
  ↓
30-Second Session Report
System Architecture
                    ┌─────────────────────┐
                    │       User          │
                    │   Performs Yoga     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Webcam         │
                    └──────────┬──────────┘
                               │
                               ▼
              ┌────────────────────────────────┐
              │       React + Vite Frontend    │
              │                                │
              │  Camera + UI + Feedback +      │
              │       Session Report            │
              └───────────────┬────────────────┘
                              │
                         HTTP Request
                              │
                              ▼
              ┌────────────────────────────────┐
              │          FastAPI Backend       │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │       MediaPipe Pose           │
              │       33 Landmarks             │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │      Feature Extraction        │
              │       132 Numerical Features   │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │    Random Forest Classifier    │
              │       200 Estimators           │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │      Posture Analysis          │
              └───────────────┬────────────────┘
                              │
                              ▼
              ┌────────────────────────────────┐
              │   Real-Time Feedback + Report  │
              └────────────────────────────────┘
Machine Learning Model
The project uses a supervised machine learning approach for yoga pose classification.
Dataset
The dataset contains 1,000 samples distributed across 10 pose classes.
Each class contains 100 samples.
Pose Class	Samples
Mountain	100
Raised Hands	100
Warrior II	100
Tree	100
T Pose	100
Hands on Hips	100
Side Stretch	100
Chair	100
Forward Bend	100
Wide Leg Standing	100
Total	1,000
Dataset Split
Dataset	Samples
Training	800
Testing	200
Total	1,000
Feature Representation
MediaPipe provides 33 body landmarks.
The project converts detected landmarks into 132 numerical features for machine learning.
Classifier
Random Forest
Number of estimators: 200
The trained model and label encoder are included in the models/ directory.
Model Performance
The trained Random Forest model achieved:
Metric	Result
Test Accuracy	94%
Macro F1 Score	0.94
These results were obtained using the project's 200-sample test set.
Real-Time Validation
A 30-second T-Pose session was tested using the running application.
Metric	Result
Detected Frames	29
Correct Posture Frames	24
Correction-Needed Frames	2
No-Pose Frames	0
Posture Score	92.3%
Average ML Confidence	41.0%
The posture score is calculated from the frames for which posture analysis produced a correct/incorrect result.
Supported Pose Classes
The machine learning model was trained on:
Mountain
Raised Hands
Warrior II
Tree
T Pose
Hands on Hips
Side Stretch
Chair
Forward Bend
Wide Leg Standing
Detailed rule-based posture analysis is currently implemented for:
Tree
T Pose
Mountain
Raised Hands
Warrior II
Hands on Hips
Side Stretch
The remaining trained classes are recognized by the machine learning classifier but have limited posture-analysis rules in the current Project Exhibition-I version.
Technology Stack
Frontend
React
Vite
JavaScript
HTML
CSS
Browser Webcam API
Backend
Python
FastAPI
Uvicorn
Pydantic
Artificial Intelligence / Computer Vision
MediaPipe Pose
NumPy
Pandas
Scikit-learn
OpenCV
Machine Learning
Random Forest Classifier
Landmark-based feature engineering
Supervised classification
Testing
Pytest
Project Structure
Yoga-Motion-AI/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── pose_engine.py
│   ├── features.py
│   ├── posture.py
│   └── yoga_analyzer.py
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── docs/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── models/
│   ├── yoga_pose_classifier.joblib
│   └── label_encoder.joblib
│
├── scripts/
│
├── tests/
│   ├── test_api.py
│   ├── test_features.py
│   ├── test_landmark_extraction.py
│   ├── test_pose_visualization.py
│   └── test_posture.py
│
├── training/
│   ├── collect_data.py
│   ├── prepare_dataset.py
│   ├── train.py
│   ├── evaluate.py
│   └── inference.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
Requirements
Hardware
Webcam
Internet connection for initial package installation
Recommended modern CPU
The application does not require specialized yoga sensors or wearable devices.
Software
Python 3.12
Node.js
npm
Git
Conda or Python virtual environment
Installation
1. Clone the Repository
git clone https://github.com/chandan25mim10179-bit/Yoga-Motion-AI.git
cd Yoga-Motion-AI
2. Activate the Python Environment
conda activate yoga-ai
The project was developed and tested using Python 3.12.
3. Install Python Dependencies
pip install -r requirements.txt
4. Install Frontend Dependencies
npm install --prefix frontend
Running the Backend
From the project root:
conda activate yoga-ai
uvicorn backend.main:app --reload
The backend runs at:
http://127.0.0.1:8000
Health endpoint:
GET /health
Frame analysis endpoint:
POST /analyze-frame
Running the Frontend
Open another Terminal window:
cd /Users/chandankumarsahu/Yoga-Motion-AI
npm run dev --prefix frontend
Open the local URL displayed by Vite in the terminal.
Allow webcam access when the browser requests permission.
API Endpoints
Health Check
GET /health
Example response:
{
  "status": "healthy",
  "service": "Yoga Motion AI"
}
Analyze Frame
POST /analyze-frame
The endpoint performs:
Pose landmark detection.
Feature extraction.
Pose classification.
Confidence calculation.
Posture analysis.
Feedback generation.
Testing
Run the automated tests:
conda activate yoga-ai
pytest
The current verified test run reports:
3 passed, 2 warnings
Model Files
The trained machine learning files are included in:
models/
Files:
yoga_pose_classifier.joblib
label_encoder.joblib
The model is therefore available directly when the repository is cloned.
Real-Time Feedback
The application provides feedback based on the detected pose and posture rules.
Example:
Good T Pose! Keep both arms extended and horizontal.
Correction feedback can include:
Raise your left hand higher.
When the pose cannot be confidently recognized, the system reports an uncertain pose and asks the user to stand clearly and face the camera.
Session Report
The application maintains statistics during a 30-second session, including:
Total frames
Detected frames
No-pose frames
Correct posture frames
Correction-needed frames
Pose counts
Uncertain frames
Average ML confidence
Posture score
Most detected pose
Main feedback
Limitations
Performance depends on webcam quality and lighting.
Pose detection may become less reliable when the body is partially outside the camera frame.
Multiple people in the frame are not the intended use case.
Extreme camera angles may affect landmark detection.
ML confidence can vary between different users and environments.
The training dataset is relatively small.
The dataset contains 1,000 samples.
Detailed posture analysis is not yet implemented for every trained pose.
The current system is designed primarily for a single person.
The application is intended as an educational/assistive system and does not replace professional yoga instruction.
Future Enhancements
Increase the size and diversity of the training dataset.
Add more yoga poses.
Implement posture rules for all trained poses.
Improve confidence calibration.
Add temporal pose analysis.
Support multiple users.
Improve robustness under different lighting conditions.
Add voice-based feedback.
Add progress tracking across multiple sessions.
Deploy the application as a cloud service.
Improve mobile compatibility.
Add personalized posture recommendations.
Project Team
Name	Registration Number	Role
Vivek Varma Ketthe	25MIM10080	Lead
Chandan Kumar Sahu	25MIM10179	Team Member
Shivani	25MIM10234	Team Member
Vanshikha Dadhich	25MIM10065	Team Member
Anupriya	25MIM10170	Team Member
Faculty
Supervisor: Dr. Satyendra Singh — 100732
Reviewer 1: Dr. Velmani Ramasamy — 100704
Reviewer 2: Dr. Rakesh Shrivastava — 100642
Academic Context
Integrated Master of Technology in Artificial Intelligence
School of Computing Science and Engineering
VIT Bhopal University
Project Exhibition-I
Repository
GitHub Repository:
https://github.com/chandan25mim10179-bit/Yoga-Motion-AI
Conclusion
Yoga Motion AI demonstrates how computer vision and machine learning can be combined to create a real-time yoga posture analysis system using an ordinary webcam.
The Project Exhibition-I implementation integrates:
Computer Vision
      +
Pose Landmark Detection
      +
Feature Engineering
      +
Machine Learning
      +
Posture Analysis
      +
Real-Time Feedback
      +
Web Application
The trained model achieved 94% test accuracy and a 0.94 macro F1 score on the project's test dataset.
License
This project is developed for academic and educational purposes as part of the Integrated M.Tech Artificial Intelligence program at VIT Bhopal University.