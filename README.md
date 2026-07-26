# 🛡️ AI-Based Network Intrusion Detection System (AI-NIDS)

An AI-powered **Network Intrusion Detection System (NIDS)** built using **Python, Scikit-learn, and Streamlit**. The project uses the **NSL-KDD dataset** to train a Random Forest machine learning model that detects malicious network traffic and displays results through an interactive web dashboard.

---

## 📌 Project Overview

This project demonstrates how Artificial Intelligence can improve cybersecurity by automatically identifying suspicious network traffic.

The system:

- Trains a Random Forest classifier using the NSL-KDD dataset.
- Detects whether network traffic is **Normal** or an **Attack**.
- Displays live packet monitoring through a Streamlit dashboard.
- Generates real-time intrusion alerts.
- Shows packet statistics and traffic visualizations.

---

## 🚀 Features

- 🤖 AI-based intrusion detection
- 🛡️ Random Forest Machine Learning model
- 📊 Interactive Streamlit dashboard
- 🚨 Real-time attack alerts
- 📦 Live packet monitoring
- 📈 Traffic statistics
- 💾 Saved trained model for fast loading
- 🖥️ Simple and easy-to-use interface

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib
- Git & GitHub

---

## 📂 Project Structure

```
AI_NIDS_Project/
│── app.py
│── train_model.py
│── requirements.txt
│── README.md
│
├── data/
│   ├── KDDTrain+.txt
│   └── KDDTest+.txt
│
├── nids_model.pkl
├── feature_encoders.pkl
└── target_encoder.pkl
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_NIDS_Project.git

cd AI_NIDS_Project
```

---

### Create a virtual environment

```bash
python -m venv venv
```

Activate it

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📥 Dataset

Download the **NSL-KDD Dataset** and place these files inside the `data/` folder:

```
KDDTrain+.txt
KDDTest+.txt
```

---

## 🧠 Train the AI Model

Run

```bash
python train_model.py
```

This will:

- Load the dataset
- Preprocess the data
- Train the Random Forest model
- Evaluate model performance
- Save the trained model

Generated files:

```
nids_model.pkl

feature_encoders.pkl

target_encoder.pkl
```

---

## ▶️ Run the Dashboard

```bash
streamlit run app.py
```

Open your browser at

```
http://localhost:8501
```

---

## 🔄 Workflow

```
NSL-KDD Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
Feature Encoding
        │
        ▼
Random Forest Training
        │
        ▼
Model Evaluation
        │
        ▼
Save Model (.pkl)
        │
        ▼
Streamlit Dashboard
        │
        ▼
Live Traffic Simulation
        │
        ▼
AI Prediction
        │
        ▼
Normal Traffic / Intrusion Alert
```

---

## 📊 Sample Output

The dashboard displays:

- Total Packets Scanned
- Normal Traffic Count
- Threat Detection Count
- Live Packet Log
- Intrusion Alerts
- Traffic Charts

---

## 🎯 Future Improvements

- Live packet capture using Scapy
- Deep Learning models
- Attack type classification
- Email notifications
- PDF security reports
- Interactive threat map
- User authentication
- Cloud deployment

---

## 📚 Dataset

NSL-KDD Dataset

Used for training and evaluating the intrusion detection model.

---

## 👨‍💻 Author

**Annant Rana**

B.Tech Computer Science (Cyber Security)

VIT Bhopal University

GitHub: https://github.com/YOUR_USERNAME

LinkedIn: https://linkedin.com/in/YOUR_LINKEDIN

---

## 📄 License

This project is developed for educational and research purposes.

