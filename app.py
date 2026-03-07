import streamlit as st
import dropbox
from dropbox.exceptions import ApiError, AuthError
import os
from datetime import datetime
import re
import base64

# Seite konfigurieren
st.set_page_config(
    page_title="Marcos 50.",
    page_icon="🎂",
    layout="centered"
)

# Hilfsfunktion zum Laden von Bildern als Base64
def get_image_base64(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

# Assets laden (Pfade müssen stimmen)
bg_base64 = get_image_base64("assets/background.png")
camera_base64 = get_image_base64("assets/camera.png")
header_base64 = get_image_base64("assets/marcos50.png")

# Elegantes Festtags-Design
st.markdown(f"""
    <style>
    /* Hintergrund & Toolbar entfernen */
    .stApp {{ 
        background-color: #f4f1ea; 
    }}
    [data-testid="stAppToolbar"], [data-testid="stHeader"], [data-testid="stFooter"], 
    footer, header, #stDecoration {{ display: none !important; visibility: hidden !important; }}
    
    .main .block-container {{
        padding-top: 2rem;
        max-width: 450px;
        background-color: #ffffff;
        border-radius: 30px;
        margin-top: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        padding-bottom: 3rem;
    }}
    
    /* Header Bild */
    .header-container {{
        text-align: center;
        margin-bottom: 1rem;
    }}
    .header-img {{
        width: 80%;
        max-width: 300px;
    }}
    
    .sub-header {{
        text-align: center;
        color: #7a7a7a;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }}

    /* Der Upload-Bereich mit Bokeh-Hintergrund */
    .stFileUploader section {{
        background-image: url("data:image/png;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        border: 2px solid #e0d9c1 !important;
        padding: 3rem 1rem !important;
        border-radius: 25px !important;
        position: relative;
        overflow: hidden;
    }}
    
    /* Kamera Icon über dem Button */
    .stFileUploader section::before {{
        content: "";
        display: block;
        width: 120px;
        height: 120px;
        margin: 0 auto 1.5rem auto;
        background-image: url("data:image/png;base64,{camera_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}

    /* Goldener Button */
    .stFileUploader section button {{
        background: linear-gradient(180deg, #d4af37 0%, #b8860b 100%) !important;
        color: #1a1a1a !important;
        border-radius: 15px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none !important;
        margin: 0 auto !important;
        display: block !important;
        box-shadow: 0 4px 15px rgba(184, 134, 11, 0.3);
        text-transform: none !important;
    }}
    
    /* Browse files Text ersetzen (Workaround) */
    .stFileUploader section button span::after {{
        content: "Fotos & Videos hochladen";
        display: block;
        position: absolute;
        background: linear-gradient(180deg, #d4af37 0%, #b8860b 100%);
        top: 0; left: 0; right: 0; bottom: 0;
        padding: 0.8rem 2rem;
        border-radius: 15px;
        color: #1a1a1a;
    }}
    
    /* Englische Texte ausblenden */
    .stFileUploader section div div {{ display: none !important; }}
    
    /* Erfolg-Meldung Styling */
    .stSuccess {{
        background-color: #e8f5e9 !important;
        color: #2e7d32 !important;
        border: none !important;
        border-radius: 15px !important;
        text-align: center;
        font-weight: 500;
    }}
    </style>
    """, unsafe_allow_html=True)

# UI Layout
st.markdown(f'<div class="header-container"><img src="data:image/png;base64,{header_base64}" class="header-img"></div>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Wähle Fotos oder Videos aus deiner Galerie</p>', unsafe_allow_html=True)

# Dropbox Logik
def get_dropbox_client():
    refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
    app_key = os.getenv("DROPBOX_APP_KEY")
    app_secret = os.getenv("DROPBOX_APP_SECRET")
    if refresh_token and app_key and app_secret:
        return dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=app_key, app_secret=app_secret)
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if access_token:
        return dropbox.Dropbox(access_token)
    return None

def upload_to_dropbox(file_obj, filename):
    dbx = get_dropbox_client()
    if not dbx: return False
    try:
        clean_name = re.sub(r'[^a-zA-Z0-9\._-]', '_', filename)
        timestamp = datetime.now().strftime("%H%M%S")
        date_folder = datetime.now().strftime("%Y-%m-%d")
        target_path = f"/Marcos_50_Uploads/{date_folder}/{timestamp}_{clean_name}"
        dbx.files_upload(file_obj.getvalue(), target_path, mode=dropbox.files.WriteMode.overwrite)
        return True
    except:
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
        status_container = st.empty()
        progress_bar = st.progress(0)
        
        erfolgreich = 0
        for i, datei in enumerate(neue_dateien):
            status_container.markdown(f"<p style='text-align:center'>Lade hoch: <b>{datei.name}</b></p>", unsafe_allow_html=True)
            if upload_to_dropbox(datei, datei.name):
                erfolgreich += 1
                st.session_state.hochgeladene_dateien.add(datei.name)
            progress_bar.progress((i + 1) / len(neue_dateien))
        
        status_container.empty()
        progress_bar.empty()

        if erfolgreich > 0:
            st.balloons()
            st.success("✨ Deine Fotos sind sicher bei Marco angekommen!")
