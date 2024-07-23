import streamlit as st
import cv2
import numpy as np
from PIL import Image

def pencil_sketch(image, contrast_level):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Invert the grayscale image
    inverted_image = 255 - gray_image
    
    # Blur the inverted image
    blurred_image = cv2.GaussianBlur(inverted_image, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blurred = 255 - blurred_image
    
    # Create the pencil sketch
    sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)
    
    # Adjust contrast
    sketch = cv2.convertScaleAbs(sketch, alpha=contrast_level, beta=0)
    
    return sketch

st.title("Image to Pencil Sketch Converter")

# Add background image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://example.com/background.jpg");
        background-size: cover;
        background-position: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    image = np.array(image)
    
    # Slider for contrast level
    contrast_level = st.slider("Contrast Level", min_value=0.1, max_value=3.0, value=1.0, step=0.1)
    
    # Convert the image to pencil sketch with selected contrast level
    sketch = pencil_sketch(image, contrast_level)
    
    # Display the original and sketch images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(sketch, caption='Pencil Sketch with Contrast Level {:.1f}'.format(contrast_level), use_column_width=True)
