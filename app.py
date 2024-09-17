import streamlit as st
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import io
import cv2  # OpenCV for bilateral filtering

# Convert PIL Image to OpenCV format
def pil_to_cv2(image):
    return np.array(image.convert('RGB'))

# Convert OpenCV format to PIL Image
def cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def pencil_sketch_bw(image, contrast_level, sharpness_level, sketch_style, refine_edges, smooth_lines):
    # Convert to grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Invert the grayscale image
    inverted_image = ImageOps.invert(gray_image)
    
    # Adjust blur radius based on the sketch style
    if sketch_style == "Detailed Sketch":
        blur_radius = 10
    elif sketch_style == "Soft Sketch":
        blur_radius = 30
    elif sketch_style == "Cartoon Sketch":
        blur_radius = 5
    else:
        blur_radius = 21
    
    # Blur the inverted image
    blurred_image = inverted_image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Invert the blurred image
    inverted_blurred = ImageOps.invert(blurred_image)
    
    # Create the pencil sketch
    sketch = Image.blend(gray_image, inverted_blurred, alpha=contrast_level)
    
    # Apply sharpening based on the sketch style
    if sketch_style == "Cartoon Sketch":
        sharpened_sketch = sketch.filter(ImageFilter.UnsharpMask(radius=3, percent=sharpness_level))
    else:
        sharpened_sketch = sketch.filter(ImageFilter.UnsharpMask(radius=2, percent=sharpness_level))
    
    # Refine edges if the option is selected
    if refine_edges:
        edge_image = gray_image.filter(ImageFilter.FIND_EDGES)
        edge_image = ImageEnhance.Contrast(edge_image).enhance(2.0)
        edge_image = ImageEnhance.Sharpness(edge_image).enhance(2.0)
        sketch = Image.blend(sharpened_sketch, edge_image, alpha=0.5)
    
    # Smooth lines if the option is selected
    if smooth_lines:
        # Convert to OpenCV format for advanced filtering
        sketch_cv2 = pil_to_cv2(sketch)
        
        # Apply Bilateral Filter for smoothing while keeping edges sharp
        smoothed_sketch_cv2 = cv2.bilateralFilter(sketch_cv2, d=9, sigmaColor=75, sigmaSpace=75)
        
        # Convert back to PIL format
        sketch = cv2_to_pil(smoothed_sketch_cv2)
    
    return sketch

def convert_image_to_bytes(image):
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

st.title("Image to Pencil Sketch using Python")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Load the input image
    image = Image.open(uploaded_file)
    
    # Convert the input image to grayscale (black and white)
    bw_image = ImageOps.grayscale(image)
    
    # Slider for contrast level for the pencil sketch
    contrast_level = st.slider("Contrast Level", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
    
    # Slider for sharpness level for the pencil sketch
    sharpness_level = st.slider("Sharpness Level", min_value=0, max_value=200, value=100, step=10)
    
    # Dropdown for selecting the sketch style
    sketch_style = st.selectbox("Choose a sketch style", ["Detailed Sketch", "Soft Sketch", "Cartoon Sketch"])
    
    # Checkbox for refining edges
    refine_edges = st.checkbox("Refine Edges", value=True)
    
    # Checkbox for smoothing lines
    smooth_lines = st.checkbox("Smooth Lines", value=True)
    
    # Generate the pencil sketch based on the selected style, edge refinement, and line smoothing
    sketch_bw = pencil_sketch_bw(image, contrast_level, sharpness_level, sketch_style, refine_edges, smooth_lines)
    
    # Display the original image
    st.image(image, caption='Original Image', use_column_width=True)
    
    # Display the black-and-white version of the input image
    st.image(bw_image, caption='Black-and-White Version', use_column_width=True)
    
    # Display the pencil sketch of the input image
    st.image(sketch_bw, caption=f'{sketch_style} with Contrast Level {contrast_level}, Sharpness Level {sharpness_level}, Edge Refinement, and Line Smoothing', use_column_width=True)
    
    # Add download button for pencil sketch
    st.download_button(
        label="Download Pencil Sketch",
        data=convert_image_to_bytes(sketch_bw),
        file_name=f"pencil_sketch_{sketch_style.lower().replace(' ', '_')}_smoothed.png",
        mime="image/png"
    )
