import streamlit as st
import requests
from PIL import Image

st.title("🌱 Crop Disease Detector")
st.write("Upload a crop image for diagnosis")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)
    
    # Send to backend
    if st.button("Analyze"):
        try:
            response = requests.post(
                "http://localhost:5000/predict",
                files={"image": uploaded_file.getvalue()}
            )
            if response.status_code == 200:
                result = response.json()
                st.success(f"**Diagnosis**: {result['disease']}")
                st.info(f"**Recommendation**: {result['recommendation']}")
            else:
                st.error(f"Error: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"Failed to connect to the server. Is the backend running?")