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

    # Validar ticker
    try:
        df = yf.download(ticker, period="1y", interval="1d", auto_adjust=True)
        if df.empty:
            return jsonify({"error": "Invalid ticker"}), 400
    except:
        return jsonify({"error": "Failed to fetch data"}), 400

    # Indicadores
    df["SMA20"] = SMAIndicator(df["Close"], window=20).sma_indicator()
    df["SMA50"] = SMAIndicator(df["Close"], window=50).sma_indicator()
    df["RSI"] = RSIIndicator(df["Close"], window=14).rsi()

    # Gráfico SMA
    plt.figure(figsize=(10,4))
    plt.plot(df["Close"], label="Close")
    plt.plot(df["SMA20"], label="SMA20")
    plt.plot(df["SMA50"], label="SMA50")
    plt.title(f"{ticker} - Close & SMA")
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    sma_img = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # Previsão Prophet 30 dias
    df_reset = df.reset_index()[["Date","Close"]].rename(columns={"Date":"ds","Close":"y"})
    model = Prophet(daily_seasonality=True)
    model.fit(df_reset)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)

    plt.figure(figsize=(10,4))
    plt.plot(df_reset["ds"], df_reset["y"], label="History")
    plt.plot(forecast["ds"], forecast["yhat"], label="Forecast", linestyle="--")
    plt.title(f"{ticker} - 30-day Forecast")
    plt.legend()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format="png")
    buf2.seek(0)
    forecast_img = base64.b64encode(buf2.read()).decode("utf-8")
    plt.close()

    return jsonify({"sma_img": sma_img, "forecast_img": forecast_img})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

