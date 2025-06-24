
import os
from flask import Flask, request, jsonify
from kiteconnect import KiteConnect
import datetime

app = Flask(__name__)

# === Load credentials from Render environment variables ===
kite_api_key = os.environ.get("w2v7z50yd1kfrj9m")
kite_api_secret = os.environ.get("7f2litnjzyo7k764qelgrejaploaoahh")
access_token = os.environ.get("tjr3Zrwcx48PESt7ZNqiLwExqHIgWxqa")

kite = KiteConnect(api_key=kite_api_key)
kite.set_access_token(access_token)

# === Utility: Round to nearest strike (e.g., 50-point intervals) ===
def get_atm_strike(ltp, step=50):
    return round(ltp / step) * step

# === Fetch option LTP ===
def fetch_option_ltp(symbol):
    try:
        data = kite.ltp([symbol])
        return data[symbol]['last_price']
    except:
        return None

# === Webhook endpoint for TradingView alerts ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    index_name = data.get("index", "NIFTY")
    direction = data.get("signal", "BUY")  # "BUY" for CE, "SELL" for PE

    # === Expiry (nearest weekly expiry - Thursday) ===
    today = datetime.date.today()
    weekday = today.weekday()
    days_to_thursday = (3 - weekday) % 7
    expiry = today + datetime.timedelta(days=days_to_thursday)

    # === Get index LTP and calculate ATM strike
    try:
        index_ltp = kite.ltp(f"NSE:{index_name}")[f"NSE:{index_name}"]['last_price']
    except Exception as e:
        return jsonify({"error": f"Failed to fetch index LTP: {e}"}), 400

    atm_strike = get_atm_strike(index_ltp)
    option_type = "CE" if direction == "BUY" else "PE"

    # === Construct option symbol
    expiry_str = expiry.strftime('%y%b').upper()
    option_symbol = f"NSE:{index_name}{expiry_str}{atm_strike}{option_type}"

    option_ltp = fetch_option_ltp(option_symbol)
    if option_ltp is None:
        return jsonify({"error": "Failed to fetch option LTP"}), 400

    # === Targets and Stop Loss
    T1 = round(option_ltp + 10, 2)
    T2 = round(option_ltp + 20, 2)
    T3 = round(option_ltp + 30, 2)
    SL = round(option_ltp * 0.75, 2)

    # === Final JSON response
    response = {
        "signal": direction,
        "index_ltp": round(index_ltp, 2),
        "strike": atm_strike,
        "option_type": option_type,
        "option_symbol": option_symbol,
        "option_ltp": round(option_ltp, 2),
        "expiry": expiry.strftime("%d-%b-%Y"),
        "T1": T1,
        "T2": T2,
        "T3": T3,
        "SL": SL
    }

    print("Webhook Signal:", response)
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
