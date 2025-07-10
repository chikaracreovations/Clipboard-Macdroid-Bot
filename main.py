from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")  # Secure via Railway env vars

def call_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324",
        "messages": [
            {
                "role": "system",
                "content": "You are a grammar corrector. ONLY return the corrected version of the sentence, with no explanation, no formatting, and no introduction. Just output the fixed sentence only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}\n{response.text}"

@app.route('/fix', methods=['POST'])
def fix_text():
    content = request.get_json()
    text = content.get('text', '')
    if not text:
        return jsonify({"error": "Missing 'text' field in request"}), 400
    fixed = call_openrouter(text)
    return jsonify({"fixed": fixed})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
