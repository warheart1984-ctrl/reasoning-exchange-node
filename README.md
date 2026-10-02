# 🧩 Reasoning Exchange Node (Minimal)

Minimal implementation of a reasoning exchange protocol.

Receive structured AI reasoning → validate → decide ADMIT or REJECT locally.

> **What ADMIT means here:** the packet is well-formed and passed this node's
> local policy. It is **not** a truth judgement — `confidence` is
> self-reported by the sender and the reasoning text is not verified.

---

## 🚀 Run

```bash
pip install -r requirements.txt
python app.py
```

## 📡 Test

```bash
curl -X POST http://localhost:5000/api/reasoning/evaluate \
  -H "Content-Type: application/json" \
  -d @example_request.json
```

Response:

```json
{
  "status": "ADMIT"
}
```

Rejects return HTTP 400 with a `reason` field, e.g.
`REJECT / invalid_json`, `unsupported_version`, `confidence_out_of_range`,
or `local_policy`.

## 🧪 Demo sender

```bash
python send_test.py
```

Simulates another system sending reasoning to the node.

## 🔌 Endpoint

`POST /api/reasoning/evaluate` → `{ "status": "ADMIT | REJECT" }`

`GET /health` → `{ "status": "ok" }`

## 📦 Packet format

```json
{
  "version": "1.0",
  "type": "reasoning_packet",
  "payload": {
    "claim": "The sky is blue",
    "reasoning": "Rayleigh scattering",
    "confidence": 0.9
  }
}
```

Limits enforced by the node:

| Rule | Value |
| --- | --- |
| Max packet size | 10 000 bytes |
| Max claim length | 2 000 chars |
| Max reasoning length | 5 000 chars |
| Confidence range | 0.0 – 1.0 |
| Max nesting depth | 8 |

## ⚖️ Design Principles

- No shared truth
- No central authority
- Each system enforces its own rules
- Rejection is normal
- ADMIT ≠ truth

## 🧠 What this does

- Other systems send structured reasoning.
- This system validates the packet structure locally, then applies its own
  admission policy (currently: confidence > 0.7 and a meaningful claim).
- It returns its own decision. It trusts nothing by default.

## 🧯 Run tests

```bash
python -m unittest discover tests -v
```

## 📄 License

Apache-2.0
