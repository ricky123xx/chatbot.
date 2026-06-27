from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from groq import Groq
import os
import json
import uuid
from datetime import datetime

app = Flask(__name__, static_folder=".")
CORS(app)

API_KEY = "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"
client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """You are PyBot, a smart and friendly AI assistant.
- Reply in the same language the user writes in (Hindi, Hinglish, or English).
- For code, always use proper markdown code blocks with the language name.
- Keep answers clear, helpful, and concise.
- Use a warm, conversational tone."""

sessions = {}

def get_session(sid):
    if sid not in sessions:
        sessions[sid] = []
    return sessions[sid]

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/chat/stream", methods=["POST"])
def chat_stream():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()
        sid = data.get("session_id", "default")

        if not user_message:
            return jsonify({"error": "Message empty hai"}), 400

        if API_KEY == "APNI-GROQ-KEY-YAHAN-DAALO":
            return jsonify({"error": "API key set nahi ki! app.py mein API_KEY update karo."}), 401

        history = get_session(sid)
        history.append({"role": "user", "content": user_message})

        def generate():
            full_reply = ""
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
                max_tokens=1024,
                stream=True
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    full_reply += token
                    yield f"data: {json.dumps({'token': token})}\n\n"

            history.append({"role": "assistant", "content": full_reply})
            yield f"data: {json.dumps({'done': True})}\n\n"

        return Response(stream_with_context(generate()),
                        mimetype="text/event-stream",
                        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

    except Exception as e:
        return jsonify({"error": f"Kuch gadbad hui: {str(e)}"}), 500

@app.route("/session/new", methods=["POST"])
def new_session():
    sid = str(uuid.uuid4())[:8]
    sessions[sid] = []
    return jsonify({"session_id": sid})

@app.route("/session/clear", methods=["POST"])
def clear_session():
    data = request.get_json(silent=True) or {}
    sid = data.get("session_id", "default")
    sessions[sid] = []
    return jsonify({"status": "cleared"})

@app.route("/session/export", methods=["POST"])
def export_session():
    data = request.get_json(silent=True) or {}
    sid = data.get("session_id", "default")
    history = get_session(sid)
    lines = [f"PyBot Chat Export — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*50}\n"]
    for msg in history:
        role = "You" if msg["role"] == "user" else "PyBot"
        lines.append(f"\n[{role}]\n{msg['content']}\n")
    text = "\n".join(lines)
    return Response(text, mimetype="text/plain",
                    headers={"Content-Disposition": "attachment; filename=pybot-chat.txt"})

if __name__ == "__main__":
    print("=" * 45)
    print("  ✨ PyBot AI Server (Groq)")
    print("=" * 45)
    if API_KEY == "APNI-GROQ-KEY-YAHAN-DAALO":
        print("  ⚠️  WARNING: API key set nahi ki!")
    else:
        print("  ✅ Groq API key detected")
    print("  🌐 Open: http://localhost:5000")
    print("=" * 45)
    app.run(debug=True, port=5000)
