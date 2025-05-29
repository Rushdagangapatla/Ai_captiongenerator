import streamlit as st
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load BLIP model from Hugging Face
@st.cache_resource
def load_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

st.title("🖼️ AI-Based Image Caption Generator")
st.write("Upload an image and let the AI describe it for you!")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Generating caption...")
    processor, model = load_model()

    # Preprocess the image
    inputs = processor(image, return_tensors="pt")

    # Generate caption
    with torch.no_grad():
        output = model.generate(**inputs, max_new_tokens=20)

    caption = processor.decode(output[0], skip_special_tokens=True)
    st.success(f"📝 Caption: **{caption}**")
