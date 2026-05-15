import streamlit as st
import pandas as pd
import joblib
import json
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #f5f7ff, #eef2ff);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141e61, #0f044c);
    color: white;
}

/* Main Title */
.main-title {
    font-size: 48px;
    font-weight: bold;
    color: #111827;
}

/* Subtitle */
.subtitle {
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 20px;
}

/* Card */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

/* Section Heading */
.section-title {
    font-size: 24px;
    font-weight: bold;
    color: #7c3aed;
    margin-bottom: 15px;
}

/* Predict Button */
div.stButton > button {
    width: 100%;
    background: linear-gradient(to right, #7c3aed, #2563eb);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}

/* Small Result Box */
.result-box {
    background-color: #ecfdf5;
    padding: 15px;
    border-radius: 12px;
    border-left: 6px solid #22c55e;
    margin-top: 20px;
}

/* Score */
.score-text {
    font-size: 34px;
    font-weight: bold;
    color: #16a34a;
}

/* Tip Box */
.tip-box {
    background-color: #eff6ff;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
    color: #2563eb;
    font-size: 15px;
}

/* Feature Box */
.feature-box {
    background-color: rgba(255,255,255,0.1);
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# USER FILE
# =========================
USER_FILE = "users.json"

if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"students": {}, "parents": {}}, f)

with open(USER_FILE, "r") as f:
    users = json.load(f)

# =========================
# SESSION STATES
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown("# 🎓 Student Predictor")

# Navigation Buttons
if not st.session_state.logged_in:

    if st.sidebar.button("🔐 Login"):
        st.session_state.page = "Login"

    if st.sidebar.button("📝 Sign Up"):
        st.session_state.page = "Sign Up"

st.sidebar.markdown("---")

# Features
st.sidebar.markdown("## ✨ Features")

st.sidebar.markdown("""
<div class="feature-box">
📊 AI-Based Prediction
</div>

<div class="feature-box">
🎯 Accurate Score Estimation
</div>

<div class="feature-box">
👨‍🎓 Student & Parent Login
</div>

<div class="feature-box">
📚 Personalized Insights
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Logout
if st.session_state.logged_in:

    st.sidebar.success(f"👤 {st.session_state.username}")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.username = ""
        st.session_state.page = "Login"

        st.rerun()

# =========================
# SIGN UP PAGE
# =========================
if st.session_state.page == "Sign Up" and not st.session_state.logged_in:

    st.markdown(
        '<p class="main-title">📝 Create Account</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Register as Student or Parent</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        role = st.selectbox(
            "Register As",
            ["Student", "Parent"]
        )

        username = st.text_input("Create Username")

    with col2:

        password = st.text_input(
            "Create Password",
            type="password"
        )

        confirm = st.text_input(
            "Confirm Password",
            type="password"
        )

    if st.button("✅ Create Account"):

        if password != confirm:
            st.error("Passwords do not match")

        elif username == "" or password == "":
            st.warning("Please fill all fields")

        else:

            if role == "Student":

                if username in users["students"]:
                    st.error("Username already exists")

                else:

                    users["students"][username] = password

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("Student Account Created")

            else:

                if username in users["parents"]:
                    st.error("Username already exists")

                else:

                    users["parents"][username] = password

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("Parent Account Created")

    # Back Button
    if st.button("⬅ Back to Login"):
        st.session_state.page = "Login"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# LOGIN PAGE
# =========================
elif st.session_state.page == "Login" and not st.session_state.logged_in:

    st.markdown(
        '<p class="main-title">🔐 Login Page</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Login to access the predictor</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

        role = st.selectbox(
            "Login As",
            ["Student", "Parent"]
        )

        username = st.text_input("Username")

    with col2:

        password = st.text_input(
            "Password",
            type="password"
        )

    if st.button("🚀 Login"):

        if role == "Student":

            if (
                username in users["students"]
                and users["students"][username] == password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role

                st.rerun()

            else:
                st.error("Invalid Username or Password")

        else:

            if (
                username in users["parents"]
                and users["parents"][username] == password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role

                st.rerun()

            else:
                st.error("Invalid Username or Password")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# MAIN APP
# =========================
elif st.session_state.logged_in:

    # Load Model
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")

    # Header
    st.markdown(
        '<p class="main-title">🎓 Student Score Predictor</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Predict student exam performance using AI</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Academic Section
    st.markdown(
        '<p class="section-title">📊 Academic Factors</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        hours = st.number_input(
            "⏰ Hours Studied",
            0.0, 24.0
        )

        previous = st.number_input(
            "⭐ Previous Score",
            0.0, 100.0
        )

    with col2:

        attendance = st.number_input(
            "📅 Attendance (%)",
            0.0, 100.0
        )

        sleep = st.number_input(
            "🌙 Sleep Hours",
            0.0, 12.0
        )

    # Personal Section
    st.markdown(
        '<p class="section-title">🧠 Personal & School Factors</p>',
        unsafe_allow_html=True
    )

    col3, col4 = st.columns(2)

    with col3:

        motivation = st.selectbox(
            "🏆 Motivation Level",
            ["Low", "Medium", "High"]
        )

        school = st.selectbox(
            "🏫 School Type",
            ["Public", "Private"]
        )

        income = st.selectbox(
            "💰 Family Income",
            ["Low", "Medium", "High"]
        )

        education = st.selectbox(
            "🎓 Parent Education",
            ["School", "College"]
        )

        resources = st.selectbox(
            "📚 Learning Resources",
            ["Low", "Medium", "High"]
        )

    with col4:

        teacher = st.selectbox(
            "👨‍🏫 Teacher Quality",
            ["Poor", "Average", "Good"]
        )

        internet = st.selectbox(
            "📶 Internet Access",
            ["Yes", "No"]
        )

        parent = st.selectbox(
            "👨‍👩‍👧 Parental Involvement",
            ["Low", "Medium", "High"]
        )

        peer = st.selectbox(
            "👥 Peer Influence",
            ["Negative", "Neutral", "Positive"]
        )

        activities = st.selectbox(
            "⚽ Extracurricular Activities",
            ["Yes", "No"]
        )

    # Predict
    if st.button("🚀 Predict Score"):

        data = {
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Previous_Scores": previous,
            "Sleep_Hours": sleep,

            "Motivation_Level": motivation,
            "Teacher_Quality": teacher,
            "School_Type": school,
            "Internet_Access": internet,
            "Family_Income": income,
            "Parental_Involvement": parent,
            "Parental_Education_Level": education,
            "Peer_Influence": peer,
            "Learning_Resources": resources,
            "Extracurricular_Activities": activities
        }

        input_df = pd.DataFrame([data])

        input_df = pd.get_dummies(input_df)

        input_df = input_df.reindex(
            columns=columns,
            fill_value=0
        )

        prediction = model.predict(input_df)

        final_score = max(
            40,
            min(100, prediction[0])
        )

        final_score = int(round(final_score))

        # SMALL RESULT BOX
        st.markdown(f"""
        <div class="result-box">
            <h2>🎯 Predicted Exam Score</h2>
            <div class="score-text">{final_score}</div>
            <p>Keep studying and improving 🚀</p>
        </div>
        """, unsafe_allow_html=True)

        # TIP
        st.markdown("""
        <div class="tip-box">
        💡 Tip: Regular study + good sleep + positive mindset = better performance.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
