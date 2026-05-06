import streamlit as st
import tensorflow as tf
import gdown
import numpy as np
import os
from tensorflow.keras.applications.xception import preprocess_input
from PIL import Image

# Set Streamlit Page Config
st.set_page_config(page_title="Lung Cancer Detection", layout="wide")

# Apply Custom CSS for Enhanced UI & Dark Mode Support
st.markdown(
    """
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
        .main {
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
        .sidebar .block-container {
            padding: 20px;
            border-radius: 10px;
        }
        .stButton > button {
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
            box-shadow: 2px 2px 10px rgba(0, 85, 170, 0.3);
        }
        .stButton > button:hover {
            transform: scale(1.05);
        }
        .risk-box {
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page Title
st.markdown("""<h1 style='text-align: center; color: #0055aa;'>Lung Cancer Detection System</h1>""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>AI-powered preliminary lung cancer detection using deep learning.</p>", unsafe_allow_html=True)

# Sidebar Section for Symptom Checker
st.sidebar.title("Symptom Checker")
st.sidebar.write("Select the symptoms you are experiencing:")

symptoms = {
    "Persistent Cough": st.sidebar.checkbox("Persistent Cough"),
    "Chest Pain": st.sidebar.checkbox("Chest Pain"),
    "Shortness of Breath": st.sidebar.checkbox("Shortness of Breath"),
    "Unexplained Weight Loss": st.sidebar.checkbox("Unexplained Weight Loss"),
    "Fatigue": st.sidebar.checkbox("Fatigue"),
    "Hoarseness": st.sidebar.checkbox("Hoarseness"),
    "Coughing up Blood": st.sidebar.checkbox("Coughing up Blood"),
    "Frequent Lung Infections": st.sidebar.checkbox("Frequent Lung Infections"),
    "Loss of Appetite": st.sidebar.checkbox("Loss of Appetite"),
    "Swelling in Neck or Face": st.sidebar.checkbox("Swelling in Neck or Face"),
}

# Risk Assessment Logic
risk_score = sum(symptoms.values())
st.sidebar.subheader("Risk Assessment")

if risk_score >= 3:
    st.sidebar.markdown("<div class='risk-box' style='background-color: #f8d7da; color: #721c24;'>High Risk: Consult a doctor immediately.</div>", unsafe_allow_html=True)
    st.sidebar.write("### Precautions:")
    st.sidebar.write("- Schedule a medical check-up immediately.")
    st.sidebar.write("- Avoid smoking and exposure to pollutants.")
    st.sidebar.write("- Maintain a healthy lifestyle and regular monitoring.")
elif risk_score > 0:
    st.sidebar.markdown("<div class='risk-box' style='background-color: #fff3cd; color: #856404;'>Moderate Risk: Monitor symptoms.</div>", unsafe_allow_html=True)
    st.sidebar.write("### Precautions:")
    st.sidebar.write("- Keep track of symptoms.")
    st.sidebar.write("- Follow a healthy diet and exercise.")
    st.sidebar.write("- Seek medical advice if symptoms persist.")
else:
    st.sidebar.markdown("<div class='risk-box' style='background-color: #d4edda; color: #155724;'>Low Risk: No major symptoms detected.</div>", unsafe_allow_html=True)
    st.sidebar.write("### Precautions:")
    st.sidebar.write("- Maintain a healthy lifestyle.")
    st.sidebar.write("- Avoid smoking and exposure to toxins.")
    st.sidebar.write("- Get regular medical check-ups.")

# Model Path Handling
model_path = "Xception_lung_cancer_model.keras"
drive_url = "https://drive.google.com/uc?export=download&id=1-0UaMC7zi7GMvBk2ZyPX2aW-nPjXYVAC"

if not os.path.exists(model_path):
    st.warning("Model not found locally. Downloading from Google Drive...")
    try:
        gdown.cached_download(drive_url, model_path, quiet=False)
    except Exception as e:
        st.error(f"Failed to download model: {str(e)}")
        st.stop()

# Load Model
try:
    model = tf.keras.models.load_model(model_path)
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    model = None

# File Uploader for X-ray Image
st.subheader("Upload Chest X-ray for Analysis")
st.markdown("<p style='text-align: center;'>Drag & Drop your X-ray/CT Scan image (JPG, JPEG, PNG)</p>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and model:
    try:
        img = Image.open(uploaded_file).convert("RGB")
        img = img.resize((350, 350))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        st.image(img, caption="Uploaded successfully", width=350)

        if st.button("Predict Cancer Stage"):
            with st.spinner("Analyzing X-ray... Please wait."):
                prediction = model.predict(img_array)
                class_names = ["No Cancer", "Stage 1", "Stage 2", "Stage 3", "Stage 4"]
                predicted_class = class_names[np.argmax(prediction)]
                
                st.markdown(f"<div class='risk-box' style='background-color: #e3f2fd; color: #0055aa;'>{predicted_class}</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
