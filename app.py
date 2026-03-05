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

# Extrem einfaches Design für bessere Lesbarkeit
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    /* Größere Schrift für die Anweisungen */
    .big-text {
        font-size: 1.5rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Den Datei-Uploader Bereich optisch hervorheben */
    .stFileUploader section {
        border: 3px dashed #ff4b4b !important;
        padding: 2rem !important;
        border-radius: 15px;
    }
    h1 {
        text-align: center;
        color: #ff4b4b;
        font-size: 3rem !important;
    }
    /* Streamlit Menü, Footer und Header ausblenden */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("🎂 Marcos 50.")
st.markdown('<p class="big-text">Fotos & Videos für Marco hochladen</p>', unsafe_allow_html=True)

# Dropbox Logik
def upload_to_dropbox(file_obj, filename):
    token = os.getenv("DROPBOX_ACCESS_TOKEN")
    if not token:
        st.error("Konfigurationsfehler: Bitte den Administrator informieren (Token fehlt).")
        return False
    
    try:
        dbx = dropbox.Dropbox(token)
        clean_name = re.sub(r'[^a-zA-Z0-9\._-]', '_', filename)
        timestamp = datetime.now().strftime("%H%M%S") # Nur Zeit für den Dateinamen
        date_folder = datetime.now().strftime("%Y-%m-%d")
        
        # Ordner-Struktur: /Marcos_50_Uploads/DATUM/ZEIT_NAME.jpg
        target_path = f"/Marcos_50_Uploads/{date_folder}/{timestamp}_{clean_name}"
        
        dbx.files_upload(file_obj.getvalue(), target_path, mode=dropbox.files.WriteMode.overwrite)
        return True
    except Exception as e:
        st.error(f"Fehler beim Hochladen von {filename}. Bitte nochmal versuchen.")
        return False

# Session State initialisieren, um doppelte Uploads zu vermeiden
if 'hochgeladene_dateien' not in st.session_state:
    st.session_state.hochgeladene_dateien = set()

# Der Uploader (Accepts multiple files)
uploaded_files = st.file_uploader(
    "Hier drücken, um Fotos auszuwählen", 
    type=["jpg", "jpeg", "png", "mp4", "mov", "avi"], 
    accept_multiple_files=True,
    label_visibility="visible"
)

# Automatischer Upload-Prozess
if uploaded_files:
    # Nur Dateien hochladen, die noch nicht in dieser Sitzung hochgeladen wurden
    neue_dateien = [f for f in uploaded_files if f.name not in st.session_state.hochgeladene_dateien]
    
    if neue_dateien:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        erfolgreich = 0
        gesamt = len(neue_dateien)
        
        for i, datei in enumerate(neue_dateien):
            status_text.markdown(f"**Wird hochgeladen:** {datei.name}...")
            if upload_to_dropbox(datei, datei.name):
                erfolgreich += 1
                st.session_state.hochgeladene_dateien.add(datei.name)
            
            progress_bar.progress((i + 1) / gesamt)
        
        status_text.empty()
        progress_bar.empty()

        if erfolgreich > 0:
            st.balloons()
            st.success(f"✅ Fertig! {erfolgreich} Datei(en) sind sicher bei Marco angekommen.")
            st.markdown('<p style="text-align: center; font-size: 1.2rem;">Du kannst jetzt einfach weitere Fotos auswählen oder die Seite schließen.</p>', unsafe_allow_html=True)

# Kurze Anleitung für die Gäste
st.info("💡 **So geht's:** Klicke oben auf das große Feld, wähle deine schönsten Fotos aus deiner Galerie aus und bestätige mit 'Hinzufügen' oder 'Fertig'. Der Rest passiert von ganz allein!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Viel Spaß beim Feiern! 🥳</p>", unsafe_allow_html=True)
