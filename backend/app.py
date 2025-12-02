from flask import Flask, request, jsonify
import yfinance as yf
import json
import os
from cryptography.fernet import Fernet

app = Flask(__name__)

# Chave secreta Fernet (32 bytes Base64) - só você deve conhecer
KEY = b"COLOQUE_SUA_CHAVE_AQUI"
fernet = Fernet(KEY)

# Arquivos de dados
EMAIL_DB_FILE = "data/used_emails.json"
ENC_FILE = "data/submissions.enc"

# Cria pasta data se não existir
os.makedirs("data", exist_ok=True)

# Carrega emails já usados
if os.path.exists(EMAIL_DB_FILE):
    with open(EMAIL_DB_FILE, "r") as f:
        used_emails = set(json.load(f))
else:
    used_emails = set()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    email = data.get("email", "").strip().lower()
    ticker = data.get("ticker", "").strip().upper()
    amount = data.get("amount")
    country = data.get("country", "").strip()
    send_copy = data.get("send_copy", "no")

    # Validação básica
    if not email or not ticker or not amount or not country:
        return jsonify({"error": "All fields are required."}), 400

    if email in used_emails:
        return jsonify({"error": "This email has already submitted a request."}), 403

    # Valida o ticker
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if "regularMarketPrice" not in info:
            raise ValueError
    except:
        return jsonify({"error": "Invalid stock ticker."}), 400

    # Cria submissão
    submission = {
        "email": email,
        "ticker": ticker,
        "amount": amount,
        "country": country,
        "send_copy": send_copy
    }

    # Criptografa e salva
    submission_json = json.dumps(submission).encode()
    encrypted_data = fernet.encrypt(submission_json)
    with open(ENC_FILE, "ab") as f:
        f.write(encrypted_data + b"\n")

    # Atualiza lista de emails usados
    used_emails.add(email)
    with open(EMAIL_DB_FILE, "w") as f:
        json.dump(list(used_emails), f)

    # Placeholder envio de cópia
    if send_copy.lower() == "yes":
        print(f"Sending copy to {email}... (not implemented)")

    return jsonify({"success": f"Request received for {ticker} with amount {amount}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
