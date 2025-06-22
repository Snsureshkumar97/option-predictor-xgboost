
# Smart Option King AI System

## Setup Instructions

1. Paste your `Z_API_KEY` and daily `Z_ACCESS_TOKEN` into `.env` file.
2. Push this repo to GitHub.
3. Connect the repo to Render.com for 24/7 hosting.
4. Set TradingView alerts to POST to:
   `https://your-render-service.onrender.com/webhook`

## Input Example (TradingView alert)

```json
{
  "signal": "BUY"
}
```

## Output

```json
{
  "strike": "49700 CE",
  "entry": 122,
  "sl": 108,
  "t1": 138,
  "t2": 156,
  "t3": 168,
  "confidence": "96%",
  "reason": "EMA + RSI + MACD + Volume"
}
```
