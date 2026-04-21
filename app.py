# app.py

import streamlit as st
import sqlite3
import torch
import pandas as pd
import os
from transformers import BertTokenizer, BertForSequenceClassification
from newspaper import Article

import ui   # 👈 Import UI

# =========================
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# =========================
# DB
# =========================
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT, role TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS news(id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, label INTEGER, status TEXT)")
conn.commit()

# =========================
# MODEL
# =========================
@st.cache_resource
def load_model():
    model = BertForSequenceClassification.from_pretrained("model")
    tokenizer = BertTokenizer.from_pretrained("model")
    return model, tokenizer

model, tokenizer = load_model()

def predict(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    return torch.argmax(probs).item(), torch.max(probs).item()

# =========================
# AUTH
# =========================
def login(u, p):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (u, p))
    return c.fetchone()

def register(u, p):
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u, p, "user"))
    conn.commit()

# =========================
# URL
# =========================
def fetch_url(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except:
        return ""

# =========================
# ROUTING
# =========================

# LOGIN PAGE
if st.session_state.page == "login":

    u, p = ui.login_page()

    col1, col2 = st.columns(2)

    if col1.button("Login"):
        res = login(u, p)
        if res:
            st.session_state.logged_in = True
            st.session_state.role = res[2]
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.error("Invalid credentials")

    if col2.button("Register Page"):
        st.session_state.page = "register"
        st.rerun()

# REGISTER PAGE
elif st.session_state.page == "register":

    u, p = ui.register_page()

    if st.button("Register"):
        register(u, p)
        st.success("Registered successfully")

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()

# DASHBOARD
elif st.session_state.page == "dashboard":

    if st.sidebar.button("Logout"):
        st.session_state.page = "login"
        st.session_state.logged_in = False
        st.rerun()

    # USER
    if st.session_state.role == "user":

        text, url = ui.user_page()

        if url:
            text = fetch_url(url)

        if st.button("Analyze"):
            pred, conf = predict(text)

            c.execute("INSERT INTO news(text,label,status) VALUES(?,?,?)",
                      (text, pred, "pending"))
            conn.commit()

            ui.show_result(pred, conf)

    # ADMIN
    elif st.session_state.role == "admin":

        ui.admin_page()

        c.execute("SELECT * FROM news WHERE status='pending'")
        rows = c.fetchall()

        for row in rows:
            st.write(row[1][:200])

            if st.button(f"Fake {row[0]}"):
                c.execute("UPDATE news SET label=0,status='approved' WHERE id=?", (row[0],))
                conn.commit()
                st.rerun()

            if st.button(f"Real {row[0]}"):
                c.execute("UPDATE news SET label=1,status='approved' WHERE id=?", (row[0],))
                conn.commit()
                st.rerun()

        if st.button("🔄 Retrain"):
            os.system("python retrain.py")
            st.success("Model retrained")
            # =========================
            # ANALYTICS DASHBOARD
            # =========================
            st.subheader("📊 Analytics Dashboard")
            df = pd.read_sql_query("SELECT * FROM news WHERE status='approved'", conn)
            if not df.empty:
                # Count values
                counts = df['label'].value_counts()
                
                # Bar Chart
                st.write("### Fake vs Real Distribution")
                st.bar_chart(counts)
                
                # Pie Chart
                
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                ax.pie(counts, labels=["Fake", "Real"], autopct='%1.1f%%')
                st.pyplot(fig)
                
                # Additional stats
                st.write("### Statistics")
                st.write(f"Total News: {len(df)}")
                st.write(f"Fake News: {counts.get(0, 0)}")
                st.write(f"Real News: {counts.get(1, 0)}")
            else:
                st.info("No approved data yet")