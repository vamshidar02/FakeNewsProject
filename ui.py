# ui.py

import streamlit as st

# =========================
# GLOBAL STYLE
# =========================
def load_css():
    st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f5f5f5;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
def login_page():
    load_css()
    st.markdown('<div class="main-title">🔐 Login</div>', unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    return username, password

# =========================
# REGISTER PAGE
# =========================
def register_page():
    load_css()
    st.markdown('<div class="main-title">📝 Register</div>', unsafe_allow_html=True)

    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")

    return username, password

# =========================
# USER DASHBOARD
# =========================
def user_page():
    load_css()
    st.markdown('<div class="main-title">📰 Analyze News</div>', unsafe_allow_html=True)

    input_type = st.radio("Choose Input", ["Text", "File", "URL"])
    text = ""

    if input_type == "Text":
        text = st.text_area("Enter news")

    elif input_type == "File":
        file = st.file_uploader("Upload txt", type=["txt"])
        if file:
            text = file.read().decode("utf-8")

    elif input_type == "URL":
        url = st.text_input("Enter URL")
        return text, url

    return text, None

# =========================
# RESULT DISPLAY
# =========================
def show_result(pred, conf):
    if pred == 0:
        st.markdown(f"""
        <div class="card" style="background:#ffcccc;">
        ❌ Fake News<br>Confidence: {conf:.2f}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card" style="background:#ccffcc;">
        ✅ Real News<br>Confidence: {conf:.2f}
        </div>
        """, unsafe_allow_html=True)

# =========================
# ADMIN PAGE
# =========================
def admin_page():
    load_css()
    st.markdown('<div class="main-title">👨‍💼 Admin Dashboard</div>', unsafe_allow_html=True)