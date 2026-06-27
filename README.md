# PyBot AI Chatbot 🤖

## Kaise chalayein (VS Code mein)

### Step 1 — API Key daalo
`app.py` file kholo aur ye line dhundho:
```
API_KEY = "YOUR_ANTHROPIC_API_KEY"
```
Apni real key yahan daalo.
Key yahan se lo: https://console.anthropic.com

### Step 2 — Libraries install karo
VS Code mein Terminal kholo (Ctrl + `) aur likho:
```
pip install -r requirements.txt
```

### Step 3 — Server chalao
```
python app.py
```

### Step 4 — Browser mein kholo
```
http://localhost:5000
```

## Files
- app.py       → Python backend (Flask server)
- index.html   → Chatbot UI
- requirements.txt → Required libraries
