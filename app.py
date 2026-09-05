import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import json
import io

# 1. Page Configuration
st.set_page_config(page_title="AI Image Scanner", page_icon="🧿", layout="wide")

# 2. Custom CSS for Modern UI
st.markdown("""
    <style>
    /* Background and general text */
    .stApp {
        background-color: #f4f6f9;
    }
    h1 {
        color: #1E3A8A;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 800;
    }
    .subtitle {
        text-align: center;
        color: #64748B;
        font-size: 18px;
        margin-bottom: 30px;
    }
    /* Stylish Upload Box */
    .stFileUploader {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.05);
    }
    /* Modern Buttons */
    .stDownloadButton>button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    .stDownloadButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.3);
        color: white;
    }
    /* Cards for Results */
    div[data-testid="stExpander"] {
        background-color: white;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.02);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("<h1>🧿 AI Image Metadata Scanner</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Detect hidden AI footprints & strip metadata instantly for 100% clean images.</div>", unsafe_allow_html=True)

st.markdown("---")

# 4. App Logic
uploaded_file = st.file_uploader("Drop your image here (PNG, JPG, JPEG, WEBP)", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    image = Image.open(uploaded_file)
    img_format = image.format if image.format else "PNG"
    
    col1, padding, col2 = st.columns([1.2, 0.1, 1])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Tip:** Download the cleaned image below to remove all traces of AI generation and camera data.")
        
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))
        img_byte_arr = io.BytesIO()
        clean_image.save(img_byte_arr, format=img_format)
        
        st.download_button(
            label="⬇️ Download Cleaned Image",
            data=img_byte_arr.getvalue(),
            file_name=f"cleaned_image.{img_format.lower()}",
            mime=f"image/{img_format.lower()}"
        )
    
    with col2:
        st.subheader("📊 Scan Results")
        metadata = {}

        if image.info:
            metadata['Basic_Info'] = {}
            for key, value in image.info.items():
                if key not in ['icc_profile', 'exif']: 
                    metadata['Basic_Info'][key] = str(value)

        exif_data = image.getexif()
        if exif_data:
            metadata['EXIF_Data'] = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata['EXIF_Data'][tag] = str(value)

        ai_traces = []
        if b'c2pa' in file_bytes or b'jumbf' in file_bytes:
            ai_traces.append("C2PA Content Credentials")
        if b'DALL-E' in file_bytes or b'dall-e' in file_bytes.lower():
            ai_traces.append("DALL-E Signature")
        if b'Midjourney' in file_bytes or b'midjourney' in file_bytes.lower():
            ai_traces.append("Midjourney Signature")
        if b'ComfyUI' in file_bytes or b'comfyui' in file_bytes.lower():
            ai_traces.append("ComfyUI Signature")
        if b'prompt' in file_bytes.lower():
             ai_traces.append("Hidden Prompt Data")

        metadata_str = json.dumps(metadata).lower()
        basic_keywords = ["prompt", "negative prompt", "steps:", "sampler:", "cfg scale", "midjourney", "stable diffusion", "comfyui", "dall-e", "c2pa"]
        found_keywords = [kw for kw in basic_keywords if kw in metadata_str]

        # Display Alert Boxes based on results
        if ai_traces or found_keywords:
            st.error("⚠️ **AI Traces Detected!**")
            if found_keywords:
                st.write(f"**Keywords:** {', '.join(found_keywords).title()}")
            if ai_traces:
                st.write(f"**Deep Scan Signatures:** {', '.join(ai_traces)}")
        else:
            st.success("✅ **100% Clean!** No AI footprints or hidden metadata found.")

        # Expandable Data View for clean UI
        with st.expander("🔍 View Raw Metadata"):
            if metadata:
                st.json(metadata)
            else:
                st.write("No raw metadata available.")
