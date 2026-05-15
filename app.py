import streamlit as st
import joblib
import pandas as pd
import json
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Student Score Predictor", page_icon="🎓")

# =========================
# USER FILE
# =========================
USER_FILE = "users.json"

# Create file if not exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({"students": {}, "parents": {}}, f)

# =========================
# LOAD USERS
# =========================
with open(USER_FILE, "r") as f:
    users = json.load(f)

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

# =========================
# SIGN UP PAGE
# =========================
if menu == "Sign Up" and not st.session_state.logged_in:

    st.title("📝 Sign Up")

    new_role = st.selectbox("Register As", ["Student", "Parent"])

    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Create Account"):

        if new_pass != confirm_pass:
            st.error("❌ Passwords do not match")

        elif new_user == "" or new_pass == "":
            st.warning("⚠ Please fill all fields")

        else:

            # Student Registration
            if new_role == "Student":

                if new_user in users["students"]:
                    st.error("❌ Username already exists")

                else:
                    users["students"][new_user] = new_pass

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("✅ Student Account Created Successfully")

            # Parent Registration
            else:

                if new_user in users["parents"]:
                    st.error("❌ Username already exists")

                else:
                    users["parents"][new_user] = new_pass

                    with open(USER_FILE, "w") as f:
                        json.dump(users, f)

                    st.success("✅ Parent Account Created Successfully")

# =========================
# LOGIN PAGE
# =========================
elif menu == "Login" and not st.session_state.logged_in:

    st.title("🔐 Login Page")

    role = st.selectbox("Login As", ["Student", "Parent"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        # Student Login
        if role == "Student":

            if (
                username in users["students"]
                and users["students"][username] == password
            ):

                st.session_state.logged_in = True
                st.session_state.role = "Student"
                st.session_state.username = username

                st.success("✅ Student Login Successful")
                st.rerun()

            else:
                st.error("❌ Invalid Username or Password")

        # Parent Login
        else:

            if (
                username in users["parents"]
                and users["parents"][username] == password
            ):

                st.session_state.logged_in = True
                st.session_state.role = "Parent"
                st.session_state.username = username

                st.success("✅ Parent Login Successful")
                st.rerun()

            else:
                st.error("❌ Invalid Username or Password")

# =========================
# MAIN APP
# =========================
elif st.session_state.logged_in:

    # Sidebar
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.sidebar.info(f"Role: {st.session_state.role}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.role = ""
        st.session_state.username = ""
        st.rerun()

    # =========================
    # LOAD MODEL
    # =========================
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")

    # =========================
    # TITLE
    # =========================
    st.title("🎓 Student Score Predictor")

    # =========================
    # INPUT FIELDS
    # =========================
    hours = st.number_input("Hours Studied", 0.0, 24.0)
    attendance = st.number_input("Attendance", 0.0, 100.0)
    previous = st.number_input("Previous Score", 0.0, 100.0)
    sleep = st.number_input("Sleep Hours", 0.0, 12.0)

    motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
    teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
    school = st.selectbox("School Type", ["Public", "Private"])
    internet = st.selectbox("Internet Access", ["Yes", "No"])
    income = st.selectbox("Family Income", ["Low", "Medium", "High"])
    parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
    education = st.selectbox("Parent Education", ["School", "College"])
    peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
    resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
    activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

    # =========================
    # PREDICT BUTTON
    # =========================
    if st.button("Predict Score"):

        # Create Dictionary
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

        # Convert to DataFrame
        input_df = pd.DataFrame([data])

        # Encoding
        input_df = pd.get_dummies(input_df)

        # Match Training Columns
        input_df = input_df.reindex(columns=columns, fill_value=0)

        # Prediction
        prediction = model.predict(input_df)

        # Fix Range
        final_score = max(40, min(100, prediction[0]))

        # Integer Output
        final_score = int(round(final_score))

        # Result
        st.success(f"🎯 Predicted Exam Score: {final_score}")
