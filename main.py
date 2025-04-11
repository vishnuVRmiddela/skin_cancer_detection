import streamlit as st
from PIL import Image
import numpy as np
from ultralytics import YOLO
import tempfile
import os

# Load your trained YOLOv8 model (update path as needed)
model = YOLO("best.pt")  # Replace with your trained model path

st.set_page_config(page_title="Skin Disease Detector", layout="centered")
st.title("🩺 Skin Disease Detection using YOLOv8")

st.markdown("Upload an image and the model will detect skin diseases.")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Save image to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        image_path = tmp_file.name
        image.save(image_path)

    # Run YOLO prediction
    results = model(image_path)

    # Get annotated image (with bounding boxes and labels)
    result_img = results[0].plot()

    # Display result
    st.subheader("🧠 Detection Result")
    st.image(result_img, caption="Predicted Image", use_column_width=True)

    # Optionally show detected classes and confidence
    st.subheader("📋 Detected Objects")
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        st.write(f"**{class_name}**: {confidence:.2%}")

    # Cleanup
    os.remove(image_path)
