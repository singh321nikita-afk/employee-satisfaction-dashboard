import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Employee Satisfaction Analyzer",
    page_icon="😊",
    layout="wide"
)

# ---------------- CUSTOM BACKGROUND ----------------
st.markdown("""
<style>
.stApp {
    background-color: #E8F5E9;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
file_path = "employee_data.csv"

if os.path.exists(file_path):
    data = pd.read_csv(file_path)
else:
    data = None

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 HR Dashboard")

page = st.sidebar.radio(
    "Navigation",
    ["Home", "Dashboard", "Employee Data", "Recommendations"]
)

# ================= HOME =================
# ================= HOME =================
if page == "Home":

    st.title("😊 Employee Satisfaction Analytics Dashboard")

    st.markdown("---")

    st.markdown("""
### 👋 Welcome!

This dashboard helps HR professionals monitor employee satisfaction,
analyze workforce trends, and generate meaningful HR insights.

Using employee ratings and feedback, managers can identify strengths,
areas for improvement, and make better HR decisions.
""")

    st.markdown("---")

    c1, c2, c3 = st.columns(3)

    c1.info("👥 Employee Records\n\nTrack employee information and satisfaction ratings.")

    c2.success("📊 Analytics Dashboard\n\nView important HR metrics and visual insights.")

    c3.warning("💡 Smart Recommendations\n\nGenerate HR suggestions based on employee data.")

    st.markdown("---")

    st.subheader("🚀 Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.write("✅ Employee Satisfaction Analysis")
        st.write("✅ Department-wise Insights")
        st.write("✅ Dynamic Dashboard")
        st.write("✅ Employee Database")

    with col2:
        st.write("✅ HR Recommendations")
        st.write("✅ Interactive Pie Chart")
        st.write("✅ Real-time Statistics")
        st.write("✅ Easy-to-use Interface")

    st.markdown("---")

    st.success("🎯 Objective: Improve employee satisfaction using HR analytics and data visualization.")

    st.caption("Developed by Nikita Singh | MBA (HR)")

# ================= DASHBOARD =================
elif page == "Dashboard":

    st.title("📊 Dashboard")

    if data is None:

        st.error("employee_data.csv not found!")

    else:

        total = len(data)
        avg = round(data["Rating"].mean(), 2)

        positive = len(data[data["Rating"] >= 4])
        neutral = len(data[data["Rating"] == 3])
        negative = len(data[data["Rating"] <= 2])

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric("👥 Employees", total)
        c2.metric("⭐ Avg Rating", avg)
        c3.metric("😊 Positive", positive)
        c4.metric("😐 Neutral", neutral)
        c5.metric("😞 Negative", negative)

        st.divider()

        st.subheader("📊 Employee Satisfaction Distribution")

        labels = ["Positive", "Neutral", "Negative"]
        sizes = [positive, neutral, negative]

        fig, ax = plt.subplots(figsize=(5,5))

        ax.pie(
            sizes,
            labels=labels,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(fig)

# ================= EMPLOYEE DATA =================
elif page == "Employee Data":

    st.title("📋 Employee Dataset")

    if data is None:

        st.error("employee_data.csv not found!")

    else:

        st.dataframe(data, use_container_width=True)

# ================= RECOMMENDATIONS =================
elif page == "Recommendations":

    st.title("💡 HR Recommendations")

    if data is None:

        st.error("employee_data.csv not found!")

    else:

        avg = data["Rating"].mean()

        if avg >= 4:
            st.success("Employees are highly satisfied.")

        elif avg >= 3:
            st.info("Employee satisfaction is moderate.")

        else:
            st.error("Employee satisfaction is low.")

        st.subheader("General Suggestions")

        st.write("✅ Conduct employee engagement activities.")
        st.write("✅ Reward top-performing employees.")
        st.write("✅ Improve work-life balance.")
        st.write("✅ Collect employee feedback regularly.")