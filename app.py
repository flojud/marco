import streamlit as st
import dropbox
from dropbox.exceptions import ApiError
import os
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Marcos 50. Geburtstag",
    page_icon="🎂",
    layout="centered"
)

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        height: 4em;
        font-size: 1.2rem;
        background-color: #ff4b4b;
        color: white;
        border-radius: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff3333;
        border: none;
        color: white;
    }
    h1 {
        text-align: center;
        color: #1f1f1f;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🎂 Marcos 50. Geburtstag")
st.markdown("<h4 style='text-align: center;'>Lade hier deine Fotos & Videos für Marco hoch!</h4>", unsafe_allow_html=True)

# Dropbox Logic
def upload_to_dropbox(file_obj, filename):
    token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not token:
        st.error("Konfigurationsfehler: DROPBOX_ACCESS_TOKEN fehlt.")
        return False
    
    try:
        dbx = dropbox.Dropbox(token)
        # Clean filename: keep alphanumeric, dots, underscores, dashes
        clean_name = re.sub(r'[^a-zA-Z0-9\._-]', '_', filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_path = f"/Marcos_50_Uploads/{timestamp}_{clean_name}"
        
        # Stream upload for larger files
        dbx.files_upload(file_obj.getvalue(), target_path, mode=dropbox.files.WriteMode.overwrite)
        return True
    except ApiError as e:
        st.error(f"Dropbox Fehler: {e}")
        return False
    except Exception as e:
        st.error(f"Fehler: {e}")
        return False

# UI Components
uploaded_files = st.file_uploader(
    "Wähle Bilder oder Videos aus", 
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    if st.button("🚀 Jetzt für Marco hochladen"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        success_count = 0
        total_files = len(uploaded_files)
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Lade '{uploaded_file.name}' hoch...")
            if upload_to_dropbox(uploaded_file, uploaded_file.name):
                success_count += 1
            
            # Update progress
            progress_bar.progress((i + 1) / total_files)
        
        if success_count == total_files:
            st.balloons()
            st.success("✨ Danke! Dein Beitrag ist sicher bei Marco angekommen.")
        elif success_count > 0:
            st.warning(f"Einige Dateien ({success_count}/{total_files}) wurden hochgeladen.")
        else:
            st.error("Upload fehlgeschlagen.")
else:
    st.info("💡 Tipp: Du kannst mehrere Dateien gleichzeitig aus deiner Galerie auswählen.")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Viel Spaß beim Feiern! 🥳</p>", unsafe_allow_html=True)
