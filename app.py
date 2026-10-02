"""Reasoning Exchange Node — receive, validate, decide ADMIT or REJECT."""

from flask import Flask, jsonify, request

from governance import evaluate
from protocol import MAX_SIZE, validate_packet

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_SIZE


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"status": "REJECT", "reason": "size_limit"}), 413


@app.errorhandler(400)
def bad_request(_error):
    return jsonify({"status": "REJECT", "reason": "invalid_json"}), 400


@app.errorhandler(500)
def internal_error(_error):
    return jsonify({"status": "REJECT", "reason": "internal_error"}), 500


@app.route("/api/reasoning/evaluate", methods=["POST"])
def evaluate_reasoning():
    raw = request.get_data(cache=False, as_text=True)

    valid, result = validate_packet(raw)

    if not valid:
        return jsonify({"status": "REJECT", "reason": result}), 400

    decision, reason = evaluate(result)

    return jsonify({"status": decision, "reason": reason})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(port=5000)
