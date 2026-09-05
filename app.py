import streamlit as st
from PIL import Image
from PIL.ExifTags import TAGS
import json
import io

# App Layout Configuration
st.set_page_config(page_title="Advanced AI Image Reader & Remover", layout="wide")

st.title("🔬 Advanced AI Image Metadata Reader & Remover")
st.write("Image-a upload panni C2PA matrum hidden metadata-va check pannunga.")

# Image Uploader
uploaded_file = st.file_uploader("Upload Image (PNG, JPG, JPEG, WEBP)", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    # Get raw file bytes for deep scanning
    file_bytes = uploaded_file.getvalue()
    
    # Image-a open pannuvom
    image = Image.open(uploaded_file)
    img_format = image.format if image.format else "PNG"
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        # --- METADATA REMOVAL ---
        st.markdown("---")
        st.subheader("🧹 Remove Metadata")
        st.write("AI generated traces-a azhikka, pudhu image-a download pannunga.")
        
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(list(image.getdata()))
        
        img_byte_arr = io.BytesIO()
        clean_image.save(img_byte_arr, format=img_format)
        
        st.download_button(
            label="⬇️ Download Cleaned Image",
            data=img_byte_arr.getvalue(),
            file_name=f"cleaned_image.{img_format.lower()}",
            mime=f"image/{img_format.lower()}",
            type="primary"
        )
    
    with col2:
        st.subheader("Extracted Metadata")
        metadata = {}

        # 1. Basic Info & PNG Text Chunks
        if image.info:
            metadata['Basic_Info'] = {}
            for key, value in image.info.items():
                if key not in ['icc_profile', 'exif']: 
                    metadata['Basic_Info'][key] = str(value)

        # 2. EXIF Data extraction
        exif_data = image.getexif()
        if exif_data:
            metadata['EXIF_Data'] = {}
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata['EXIF_Data'][tag] = str(value)

        if metadata:
            st.json(metadata)
        else:
            st.write("No basic metadata found. Running Deep Scan...")

        # --- 3. ADVANCED DEEP BINARY SCAN (For ChatGPT, DALL-E, C2PA) ---
        st.markdown("### 🧬 Deep Binary Scan Results")
        
        ai_traces = []
        
        # Checking raw bytes for hidden AI signatures
        if b'c2pa' in file_bytes or b'jumbf' in file_bytes:
            ai_traces.append("C2PA Content Credentials (Used by ChatGPT/DALL-E 3/Adobe)")
            
        if b'DALL-E' in file_bytes or b'dall-e' in file_bytes.lower():
            ai_traces.append("DALL-E Signature")
            
        if b'Midjourney' in file_bytes or b'midjourney' in file_bytes.lower():
            ai_traces.append("Midjourney Signature")
            
        if b'ComfyUI' in file_bytes or b'comfyui' in file_bytes.lower():
            ai_traces.append("ComfyUI Signature")
            
        if b'prompt' in file_bytes.lower():
             ai_traces.append("Hidden Prompt Data")

        st.subheader("AI Detection Result")
        if ai_traces or metadata:
            # Check basic metadata as well
            metadata_str = json.dumps(metadata).lower()
            basic_keywords = ["prompt", "negative prompt", "steps:", "sampler:", "cfg scale", "midjourney", "stable diffusion", "comfyui", "dall-e", "c2pa"]
            found_keywords = [kw for kw in basic_keywords if kw in metadata_str]
            
            if ai_traces or found_keywords:
                st.error("⚠️ **AI Traces Found!**")
                if found_keywords:
                    st.write(f"**Keywords found in Metadata:** {', '.join(found_keywords).title()}")
                if ai_traces:
                    st.write(f"**Hidden Signatures found via Deep Scan:** {', '.join(ai_traces)}")
                st.write("Idhu kanchippaaga oru AI tool aala generate pannappatta image aagum.")
            else:
                st.success("✅ No clear AI footprints found even after Deep Scan.")
        else:
            st.success("✅ No clear AI footprints found even after Deep Scan.")