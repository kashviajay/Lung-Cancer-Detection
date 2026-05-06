import streamlit as st
import tensorflow as tf
import gdown
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# Path of your model file (local path)
model_path = r"C:\frontend\best_model.keras"

# Check if the model file exists locally, if not, download it
if not os.path.exists(model_path):
    # URL of your Google Drive file (replace with your actual file ID)
    drive_url = 'https://drive.google.com/uc?export=download&id=1k9wsALn_pJiw42XdAKnPfe9VFpCbxo-E'
    # Download the model from Google Drive
    gdown.download(drive_url, model_path, quiet=False)

# Load the model
model = tf.keras.models.load_model(model_path)

# Set up the Streamlit UI with an aesthetic theme
st.set_page_config(page_title="Lung Cancer Detection", page_icon=":guardsman:", layout="wide")
st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #a8c0ff, #3faffa);
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #003366;
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            margin-top: 50px;
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
        }
        .button {
            background-color: #1e90ff;
            color: white;
            padding: 15px 32px;
            font-size: 18px;
            border-radius: 8px;
            margin-top: 20px;
            width: 50%;
            margin-left: 25%;
        }
        .button:hover {
            background-color: #4682b4;
        }
        .info {
            font-size: 18px;
            color: #2a2a2a;
            text-align: center;
            margin-top: 20px;
            font-weight: bold;
            padding: 10px;
        }
        .result {
            text-align: center;
            font-size: 24px;
            margin-top: 30px;
        }
        .cancer-detected {
            color: red;
            font-weight: bold;
            font-size: 28px;
            text-shadow: 2px 2px 4px rgba(255, 0, 0, 0.6);
        }
        .no-cancer {
            color: green;
            font-weight: bold;
            font-size: 28px;
            text-shadow: 2px 2px 4px rgba(0, 255, 0, 0.6);
        }
        .footer {
            visibility: hidden;
        }
        .file-uploader {
            display: flex;
            justify-content: center;
        }
        .file-uploader input[type="file"] {
            background-color: #4caf50;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
            color: white;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="title">Lung Cancer Detection Using AI :lungs:</h1>', unsafe_allow_html=True)
st.write("Upload a lung X-ray image to predict if cancer is detected and identify the stage of cancer.")

# Add some helpful information about the prediction
st.markdown("""
    <div class="info">
        <p>This app uses AI to detect whether lung cancer is present based on X-ray images. The model predicts the stage of cancer, from Stage 1 (early stages) to Stage 4 (advanced stages).</p>
    </div>
""", unsafe_allow_html=True)

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Prediction button
if uploaded_file is not None:
    st.write("**Image ready for prediction. Click 'Predict' to analyze the X-ray.**")
    st.write("")

    predict_button = st.button("Predict", key="predict_button")

    if predict_button:
        # Preprocess the image for prediction
        img = image.load_img(uploaded_file, target_size=(350, 350))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array /= 255.0  # Rescale pixel values

        # Make prediction
        prediction = model.predict(img_array)
        class_names = ["Stage 1", "Stage 2", "Stage 3", "Stage 4"]  # Replace with your actual class names
        predicted_class = class_names[np.argmax(prediction)]

        # Display the result in a more aesthetic format
        st.write(f"**Prediction**: {predicted_class}")
        
        # Output for cancer detection
        if predicted_class in ["Stage 3", "Stage 4"]:  # Assuming Stage 3 and 4 represent cancer detected
            st.markdown("<h3 class='result cancer-detected'>Cancer Detected</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 class='result no-cancer'>No Cancer Detected</h3>", unsafe_allow_html=True)

# Footer (hiding Streamlit's default footer)
st.markdown("""
    <style>
        footer {
            visibility: hidden;
        }
    </style>
""", unsafe_allow_html=True)
