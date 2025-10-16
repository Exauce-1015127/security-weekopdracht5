from flask import Flask, jsonify, request, abort, url_for, redirect, render_template, flash, session
from model.encryption import encrypt, decrypt
from model.login_module import login_user
from model.registratie_module import register_user
import sqlite3
import base64

app = Flask(__name__)
app.secret_key = 'friesland'

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def verify_password(stored_password, provided_password):
    # Hier zou je de werkelijke verificatielogica implementeren, bijvoorbeeld met Argon2
    return stored_password == provided_password  # Vervang dit door echte verificatie
@app.route('/')
def index():
    return render_template('login.html')


@app.route("/login", methods=["POST"])
def login_user():
    if not request.is_json:
        return jsonify({"success": False, "message": "Ongeldig verzoek. JSON verwacht."}), 400

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"success": False, "message": "Gebruikersnaam en wachtwoord zijn verplicht."}), 400

    print(f"Ingevoerde gebruikersnaam: {username}")  # Debug

    if login_user(username, password):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        session['login'] = user[0]
        print(f"Gebruiker ingelogd: {session.get('login')}")  # Debug
        return jsonify({"success": True, "message": "Succesvol ingelogd!", "redirect": url_for("dashboard")}), 200
    else:
        print("Inloggen mislukt.")  # Debug
        return jsonify({"success": False, "message": "Ongeldige inloggegevens"}), 401


@app.route("/dashboard")
def dashboard():
    if "login" not in session:
        return jsonify({"success": False, "message": "Niet ingelogd"}), 401
    return f"Welkom gebruiker {session['login']}!"

@app.route('/registratie')
def registerpage():
    return render_template('registratie.html')

@app.route('/dashboard2')
def dashboard2():
    return render_template('dashboard2.html')

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    encrypted_data = None
    key_hex = None
    decrypted_message = None

    if request.method == 'POST':
        if 'encrypt' in request.form:
            # Gebruiker wil encrypten
            message = request.form['message']
            nonce, ciphertext, tag, key = encrypt(message)
            # Encodeer nonce, ciphertext, tag, key in base64 om ze makkelijk te kunnen zetten
            nonce_b64 = base64.b64encode(nonce).decode('utf-8')
            ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
            tag_b64 = base64.b64encode(tag).decode('utf-8')
            key_hex = key.hex()
            encrypted_data = {
                'nonce': nonce_b64,
                'ciphertext': ciphertext_b64,
                'tag': tag_b64
            }
        elif 'decrypt' in request.form:
            # Gebruiker wil decrypten
            key_hex_input = request.form['key']
            nonce_b64 = request.form['nonce']
            ciphertext_b64 = request.form['ciphertext']
            tag_b64 = request.form['tag']
            try:
                key = bytes.fromhex(key_hex_input)
                nonce = base64.b64decode(nonce_b64)
                ciphertext = base64.b64decode(ciphertext_b64)
                tag = base64.b64decode(tag_b64)
                decrypted_message = decrypt(nonce, ciphertext, tag, key)
            except Exception as e:
                decrypted_message = "Decryption mislukt. Controleer de invoer."

    return render_template('index2.html', encrypted_data=encrypted_data, key_hex=key_hex, decrypted_message=decrypted_message)

if __name__ == '__main__':
    app.run(debug=True)