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

📁 2. Full Minimal Repo (copy exactly)
📄 README.md
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

---

## 📄 `requirements.txt`

```txt
flask
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
🔥 3. OPTIONAL (but powerful): 2-node demo

Create another file:

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

👉 Add to requirements:

requests

Now people can run:

python send_test.py

That makes it feel like:

“another system sent this”

🧠 4. Step-by-step: Put on GitHub
🟢 Step 1 — Create folder
mkdir reasoning-exchange-node
cd reasoning-exchange-node
🟢 Step 2 — Create files

Paste everything above into:

README.md
app.py
protocol.py
governance.py
requirements.txt
example_request.json

(optional: send_test.py)

🟢 Step 3 — Init git
git init
🟢 Step 4 — Add files
git add .
🟢 Step 5 — First commit
git commit -m "Initial minimal reasoning exchange node"
🟢 Step 6 — Create repo on GitHub

Go to:
👉 https://github.com/new

Name: reasoning-exchange-node
Public ✅
DO NOT add README (you already have one)
🟢 Step 7 — Link repo

GitHub will show something like:

git remote add origin https://github.com/YOURNAME/reasoning-exchange-node.git

Run that.

🟢 Step 8 — Push
git branch -M main
git push -u origin main
