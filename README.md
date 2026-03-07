# 🎂 Marcos 50. Geburtstag - Foto Uploader

Ein moderner Foto- & Video-Uploader im Dribbble-Design. Gäste können Medien direkt vom Smartphone in einen Dropbox-Ordner hochladen – ohne Login, ohne Stress.

---

## 🛠️ Dateien
- `app.py`: Die Streamlit Web-App (UI + Backend).
- `requirements.txt`: Python-Bibliotheken (`streamlit`, `dropbox`).

---

## 📦 Schritt 1: Dropbox App erstellen

1.  Gehe zur [Dropbox App Console](https://www.dropbox.com/developers/apps).
2.  Klicke auf **"Create App"**.
3.  Wähle:
    - **API**: "Scoped Access"
    - **Zugriffstyp**: "App folder" (Sicherer) oder "Full Dropbox"
    - **Name**: z.B. `Marcos-50-Uploader`
4.  Gehe zum Tab **"Permissions"**:
    - Aktiviere das Häkchen bei **`files.content.write`**.
    - Klicke unten auf **"Submit"** oder **"Update"**.
5.  Gehe zum Tab **"Settings"**:
    - Kopiere den **App key** und den **App secret**. Du brauchst sie für Schritt 2.

---

## 🔑 Schritt 2: Dauerhaften Refresh-Token erhalten

Standard-Token halten nur 4 Stunden. Für die Party brauchst du einen **Refresh-Token**:

1.  **Autorisierungs-Link erstellen**:
    Ersetze `DEIN_APP_KEY` im folgenden Link und öffne ihn im Browser:
    `https://www.dropbox.com/oauth2/authorize?client_id=DEIN_APP_KEY&token_access_type=offline&response_type=code`

2.  Klicke auf **"Weiter"** -> **"Zulassen"**. Kopiere den angezeigten **Code**.

3.  **Token generieren (Terminal)**:
    Führe diesen Befehl aus (ersetze die Platzhalter):
    ```bash
    curl https://api.dropbox.com/oauth2/token \
        -d code=DEIN_KOPIERTER_CODE \
        -d grant_type=authorization_code \
        -u DEIN_APP_KEY:DEIN_APP_SECRET
    ```
    In der Antwort findest du den `"refresh_token"`. **Dieser ist dauerhaft gültig!**

---

## 🚀 Schritt 3: Deployment (Streamlit Cloud)

1.  Lade `app.py` und `requirements.txt` in ein privates GitHub-Repository hoch.
2.  Verbinde das Repo mit [Streamlit Cloud](https://share.streamlit.io/).
3.  Gehe vor dem Deployen auf **"Advanced settings"** -> **"Secrets"**.
4.  Füge deine Zugangsdaten ein:
    ```toml
    DROPBOX_REFRESH_TOKEN = "dein_refresh_token_hier"
    DROPBOX_APP_KEY = "dein_app_key_hier"
    DROPBOX_APP_SECRET = "dein_app_secret_hier"
    ```
5.  Klicke auf **"Deploy!"**.

---

## 📱 Tipps für die Party
- **QR-Code**: Drucke einen QR-Code mit der URL der App aus und verteile ihn auf den Tischen.
- **WLAN**: Wenn das mobile Netz schwach ist, hänge die WLAN-Zugangsdaten direkt daneben.
- **Live-Diashow**: Du kannst den Dropbox-Ordner an deinem Laptop öffnen und die Fotos direkt als Diashow an die Wand werfen!

Viel Spaß beim Feiern! 🥳🎂
