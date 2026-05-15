import streamlit as st
import pandas as pd
import joblib
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime

# PDF
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
from reportlab.lib.pagesizes import letter

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Student Score Predictor",
    page_icon="🎓",
    layout="wide"
)

# =========================
# THEME SESSION
# =========================
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# =========================
# THEME COLORS
# =========================
if st.session_state.theme == "Light":

    bg_color = "#f5f7ff"
    card_color = "white"
    text_color = "#111827"
    subtitle_color = "#6b7280"

else:

    bg_color = "#0f172a"
    card_color = "#1e293b"
    text_color = "white"
    subtitle_color = "#cbd5e1"

# =========================
# CUSTOM CSS
# =========================
st.markdown(f"""
<style>

.stApp {{
    background: {bg_color};
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #141e61, #0f044c);
    color: white;
}}

/* Main Title */
.main-title {{
    font-size: 70px;
    font-weight: 800;
    color: {text_color};
    margin-bottom: 10px;
}}

/* Subtitle */
.subtitle {{
    font-size: 20px;
    color: {subtitle_color};
    margin-bottom: 20px;
}}

/* Card */
.card {{
    background-color: {card_color};
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}}

/* Section Heading */
.section-title {{
    font-size: 24px;
    font-weight: bold;
    color: #7c3aed;
    margin-bottom: 15px;
}}

/* Button */
div.stButton > button {{
    width: 100%;
    background: linear-gradient(to right, #7c3aed, #2563eb);
    color: white;
    border: none;
    padding: 12px;
    border-radius: 12px;
    font-size: 18px;
    font-weight: bold;
}}

/* Result Box */
.result-box {{
    background-color: #ecfdf5;
    padding: 15px;
    border-radius: 12px;
    border-left: 6px solid #22c55e;
    margin-top: 20px;
}}

/* Score */
.score-text {{
    font-size: 34px;
    font-weight: bold;
    color: #16a34a;
}}

/* Tip Box */
.tip-box {{
    background-color: #eff6ff;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
    color: #2563eb;
    font-size: 15px;
}}

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

# Theme Selector
theme_option = st.sidebar.selectbox(
    "🎨 Select Theme",
    ["Light", "Dark"]
)

st.session_state.theme = theme_option

# Navigation
if not st.session_state.logged_in:

    if st.sidebar.button("🔐 Login"):
        st.session_state.page = "Login"

    if st.sidebar.button("📝 Sign Up"):
        st.session_state.page = "Sign Up"

# =========================
# USER PROFILE
# =========================
if st.session_state.logged_in:

    role = st.session_state.role
    username = st.session_state.username

    if role == "Student":
        user_data = users["students"][username]
    else:
        user_data = users["parents"][username]

    st.sidebar.markdown("---")
    st.sidebar.markdown("## 👤 User Profile")

    # Gender Based Image
    if user_data["gender"] == "Male":

        profile_pic = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

    else:

        profile_pic = "https://cdn-icons-png.flaticon.com/512/6997/6997662.png"

    st.sidebar.image(profile_pic, width=100)

    st.sidebar.write(f"### {user_data['name']}")
    st.sidebar.write(f"**Role:** {role}")
    st.sidebar.write(f"**Age:** {user_data['age']}")
    st.sidebar.write(f"**DOB:** {user_data['dob']}")

    if role == "Student":
        st.sidebar.write(f"**Class:** {user_data['class']}")

    else:
        st.sidebar.write(f"**Relation:** {user_data['relation']}")

    st.sidebar.markdown("---")

    # Logout
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

    role = st.selectbox(
        "Register As",
        ["Student", "Parent"]
    )

    col1, col2 = st.columns(2)

    with col1:

        full_name = st.text_input("👤 Full Name")

        username = st.text_input("🆔 Create Username")

        gender = st.selectbox(
            "⚧ Gender",
            ["Male", "Female"]
        )

        dob = st.date_input("📅 Date of Birth")

        age = st.number_input(
            "🎂 Age",
            min_value=1,
            max_value=100,
            step=1
        )

    with col2:

        password = st.text_input(
            "🔒 Create Password",
            type="password"
        )

        confirm = st.text_input(
            "🔑 Confirm Password",
            type="password"
        )

        # Student Class
        if role == "Student":

            student_class = st.selectbox(
                "🏫 Class",
                [
                    "1", "2", "3", "4", "5", "6",
                    "7", "8", "9", "10", "11", "12"
                ]
            )

        # Parent Relation
        else:

            relation = st.selectbox(
                "👨‍👩‍👧 Relation with Student",
                [
                    "Father",
                    "Mother",
                    "Guardian",
                    "Brother",
                    "Sister",
                    "Other"
                ]
            )

    # CREATE ACCOUNT
    if st.button("✅ Create Account"):

        if password != confirm:
            st.error("Passwords do not match")

        elif username == "" or password == "" or full_name == "":
            st.warning("Please fill all fields")

        else:

            # STUDENT ACCOUNT
            if role == "Student":

                if username in users["students"]:
                    st.error("Username already exists")

                else:

                    users["students"][username] = {
                        "name": full_name,
                        "gender": gender,
                        "password": password,
                        "dob": str(dob),
                        "age": age,
                        "class": student_class
                    }

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("🎉 Student Account Created Successfully")

            # PARENT ACCOUNT
            else:

                if username in users["parents"]:
                    st.error("Username already exists")

                else:

                    users["parents"][username] = {
                        "name": full_name,
                        "gender": gender,
                        "password": password,
                        "dob": str(dob),
                        "age": age,
                        "relation": relation
                    }

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("🎉 Parent Account Created Successfully")

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

        # Student Login
        if role == "Student":

            if (
                username in users["students"]
                and users["students"][username]["password"] == password
            ):

                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role

                st.rerun()

            else:
                st.error("Invalid Username or Password")

        # Parent Login
        else:

            if (
                username in users["parents"]
                and users["parents"][username]["password"] == password
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

    # LOAD MODEL
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")

    # HEADER
    st.markdown(
        '<p class="main-title">🎓 Student Score Predictor</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Predict student exam performance using AI</p>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)

    # Academic Factors
    st.markdown(
        '<p class="section-title">📊 Academic Factors</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        hours = st.number_input("⏰ Hours Studied", 0.0, 24.0)
        previous = st.number_input("⭐ Previous Score", 0.0, 100.0)

    with col2:
        attendance = st.number_input("📅 Attendance (%)", 0.0, 100.0)
        sleep = st.number_input("🌙 Sleep Hours", 0.0, 12.0)

    # Personal Factors
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

    # Predict Button
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

        # Result
        st.markdown(f"""
        <div class="result-box">
            <h2>🎯 Predicted Exam Score</h2>
            <div class="score-text">{final_score}</div>
            <p>Keep studying and improving 🚀</p>
        </div>
        """, unsafe_allow_html=True)

        # GRAPH
        st.subheader("📊 Score Visualization")

        subjects = [
            "Study",
            "Attendance",
            "Previous",
            "Predicted"
        ]

        values = [
            hours * 4,
            attendance,
            previous,
            final_score
        ]

        fig, ax = plt.subplots(figsize=(7,4))

        ax.bar(subjects, values)

        ax.set_ylim(0, 100)

        ax.set_ylabel("Score")

        ax.set_title("Student Performance Overview")

        st.pyplot(fig)

        # REPORT CARD
        st.subheader("📄 Student Report Card")

        grade = ""

        if final_score >= 90:
            grade = "A+"

        elif final_score >= 80:
            grade = "A"

        elif final_score >= 70:
            grade = "B"

        elif final_score >= 60:
            grade = "C"

        else:
            grade = "D"

        role = st.session_state.role
        username = st.session_state.username

        user_data = users["students"][username]

        report_data = {
            "Name": user_data["name"],
            "Class": user_data["class"],
            "Age": user_data["age"],
            "Hours Studied": hours,
            "Attendance": attendance,
            "Previous Score": previous,
            "Predicted Score": final_score,
            "Grade": grade,
            "Generated On": datetime.now().strftime("%d-%m-%Y")
        }

        report_df = pd.DataFrame(
            report_data.items(),
            columns=["Field", "Value"]
        )

        st.table(report_df)

        # =========================
        # PDF REPORT
        # =========================
        pdf_file = "student_report_card.pdf"

        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=letter
        )

        styles = getSampleStyleSheet()

        elements = []

        title = Paragraph(
            "Student Report Card",
            styles['Title']
        )

        elements.append(title)

        elements.append(Spacer(1, 12))

        table_data = [
            ["Field", "Value"]
        ]

        for key, value in report_data.items():
            table_data.append([key, str(value)])

        table = Table(
            table_data,
            colWidths=[200, 250]
        )

        table.setStyle(TableStyle([

            ('BACKGROUND', (0,0), (-1,0), colors.purple),

            ('TEXTCOLOR', (0,0), (-1,0), colors.white),

            ('GRID', (0,0), (-1,-1), 1, colors.black),

            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

            ('BOTTOMPADDING', (0,0), (-1,0), 10),

            ('BACKGROUND', (0,1), (-1,-1), colors.beige),

        ]))

        elements.append(table)

        doc.build(elements)

        # Download Button
        with open(pdf_file, "rb") as file:

            st.download_button(
                label="⬇ Download PDF Report Card",
                data=file,
                file_name="student_report_card.pdf",
                mime="application/pdf"
            )

        # TIP
        st.markdown("""
        <div class="tip-box">
        💡 Tip: Regular study + good sleep + positive mindset = better performance.
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
