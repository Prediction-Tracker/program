# app.py
from flask import Flask, request, jsonify
import yfinance as yf
import json
import os

app = Flask(__name__)

# Arquivo para controlar emails já usados
EMAIL_DB_FILE = "data/used_emails.json"

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
    send_copy = data.get("send_copy", "no")

    # Validação simples
    if not email or not ticker or not amount:
        return jsonify({"error": "All fields are required."}), 400

    if email in used_emails:
        return jsonify({"error": "This email has already submitted a request."}), 403

    # Valida o ticker com yfinance
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        if "regularMarketPrice" not in info:
            raise ValueError
    except:
        return jsonify({"error": "Invalid stock ticker."}), 400

    # Aqui você armazenaria a solicitação em um banco de dados real
    used_emails.add(email)
    with open(EMAIL_DB_FILE, "w") as f:
        json.dump(list(used_emails), f)

    # Envio de cópia por email (placeholder)
    if send_copy.lower() == "yes":
        # TODO: configurar envio real com SMTP/SendGrid/etc
        print(f"Sending copy to {email}... (not implemented)")

    return jsonify({"success": f"Request received for {ticker} with amount {amount}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
