import streamlit as st
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import io

def pencil_sketch_bw(image, contrast_level, sharpness_level):
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
    
    # Apply sharpening
    sharpened_sketch = sketch.filter(ImageFilter.UnsharpMask(radius=2, percent=sharpness_level))
    
    return sharpened_sketch

def pencil_sketch_color(image, contrast_level, sharpness_level):
    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Invert the grayscale image
    inverted_image = ImageOps.invert(gray_image)
    
    # Blur the inverted image
    blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(radius=21))
    
    # Invert the blurred image
    inverted_blurred = ImageOps.invert(blurred_image)
    
    # Create the color pencil sketch
    sketch = Image.blend(image, inverted_blurred.convert("RGB"), alpha=contrast_level)
    
    # Apply sharpening
    sharpened_sketch = sketch.filter(ImageFilter.UnsharpMask(radius=2, percent=sharpness_level))
    
    return sharpened_sketch

def adjust_line_thickness(image, thickness_level):
    # Adjust contrast to simulate line thickness
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(thickness_level)

def convert_image_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

st.title("Pencil Sketch Converter")

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

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    
    # Slider for contrast level
    contrast_level = st.slider("Contrast Level", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    
    # Slider for sharpness level
    sharpness_level = st.slider("Sharpness Level", min_value=0, max_value=200, value=100, step=10)
    
    # Slider for line thickness level
    thickness_level = st.slider("Line Thickness Level", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
    
    # Convert the image to pencil sketches
    sketch_bw = pencil_sketch_bw(image, contrast_level, sharpness_level)
    sketch_color = pencil_sketch_color(image, contrast_level, sharpness_level)
    
    # Adjust line thickness
    bw_with_thickness = adjust_line_thickness(sketch_bw, thickness_level)
    color_with_thickness = adjust_line_thickness(sketch_color, thickness_level)
    
    # Display the original and adjusted images
    st.image(image, caption='Original Image', use_column_width=True)
    st.image(bw_with_thickness, caption='Black-and-White Pencil Sketch with Contrast Level {:.1f}, Sharpness Level {}, and Line Thickness Level {:.1f}'.format(contrast_level, sharpness_level, thickness_level), use_column_width=True)
    st.image(color_with_thickness, caption='Color Pencil Sketch with Contrast Level {:.1f}, Sharpness Level {}, and Line Thickness Level {:.1f}'.format(contrast_level, sharpness_level, thickness_level), use_column_width=True)
    
    # Add download buttons for adjusted images
    st.download_button(
        label="Download Black-and-White Pencil Sketch",
        data=convert_image_to_bytes(bw_with_thickness),
        file_name="pencil_sketch_bw.png",
        mime="image/png"
    )
    
    st.download_button(
        label="Download Color Pencil Sketch",
        data=convert_image_to_bytes(color_with_thickness),
        file_name="pencil_sketch_color.png",
        mime="image/png"
    )
