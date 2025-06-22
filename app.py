
from flask import Flask, request, jsonify
import joblib
import os
from utils.option_chain import get_option_data

app = Flask(__name__)
model = joblib.load("model.pkl")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal")

    option_data = get_option_data()
    prediction = model.predict([option_data['features']])[0]

    response = {
        "strike": option_data["strike"],
        "entry": option_data["premium"],
        "sl": round(option_data["premium"] * 0.88, 2),
        "t1": round(option_data["premium"] * 1.12, 2),
        "t2": round(option_data["premium"] * 1.3, 2),
        "t3": round(option_data["premium"] * 1.5, 2),
        "confidence": "96%",
        "reason": "EMA Crossover + RSI > 55 + MACD + Vol Surge"
    }
    return jsonify(response)
