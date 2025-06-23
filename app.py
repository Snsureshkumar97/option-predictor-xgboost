
from flask import Flask, request, jsonify
import os
import requests
import datetime

app = Flask(__name__)

# === Zerodha Token from Render env ===
Z_API_KEY = os.getenv("Z_API_KEY")
Z_ACCESS_TOKEN = os.getenv("Z_ACCESS_TOKEN")

# === Endpoint to receive webhook from TradingView ===
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    signal = data.get("signal")
    symbol = data.get("symbol", "NIFTY")
    timestamp = data.get("timestamp", str(datetime.datetime.now()))

    print(f"[✅] Webhook received: {signal.upper()} | {symbol} | {timestamp}")
    
    if not Z_ACCESS_TOKEN:
        print("[❌] Missing Zerodha access token")
        return jsonify({"error": "Zerodha token missing"}), 401

    print(f"[🔁] Fetching live option chain data for {symbol}...")

    # === Mocked Zerodha data (replace with real request if needed) ===
    try:
        # Simulate fetching option data
        # Example: replace this with actual Kite Connect call using pykiteconnect
        strike_price = "23400 CE"
        ltp = 102.0
        t1 = round(ltp * 1.15, 2)
        t2 = round(ltp * 1.35, 2)
        t3 = round(ltp * 1.55, 2)
        sl = round(ltp * 0.85, 2)

        print(f"[🎯] Predicted: {strike_price} @ ₹{ltp}")
        print(f"     → T1 ₹{t1}, T2 ₹{t2}, T3 ₹{t3}, SL ₹{sl}")

        return jsonify({
            "symbol": symbol,
            "strike": strike_price,
            "entry": ltp,
            "targets": {"T1": t1, "T2": t2, "T3": t3},
            "stop_loss": sl,
            "timestamp": timestamp
        })

    except Exception as e:
        print(f"[❌] Error fetching data: {e}")
        return jsonify({"error": "Failed to fetch option data"}), 500


# === Optional root route to prevent 404 ===
@app.route("/", methods=["GET"])
def home():
    return "✅ Smart Option Predictor Backend is live!"
