
from flask import Flask, request, jsonify
import os
import datetime

# Initialize the Flask app
app = Flask(__name__)

# Webhook endpoint to receive TradingView alerts
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("Received alert:", data)

        # Extract relevant fields from TradingView alert
        symbol = data.get("symbol")
        direction = data.get("direction")  # e.g., "buy" or "sell"
        price = float(data.get("price", 0))
        time = data.get("time")

        # Dummy example logic (replace with your actual strike prediction logic)
        prediction = {
            "symbol": symbol,
            "direction": direction,
            "strike": round(price),
            "entry_price": price,
            "T1": round(price * 1.02, 2),
            "T2": round(price * 1.04, 2),
            "T3": round(price * 1.06, 2),
            "SL": round(price * 0.98, 2),
            "time": time
        }

        print("Generated prediction:", prediction)

        return jsonify({"status": "success", "prediction": prediction}), 200

    except Exception as e:
        print("Webhook error:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Basic route to check server status
@app.route("/", methods=["GET"])
def home():
    return "✅ Smart Option Predictor is live!", 200

# Run the app (only if running locally; Render uses gunicorn)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
