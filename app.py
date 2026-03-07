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

# Assets laden
bg_base64 = get_image_base64("assets/background.png")
camera_base64 = get_image_base64("assets/camera.png")
header_base64 = get_image_base64("assets/marcos50.png")

# Finales Design laut Screenshot & Feedback
st.markdown(f"""
    <style>
    /* Das 6rem Padding von Streamlit hart überschreiben */
    .stAppViewContainer {{
        padding-top: 0 !important;
    }}
    .stMainBlockContainer {{
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
    }}
    
    /* Äußerer Seiten-Hintergrund (Beige/Grau) */
    .stApp {{ 
        background-color: #ffffff !important; 
    }}
    
    /* Die weiße Karte (Container) */
    .main .block-container {{
        background-color: #ffffff !important;
        border-radius: 40px !important;
        max-width: 500px !important;
        margin-top: 1rem !important;
        margin-bottom: 2rem !important;
        padding: 1rem 1.5rem 4rem 1.5rem !important;
        box-shadow: 0 15px 50px rgba(0,0,0,0.2) !important;
    }}

    /* Streamlit-Elemente ausblenden */
    [data-testid="stAppToolbar"], [data-testid="stHeader"], [data-testid="stFooter"], 
    footer, header, #stDecoration {{ display: none !important; }}

    /* Header Bild zentrieren */
    .header-box {{
        text-align: center;
        margin-bottom: 0.5rem;
        padding-top: 1rem;
    }}
    .header-box img {{
        width: 85%;
        max-width: 320px;
    }}

    /* "Wähle Fotos..." Text */
    .sub-text {{
        text-align: center;
        color: #666666;
        font-family: 'Inter', sans-serif;
        font-size: 1.15rem;
        margin-bottom: 2.5rem;
    }}

    /* Upload Bereich mit Bokeh-Hintergrund */
    .stFileUploader section {{
        background-image: url("data:image/png;base64,{bg_base64}") !important;
        background-size: cover !important;
        background-position: center !important;
        border: 2px solid #e0d9c1 !important;
        padding: 4.5rem 1.5rem !important;
        border-radius: 35px !important;
        text-align: center;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* Kamera Icon */
    .stFileUploader section::before {{
        content: "";
        display: block;
        width: 140px;
        height: 140px;
        margin: 0 auto 1.5rem auto;
        background-image: url("data:image/png;base64,{camera_base64}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
    }}

    /* Container des Buttons auf 100% Breite setzen */
    .stFileUploader section > div {{
        width: 100% !important;
        display: flex !important;
        justify-content: center !important;
    }}

    /* Der Goldene Button - Jetzt 100% Breite */
    .stFileUploader section button {{
        background: linear-gradient(180deg, #dfbc5e 0%, #b8860b 100%) !important;
        color: #1a1a1a !important;
        border-radius: 20px !important;
        padding: 0.9rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.25rem !important;
        border: none !important;
        box-shadow: 0 5px 20px rgba(184, 134, 11, 0.4) !important;
        text-transform: none !important;
        width: 100% !important;
        margin: 0 auto !important;
        display: block !important;
        position: relative;
    }}
    
    /* Text-Ersatz für den Button auf Deutsch & Zentriert */
    .stFileUploader section button span {{
        visibility: hidden;
        display: block !important;
        width: 100% !important;
    }}
    .stFileUploader section button span::before {{
        content: "Fotos & Videos hochladen";
        visibility: visible;
        display: block;
        position: absolute;
        width: 100% !important;
        left: 0;
        right: 0;
        top: 50%;
        transform: translateY(-50%);
        text-align: center;
    }}

    /* Englische Texte entfernen */
    .stFileUploader section div div {{ display: none !important; }}

    /* Dateinamen-Text in Schwarz */
    [data-testid="stFileUploaderFileData"] div {{
        color: #000000 !important;
        font-weight: 500 !important;
    }}

    /* Erfolgsmeldung */
    .success-box {{
        background-color: #d1f2e5;
        color: #2c6e49;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: left;
        font-size: 1.1rem;
        margin-top: 2rem;
        font-weight: 500;
    }}
    </style>
    """, unsafe_allow_html=True)

# Layout Struktur
st.markdown(f'<div class="header-box"><img src="data:image/png;base64,{header_base64}"></div>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Wähle Fotos oder Videos aus deiner Galerie</p>', unsafe_allow_html=True)

# Dropbox Logik (Bleibt identisch)
def get_dropbox_client():
    refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
    app_key = os.getenv("DROPBOX_APP_KEY")
    app_secret = os.getenv("DROPBOX_APP_SECRET")
    if refresh_token and app_key and app_secret:
        return dropbox.Dropbox(oauth2_refresh_token=refresh_token, app_key=app_key, app_secret=app_secret)
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
    except: return False

if 'hochgeladene_dateien' not in st.session_state:
    st.session_state.hochgeladene_dateien = set()

# Uploader
uploaded_files = st.file_uploader("Upload", type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded_files:
    neue_dateien = [f for f in uploaded_files if f.name not in st.session_state.hochgeladene_dateien]
    if neue_dateien:
        status_container = st.empty()
        progress_bar = st.progress(0)
        for i, datei in enumerate(neue_dateien):
            status_container.markdown(f"<p style='text-align:center'>Lade hoch: {datei.name}</p>", unsafe_allow_html=True)
            if upload_to_dropbox(datei, datei.name):
                st.session_state.hochgeladene_dateien.add(datei.name)
            progress_bar.progress((i + 1) / len(neue_dateien))
        status_container.empty()
        progress_bar.empty()
        if len(st.session_state.hochgeladene_dateien) > 0:
            st.balloons()
            st.markdown('<div class="success-box">✨ Deine Fotos sind sicher bei Marco angekommen!</div>', unsafe_allow_html=True)
