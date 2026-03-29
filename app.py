import streamlit as st
import pandas as pd
import base64

# Function to set background image
st.markdown("""
<style>
.stTextInput label {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
        background: 
        linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)),
        url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Call the function
set_bg("rce1.jpg.png")
st.markdown("""
<h1 style='
margin-top: 120px;
text-align: center;
font-size: 50px;
font-weight: 900;
color: black;
text-shadow: 2px 2px 6px rgba(0,0,0,0.2);
'>
AI Powered Student Performance Analyzer
</h1>
""", unsafe_allow_html=True)

# Load Excel file
df = pd.read_excel("studentss.xlxs.xlsx")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

def analyze_student(attendance, marks):
    score = (attendance * 0.4) + (marks * 0.6)
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Poor"

def suggestion(attendance, marks):
    if attendance < 60 and marks < 60:
        return "High Risk - Improve attendance & study daily"
    elif attendance < 60:
        return "Improve attendance"
    elif marks < 60:
        return "Focus more on academics"
    else:
        return "Keep up the good work"

def failure_risk(attendance, marks):
    if attendance < 50 or marks < 40:
        return "Very High"
    elif attendance < 60 or marks < 50:
        return "High"
    elif attendance < 70 or marks < 60:
        return "Medium"
    else:
        return "Low"
def placement_chance(marks):
    if marks >= 85:
        return "High"
    elif marks >= 70:
        return "Moderate"
    elif marks >= 60:
        return "Low"
    else:
        return "Very Low"

# Apply AI logic
df["Performance"] = df.apply(
    lambda x: analyze_student(x["attendance"], x["marks"]), axis=1
)

df["Advice"] = df.apply(
    lambda x: suggestion(x["attendance"], x["marks"]), axis=1
)
df["Failure Risk"] = df.apply(
    lambda x: failure_risk(x["attendance"], x["marks"]), axis=1
)
df["Placement Chance"] = df["marks"].apply(placement_chance)

# 🔍 Search Section
st.markdown(
    "<h3 style='color: black;'>Search Student by Roll Number</h3>",
    unsafe_allow_html=True
)
roll_input = st.text_input("Enter Roll Number")

if roll_input:
    student = df[df["roll.no"].astype(str).str.upper() == roll_input.upper()]
    
    if not student.empty:
        st.success("Student Found ✅")
        st.dataframe(student)
        st.balloons()
    else:
        st.error("Roll Number Not Found ❌")
st.markdown("""
<style>
div[data-testid="stCheckbox"] label p {
    color: black !important;
}
</style>
""", unsafe_allow_html=True)
# Show full table option
if st.checkbox("Show Full Class Data"):
    st.dataframe(df)

# Class Summary
average_marks = round(df["marks"].mean(), 2)
risk_count = df[df["Advice"].str.contains("High Risk")].shape[0]

average_marks = round(df["marks"].mean(), 2)
risk_count = df[df["Advice"].str.contains("High Risk")].shape[0]

st.markdown("<h2 style='color:black; margin-bottom:20px;'>Class Summary</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
    <div style='
        background:#E8F6F3;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
    '>
        <h4 style='color:#1B4F72;'>Total Students</h4>
        <h1 style='color:black;'>{len(df)}</h1>
    </div>
""", unsafe_allow_html=True)

col2.markdown(f"""
    <div style='
        background:#EBF5FB;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
    '>
        <h4 style='color:#1B4F72;'>Average Marks</h4>
        <h1 style='color:black;'>{average_marks}</h1>
    </div>
""", unsafe_allow_html=True)

col3.markdown(f"""
    <div style='
        background:#FDEDEC;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow:0 4px 12px rgba(0,0,0,0.15);
    '>
        <h4 style='color:#922B21;'>High Risk</h4>
        <h1 style='color:black;'>{risk_count}</h1>
    </div>
""", unsafe_allow_html=True)