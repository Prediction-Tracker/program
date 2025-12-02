from flask import Flask, request, jsonify
import yfinance as yf
import matplotlib.pyplot as plt
import io, base64
from statsmodels.tsa.arima.model import ARIMA
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from prophet import Prophet
import pandas as pd

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    ticker = data.get("ticker")
    email = data.get("email")
    country = data.get("country")
    send_copy = data.get("sendCopy")

    # Validar ticker
    try:
        df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
        if df.empty:
            return jsonify({"error": "Ticker inválido"}), 400
    except:
        return jsonify({"error": "Erro ao baixar dados"}), 400

    # Calcular indicadores
    df["SMA20"] = SMAIndicator(df["Close"], window=20).sma_indicator()
    df["SMA50"] = SMAIndicator(df["Close"], window=50).sma_indicator()
    df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()

    # Gerar gráfico SMA + Close
    plt.figure(figsize=(10,4))
    plt.plot(df["Close"], label="Close")
    plt.plot(df["SMA20"], label="SMA20")
    plt.plot(df["SMA50"], label="SMA50")
    plt.title(f"{ticker} - Close e SMA")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # Gerar previsão Prophet (30 dias)
    df_reset = df.reset_index()[["Date","Close"]].rename(columns={"Date":"ds","Close":"y"})
    model = Prophet(daily_seasonality=True)
    model.fit(df_reset)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    # Gráfico previsão Prophet
    plt.figure(figsize=(10,4))
    plt.plot(df_reset["ds"], df_reset["y"], label="Histórico")
    plt.plot(forecast["ds"], forecast["yhat"], label="Previsto", linestyle="--")
    plt.title(f"{ticker} - Previsão 30 dias")
    plt.legend()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png")
    buf2.seek(0)
    forecast_base64 = base64.b64encode(buf2.read()).decode("utf-8")
    plt.close()

    # Retornar imagens base64
    return jsonify({
        "sma_img": img_base64,
        "forecast_img": forecast_base64
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
