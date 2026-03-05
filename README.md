# 🎂 Marcos 50. Geburtstag - Foto Uploader

Ein mobiler Foto- & Video-Uploader für Marcos 50. Geburtstag. Gäste können Medien direkt vom Smartphone in einen Dropbox-Ordner hochladen.

## 🛠️ Dateien
- `app.py`: Die Streamlit Web-App.
- `requirements.txt`: Benötigte Python-Bibliotheken.

---

## 📦 Schritt 1: Dropbox API einrichten

1. **App erstellen:**
   - Gehe zur [Dropbox App Console](https://www.dropbox.com/developers/apps).
   - Klicke auf **"Create App"**.
   - Wähle **"Scoped Access"**.
   - Wähle **"App folder"** (Sicherer, Zugriff nur auf einen Ordner) oder **"Full Dropbox"**.
   - Gib der App einen Namen (z.B. `Marcos-50-Uploader`).

2. **Berechtigungen (Permissions) setzen:**
   - Gehe zum Tab **"Permissions"**.
   - Aktiviere das Häkchen bei `files.content.write`.
   - Klicke unten auf **"Submit"** oder **"Update"**, um die Änderungen zu speichern.

3. **Token generieren:**
   - Gehe zurück zum Tab **"Settings"**.
   - Suche den Bereich **"Generated access token"**.
   - Klicke auf **"Generate"**.
   - **Wichtig:** Dieser Token ist kurzlebig (ca. 4 Std.). Für die Party solltest du den Token kurz vorher generieren oder eine "Refresh Token" Logik nutzen. Kopiere diesen Token für Schritt 2.

---

## 🚀 Schritt 2: Deployment (Streamlit Cloud)

Streamlit Cloud ist der einfachste Weg, diese App kostenlos zu hosten.

1. Erstelle ein Repository auf **GitHub** und lade `app.py` und `requirements.txt` hoch.
2. Melde dich bei [Streamlit Cloud](https://share.streamlit.io/) mit deinem GitHub-Account an.
3. Klicke auf **"New app"**, wähle dein Repository und `app.py` aus.
4. **Geheimnisse (Secrets) hinzufügen:**
   - Klicke vor dem Deployen auf **"Advanced settings"**.
   - Füge im Feld **"Secrets"** folgendes ein:
     ```toml
     DROPBOX_ACCESS_TOKEN = "DEIN_KOPIERTER_TOKEN"
     ```
5. Klicke auf **"Deploy!"**. Deine App ist nun unter einer öffentlichen URL (z.B. `marcos-50.streamlit.app`) erreichbar.

---

## 📱 Nutzung für Gäste
- QR-Code mit der URL der App auf der Party auslegen.
- Gäste scannen den Code, wählen Bilder/Videos aus und klicken auf **"Hochladen"**.
- Die Dateien landen automatisch im Dropbox-Ordner `/Apps/Marcos-50-Uploader/Marcos_50_Uploads/` mit Zeitstempel.

---

## ⚙️ Lokale Entwicklung
1. Installiere Anforderungen: `pip install -r requirements.txt`
2. Setze Umgebungsvariable: `export DROPBOX_ACCESS_TOKEN='dein_token'`
3. Starte App: `streamlit run app.py`
