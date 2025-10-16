from flask import Flask, jsonify, request, render_template, send_file
from model.encryption import encrypt, decrypt
import base64
import json
import io

app = Flask(__name__)
app.secret_key = 'friesland'

@app.route('/', methods=['GET', 'POST'])
def index():
    # Variabelen initialiseren
    encrypted_data = None
    key_hex = None
    decrypted_message = None

    if request.method == 'POST':
        if 'encrypt' in request.form:
            # Getypte bericht ophalen uit het formulier op de webpagina
            # Bericht wordt versleuteld met de geïmporteerde encrypt functie
            message = request.form['message']
            nonce, ciphertext, tag, key = encrypt(message)

            # Encodeer nonce, ciphertext, tag en key in base64 om zeker te zijn dat het
            # correct wordt verwerkt bij omzetting naar JSON en html weergave
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
            # Ingevoerde sleutels ophalen uit het formulier op de webpagina
            key_hex_input = request.form['key']
            nonce_b64 = request.form['nonce']
            ciphertext_b64 = request.form['ciphertext']
            tag_b64 = request.form['tag']
            try:
                # Zet hex en base64 terug om naar bytes om correct ontsleutelen
                key = bytes.fromhex(key_hex_input)
                nonce = base64.b64decode(nonce_b64)
                ciphertext = base64.b64decode(ciphertext_b64)
                tag = base64.b64decode(tag_b64)
                decrypted_message = decrypt(nonce, ciphertext, tag, key)
            except Exception as e:
                decrypted_message = "Decryption mislukt. Controleer de invoer."

    return render_template('index.html', encrypted_data=encrypted_data, key_hex=key_hex, decrypted_message=decrypted_message)

@app.route('/download', methods=['POST'])
def download_data():
    data = request.form.to_dict()
    # Gegevens uit het encryption proces ophalen
    # Deze data wordt in JSON formaat opgeslagen
    # Data bevat key, nonce, ciphertext, tag
    json_data = json.dumps(data)

    # Maak een in-memory bestand
    # Hiermee wordt een tijdelijk bestand aangemaakt dat direct wordt gedownload
    # Daarna wordt het bestand verwijderd en kan het niet meer worden opgevraagd
    buffer = io.BytesIO()
    buffer.write(json_data.encode('utf-8'))
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name='encrypted_data.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)