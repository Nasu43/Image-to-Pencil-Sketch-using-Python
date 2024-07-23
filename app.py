import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter

def pencil_sketch(image, contrast_level):
    # Convert to grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Invert the grayscale image
    inverted_image = ImageOps.invert(gray_image)
    
    # Blur the inverted image
    blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(radius=21))
    
    # Invert the blurred image
    inverted_blurred = ImageOps.invert(blurred_image)
    
    # Create the pencil sketch
    sketch = Image.blend(gray_image, inverted_blurred, alpha=contrast_level)
    
    return sketch

st.title("Image to Pencil Sketch Converter")

# Add background image (optional)
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
    
    # Slider for contrast level
    contrast_level = st.slider("Contrast Level", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    
    # Convert the image to pencil sketch with selected contrast level
    sketch = pencil_sketch(image, contrast_level)
    
    # Display the original and sketch images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(sketch, caption='Pencil Sketch with Contrast Level {:.1f}'.format(contrast_level), use_column_width=True)
