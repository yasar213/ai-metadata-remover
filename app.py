import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import json
import io

# 1. Page Configuration (Centered Layout like the image)
st.set_page_config(page_title="AI Metadata Cleaner", layout="centered", initial_sidebar_state="collapsed")

# 2. Custom CSS to mimic the uploaded image's UI
st.markdown("""
<style>
    /* Main background color - elegant beige */
    .stApp {
        background-color: #F8F7F2;
    }
    
    /* Hide default Streamlit header and footer for a clean look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Import elegant fonts (Serif for headings, Sans-serif for text) */
    @import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;600&display=swap');
    
    h1 {
        font-family: 'Lora', serif;
        color: #1A1A1A;
        text-align: center;
        font-size: 3.2rem !important;
        margin-bottom: 0px !important;
        padding-bottom: 10px !important;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #4A4A4A;
        font-size: 1.1rem;
        margin-top: 5px;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* The orange process button */
    .stDownloadButton>button {
        background-color: #E24A29;
        color: white;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border-radius: 6px;
        border: none;
        padding: 15px 30px;
        width: 100%;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    .stDownloadButton>button:hover {
        background-color: #C83D1F;
        color: white;
        box-shadow: 0px 4px 12px rgba(226, 74, 41, 0.3);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploadDropzone"] {
        background-color: #F4F2E9;
        border: 1px dashed #BDBDBD;
        border-radius: 8px;
        padding: 40px;
    }
    
    /* Top Navbar fake UI */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 0px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        border-bottom: 1px solid #EAE8DF;
        margin-bottom: 50px;
    }
    .nav-links span {
        margin: 0 15px;
        color: #555;
        cursor: pointer;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. Fake Navbar (Visual Only)
st.markdown("""
<div class="navbar">
    <div style="font-family: 'Lora', serif; font-size: 1.5rem; font-weight: bold; color: #E24A29;">
        A <span style="color: #333; font-style: italic;">AI Metadata Cleaner</span>
    </div>
    <div class="nav-links">
        <span>Blog</span>
        <span>Pricing</span>
        <span>Disclaimer</span>
        <span>Other Tools ⌄</span>
    </div>
    <div>
        <span style="margin-right: 20px; font-weight: bold; cursor: pointer; color: #333;">➔ Sign In</span>
        <button style="background-color: #E24A29; color: white; border: none; padding: 10px 24px; border-radius: 4px; font-weight: bold; cursor: pointer;">Register</button>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Header Section
st.markdown("<h1>Free Metadata Cleaner & AI Tag Remover</h1>", unsafe_allow_html=True)
st.markdown("""
<p class='subtitle'>
Online metadata cleaner and remover that strips EXIF, GPS, C2PA, and AI generation tags<br>
from your images, and removes Stable Diffusion parameters — to protect your privacy before<br>
you share, all in your browser.
</p>
""", unsafe_allow_html=True)

# 5. Main Content Area (Centered)
col1, col2, col3 = st.columns([1, 5, 1])

with col2:
    uploaded_file = st.file_uploader("Drop image here (.JPG, .PNG, .WEBP - UP TO 10MB)", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
    
    st.markdown("<p style='text-align: center; color: #E24A29; font-size: 0.85rem; margin-top: 10px; font-weight: bold;'>1/3 IMAGES TODAY <br> <span style='font-weight: normal; color: #777;'>2 REMAINING</span></p>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_format = image.format if image.format else "PNG"
        
        # Display the uploaded image thumbnail
        st.image(image, caption=uploaded_file.name, width=250)
        
        # Processing Logic (Cleaning metadata)
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))
        img_byte_arr = io.BytesIO()
        clean_image.save(img_byte_arr, format=img_format)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # The Orange Process Button
        st.download_button(
            label="⚡ Process & Download Image",
            data=img_byte_arr.getvalue(),
            file_name=f"cleaned_{uploaded_file.name}",
            mime=f"image/{img_format.lower()}"
        )
