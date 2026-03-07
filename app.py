import streamlit as st
import dropbox
from dropbox.exceptions import ApiError, AuthError
import os
from datetime import datetime
import re

# Seite konfigurieren
st.set_page_config(
    page_title="Marcos 50.",
    page_icon="🎂",
    layout="centered"
)

# Modernes Dribbble-Style Design
st.markdown("""
    <style>
    /* Hintergrund & Toolbar entfernen */
    .stApp { background-color: #ffffff; }
    [data-testid="stAppToolbar"], [data-testid="stHeader"], [data-testid="stFooter"], 
    footer, header, #stDecoration { display: none !important; visibility: hidden !important; }
    
    .main .block-container {
        padding-top: 5rem;
        max-width: 500px;
    }
    
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

    /* Der moderne Upload-Kasten */
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
    }

    /* Button Styling */
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
    
    /* Englische Texte ausblenden */
    .stFileUploader section div div { display: none !important; }
    
    /* Icon */
    .stFileUploader section::before {
        content: '📸';
        display: block;
        font-size: 3rem;
        text-align: center;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("Marcos 50.")
st.markdown('<p class="sub-header">Wähle Fotos oder Videos aus deiner Galerie</p>', unsafe_allow_html=True)

# Dropbox Logik mit Unterstützung für Refresh-Tokens (Dauerhaft gültig)
def get_dropbox_client():
    # 1. Versuch: Refresh Token Flow (Empfohlen für die Party)
    refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
    app_key = os.getenv("DROPBOX_APP_KEY")
    app_secret = os.getenv("DROPBOX_APP_SECRET")
    
    if refresh_token and app_key and app_secret:
        return dropbox.Dropbox(
            oauth2_refresh_token=refresh_token,
            app_key=app_key,
            app_secret=app_secret
        )
    
    # 2. Versuch: Einfacher Access Token (Hält nur 4 Std.)
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if access_token:
        return dropbox.Dropbox(access_token)
        
    return None

def upload_to_dropbox(file_obj, filename):
    dbx = get_dropbox_client()
    if not dbx:
        st.error("Fehler: Keine Dropbox-Zugangsdaten gefunden (Token fehlt).")
        return False
    
    try:
        clean_name = re.sub(r'[^a-zA-Z0-9\._-]', '_', filename)
        timestamp = datetime.now().strftime("%H%M%S")
        date_folder = datetime.now().strftime("%Y-%m-%d")
        target_path = f"/Marcos_50_Uploads/{date_folder}/{timestamp}_{clean_name}"
        
        dbx.files_upload(file_obj.getvalue(), target_path, mode=dropbox.files.WriteMode.overwrite)
        return True
    except AuthError:
        st.error("Fehler: Dropbox Token ist ungültig oder abgelaufen.")
    except ApiError as e:
        st.error(f"Dropbox API Fehler: {e}")
    except Exception as e:
        st.error(f"Unerwarteter Fehler: {e}")
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
