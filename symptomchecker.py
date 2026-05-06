import streamlit as st

# Sidebar Section for Symptom Checker
st.sidebar.title("🔍 Check Your Symptoms")
st.sidebar.write("Answer a few quick questions to assess your risk before uploading an X-ray or CT scan.")

# Define symptoms with checkboxes
symptoms = {
    "Persistent Cough (lasting more than 3 weeks)": st.sidebar.checkbox("Persistent Cough"),
    "Chest Pain (especially when breathing deeply or coughing)": st.sidebar.checkbox("Chest Pain"),
    "Shortness of Breath": st.sidebar.checkbox("Shortness of Breath"),
    "Unexplained Weight Loss": st.sidebar.checkbox("Unexplained Weight Loss"),
    "Fatigue (feeling unusually tired all the time)": st.sidebar.checkbox("Fatigue"),
    "Hoarseness or Voice Changes": st.sidebar.checkbox("Hoarseness or Voice Changes"),
    "Coughing up Blood (even small amounts)": st.sidebar.checkbox("Coughing up Blood"),
    "Frequent Lung Infections (pneumonia, bronchitis)": st.sidebar.checkbox("Frequent Lung Infections"),
    "Loss of Appetite": st.sidebar.checkbox("Loss of Appetite"),
    "Swelling in Neck or Face": st.sidebar.checkbox("Swelling in Neck or Face"),
}

# Calculate the total risk score based on selected symptoms
risk_score = sum(symptoms.values())

# Display Risk Assessment Results
st.sidebar.subheader("🩺 Risk Assessment Results")

if risk_score >= 3:
    st.sidebar.error("⚠ *High Risk*: Your symptoms indicate a potential risk for lung conditions. It is strongly recommended to upload a medical scan for analysis and consult a doctor.")
elif risk_score > 0:
    st.sidebar.warning("⚠ *Moderate Risk*: You have some symptoms associated with lung conditions. If symptoms persist, consult a doctor for further evaluation.")
else:
    st.sidebar.success("✅ *Low Risk*: No major symptoms detected. Maintain a healthy lifestyle and monitor any future symptoms.")

# Additional Recommendations
st.sidebar.subheader("📌 Recommendations")
if risk_score >= 3:
    st.sidebar.info("🔹 Consider uploading an X-ray or CT scan for further analysis.\n🔹 Schedule a medical consultation as soon as possible.\n🔹 Avoid smoking or exposure to air pollution.\n🔹 Stay hydrated and monitor your symptoms closely.")
elif risk_score > 0:
    st.sidebar.info("🔹 Maintain a healthy diet and lifestyle.\n🔹 Monitor your symptoms for any changes.\n🔹 If symptoms persist for more than 2 weeks, consult a healthcare professional.")
else:
    st.sidebar.info("🔹 Keep up with regular health check-ups.\n🔹 Avoid smoking and stay in well-ventilated areas.\n🔹 Practice deep breathing exercises for lung health.")