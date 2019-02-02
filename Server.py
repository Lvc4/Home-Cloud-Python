from flask import *
import os
from werkzeug.utils import secure_filename
import db # Importieren der db.py

# Initialisiert die Flask app
app = Flask(__name__)

mypassword = 'password'
app.config['UPLOAD_FOLDER'] = 'uploads'# Definiert Upload Ordner
app.secret_key = 'X\xa1\xd2\x13\xfc\x9f\xb8\xd1=\xe5A\xd4\x90\xe5>\xb4\xf9\x92F\xd4_\xc1\xa4K\xa3\xa3|\x13kL\xc6\xa0JJ\xe4\xd9\xc3\x9cL\x0e\xb0\x1e\xa6\x11\xee\xf2\xad\xa1'# Session key
ALLOWED_EXTENSIONS = set(['odt', 'ods', 'vbs', 'py', 'zip', 'rar', 'jar', 'php', 'css', 'html', 'exe', 'bat', 'mp3', 'mp4', 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])# Erlaubte Datei typen

def allowed_file(filename):# Checkt ob eine Datei vom typ erlaubt ist
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['POST', 'GET'])# Login seite
def login():
    if request.method == 'POST':# Falls das Passwort gesendet wird
        password = request.form['pass']# Passwort empfangen
        if password == mypassword:# Passwort prüfen
            session['logged_in'] = "Is_logged_in"# Login session erstellen
            return redirect('/')
        else:#Passwort Falsch
            return render_template('login.html')# Erneut die Login Seite
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])# Haubtmenü
def list_files():
    if 'logged_in' in session and session['logged_in'] == "Is_logged_in":# Login Session prüfen
        if request.method == 'POST':# Logout
            session.pop('logged_in', None)# Login Session löschen
            return redirect('/login')
        elif request.method == 'GET':
        	return render_template('index.html',files = db.view())# index.html mit liste der hochgeladenen Dateien zurückgeben
    else:
        return redirect('/login')

@app.route('/upload', methods=['POST', 'GET'])# Upload
def upload_file():
    if 'logged_in' in session and session['logged_in'] == "Is_logged_in":# Login Session prüfen
        if request.method == 'POST':
            if 'file' not in request.files:# Checken ob eine Datei gesendet wurde
                flash('Keine Datei gesendet')
                return redirect(request.url)
            file = request.files['file']# Datei empfangen
            if file.filename == '':# Dateiname checken
                flash('Keine Datei ausgwählt')
                return redirect(request.url)
            if file and allowed_file(file.filename):# Checken ob diese Datei erlaubt ist
                filename = secure_filename(file.filename)
                db.insert(filename)# Datei in die Datenbank eintragen
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))# Datei in UPLOAD_FOLDER speichern
                return redirect('/')
        elif request.method == 'GET':
            return render_template('Upload.html')
    else:
        return redirect('/login')

@app.route('/upload/<filename>', methods=['GET'])# Datei anzeigen / runterladen
def uploaded_file(filename):
    if 'logged_in' in session and session['logged_in'] == "Is_logged_in":# Login Session prüfen
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)# Datei zurückgeben
    else: return redirect('/login')

@app.route('/delete', methods=['POST', 'GET'])# Dateien löschen
def delete_file():
    if 'logged_in' in session and session['logged_in'] == "Is_logged_in":# Login Session prüfen
        if request.method == 'POST':
            filename = request.form['file']# Zu löschenden Dateinamen erhalten
            db.delete(filename)# Datei aus der Datenbank löschen
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))# Datei aus UPLOAD_FOLDER löschen
            return redirect('/')

        elif request.method == 'GET':
            return render_template('delete.html', files = db.view())
    else:
        return redirect('/login')

# App starten
if __name__ == "__main__":
    app.run(
        debug=False,# Wird nicht gedebugt
        host= '192.168.180.40',# Host setzen
        threaded=True,# Multithreading erlaubt mehrere Clients gleichzeitig
        port = 80 # Port setzen
        )
