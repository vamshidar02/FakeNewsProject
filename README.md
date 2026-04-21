# 📰 Fake News Detection System

## Overview

An AI-powered Fake News Detection System built using BERT (Transformers) and Streamlit.
The system classifies news as Fake ❌ or Real ✅ and includes admin validation, analytics, and retraining.

---

## Features
🔐 User & Admin Authentication
🧠 BERT-based NLP Classification
📂 File Upload (.txt support)
🌐 URL News Extraction
📊 Admin Analytics Dashboard
🔄 Continuous Model Retraining

---

## Technologies Used
Python
Transformers (BERT)
PyTorch
Streamlit
SQLite
Pandas
Matplotlib
Newspaper3k

---

##  Project Structure
FakeNewsProject/
│── app.py          # Main logic & routing
│── ui.py           # UI/UX design
│── retrain.py      # Model retraining script
│── database.db     # SQLite database
│── model/          # Trained model (not uploaded)


---

## ⚠️ Note
The trained model is not included due to GitHub size limitations.

---

## ▶️ How to Run
## step-1 Clone the repository
git clone https://github.com/vamshidar02/FakeNewsProject.git
cd FakeNewsProject

## Step - 2 Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

## Step - 3 Install dependencies
pip install -r requirements.txt

## Step - 4 Run the app
streamlit run app.py

## Author
Madupathi Vamshidar

-----
