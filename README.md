# reasoning-exchange-node
Minimal implementation of a reasoning exchange protocol. Receive structured AI reasoning → validate → decide ADMIT or REJECT locally.
# 🧩 Reasoning Exchange Node (Minimal)

This is a minimal implementation of a reasoning exchange protocol.

It allows systems to:
- receive structured reasoning
- evaluate it locally
- return ADMIT or REJECT

---

## 🚀 Run

```bash
pip install -r requirements.txt
python app.py
.

✅ CLEAN FINAL REPO CONTENT
📄 README.md (use this EXACT version)
# 🧩 Reasoning Exchange Node (Minimal)

Minimal implementation of a reasoning exchange protocol.

Receive structured AI reasoning → validate → decide ADMIT or REJECT locally.

---

## 🚀 Run

```bash
pip install -r requirements.txt
python app.py
📡 Test
curl -X POST http://localhost:5000/api/reasoning/evaluate \
  -H "Content-Type: application/json" \
  -d @example_request.json
🧠 What this does

Other systems can send reasoning.

This system decides whether to trust it.

⚖️ Design Principles
No shared truth
No central authority
Each system enforces its own rules
Rejection is normal
🔌 Endpoint

POST /api/reasoning/evaluate

Returns:

{
  "status": "ADMIT | REJECT"
}
🧪 Optional Demo

Run:

python send_test.py

Simulates another system sending reasoning.


---

## 📄 `requirements.txt`

```txt
flask
requests
🧩 protocol.py
import json

MAX_SIZE = 10000

def validate_packet(raw_data):
    if len(raw_data) > MAX_SIZE:
        return False, "size_limit"

    try:
        packet = json.loads(raw_data)
    except:
        return False, "invalid_json"

    if packet.get("version") != "1.0":
        return False, "unsupported_version"

    if packet.get("type") != "reasoning_packet":
        return False, "unsupported_type"

    payload = packet.get("payload", {})

    if "claim" not in payload or "reasoning" not in payload:
        return False, "invalid_payload"

    return True, packet
⚖️ governance.py
def evaluate(packet):
    payload = packet["payload"]

    claim = payload.get("claim", "")
    confidence = payload.get("confidence", 0)

    if confidence > 0.7 and len(claim) > 5:
        return "ADMIT"

    return "REJECT"
🌐 app.py
from flask import Flask, request, jsonify
from protocol import validate_packet
from governance import evaluate

app = Flask(__name__)

@app.route("/api/reasoning/evaluate", methods=["POST"])
def evaluate_reasoning():
    raw = request.data.decode("utf-8")

    valid, result = validate_packet(raw)

    if not valid:
        return jsonify({
            "status": "REJECT",
            "reason": result
        }), 400

    decision = evaluate(result)

    return jsonify({
        "status": decision
    })

if __name__ == "__main__":
    app.run(port=5000)
📄 example_request.json
{
  "version": "1.0",
  "type": "reasoning_packet",
  "payload": {
    "claim": "The sky is blue",
    "reasoning": "Rayleigh scattering",
    "confidence": 0.9
  }
}
📄 send_test.py
import requests
import json

with open("example_request.json") as f:
    data = json.load(f)

res = requests.post(
    "http://localhost:5000/api/reasoning/evaluate",
    json=data
)

print(res.json())
🚀 FINAL: GitHub STEPS (clean + simple)
1. Open terminal in your folder
cd reasoning-exchange-node
2. Init git
git init
git add .
git commit -m "Initial minimal reasoning exchange node"
3. Create repo

Go here:
👉 https://github.com/new

Name: reasoning-exchange-node
Public ✅
No README ❌
4. Connect repo
git remote add origin https://github.com/YOURNAME/reasoning-exchange-node.git
5. Push
git branch -M main
git push -u origin main
