import streamlit as st
import dropbox
from dropbox.exceptions import ApiError
import os
from datetime import datetime
import re

# Seite konfigurieren
st.set_page_config(
    page_title="Marcos 50. Geburtstag",
    page_icon="🎂",
    layout="centered"
)

# Extrem einfaches Design (Dribbble-Style)
st.markdown("""
    <style>
    /* Hintergrund & Container */
    .stApp {
        background-color: #ffffff;
    }
    .main .block-container {
        padding-top: 5rem;
        max-width: 500px;
    }
    
    /* Header Styling */
    h1 {
        text-align: center;
        color: #1a1a1a;
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        margin-bottom: 0.5rem !important;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 3rem;
    }

    /* Der moderne Upload-Kasten (Dribbble Style) */
    .stFileUploader section {
        background-color: #fafafa !important;
        border: 2px dashed #e0e0e0 !important;
        padding: 4rem 2rem !important;
        border-radius: 20px !important;
        transition: all 0.3s ease-in-out !important;
        cursor: pointer;
    }
    .stFileUploader section:hover {
        border-color: #ff4b4b !important;
        background-color: #fffafa !important;
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }

    /* 'Browse files' Button stylen */
    .stFileUploader section button {
        background-color: #1a1a1a !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        border: none !important;
        margin: 0 auto !important;
        display: block !important;
    }
    
    /* Englische Texte komplett weg */
    .stFileUploader section div div {
        display: none !important;
    }
    
    /* Icon-Ersatz (Simuliert das Upload-Icon) */
    .stFileUploader section::before {
        content: '📸';
        display: block;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* Alles von Streamlit verstecken */
    [data-testid="stAppToolbar"], [data-testid="stHeader"], [data-testid="stFooter"], 
    footer, header, #stDecoration {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Marcos 50.")
st.markdown('<p class="sub-header">Wähle Fotos oder Videos aus deiner Galerie</p>', unsafe_allow_html=True)

# Dropbox Logik (Bleibt gleich)
def upload_to_dropbox(file_obj, filename):
    token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not token:
        st.error("Konfigurationsfehler: Token fehlt.")
        return False
    
    try:
        dbx = dropbox.Dropbox(token)
        clean_name = re.sub(r'[^a-zA-Z0-9\._-]', '_', filename)
        timestamp = datetime.now().strftime("%H%M%S")
        date_folder = datetime.now().strftime("%Y-%m-%d")
        target_path = f"/Marcos_50_Uploads/{date_folder}/{timestamp}_{clean_name}"
        dbx.files_upload(file_obj.getvalue(), target_path, mode=dropbox.files.WriteMode.overwrite)
        return True
    except Exception:
        return False

# Session State
if 'hochgeladene_dateien' not in st.session_state:
    st.session_state.hochgeladene_dateien = set()

# Uploader
uploaded_files = st.file_uploader(
    "Upload", 
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], 
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Upload Prozess
if uploaded_files:
    neue_dateien = [f for f in uploaded_files if f.name not in st.session_state.hochgeladene_dateien]
    
    if neue_dateien:
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        erfolgreich = 0
        for i, datei in enumerate(neue_dateien):
            status_text.markdown(f"<p style='text-align:center'>Lade hoch: {datei.name}</p>", unsafe_allow_html=True)
            if upload_to_dropbox(datei, datei.name):
                erfolgreich += 1
                st.session_state.hochgeladene_dateien.add(datei.name)
            progress_bar.progress((i + 1) / len(neue_dateien))
        
        status_text.empty()
        progress_bar.empty()

        if erfolgreich > 0:
            st.balloons()
            st.success("✨ Deine Fotos sind sicher bei Marco angekommen!")
