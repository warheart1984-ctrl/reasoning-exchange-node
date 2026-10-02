"""Packet parsing and structural validation for the reasoning exchange protocol."""

import json

MAX_SIZE = 10000
SUPPORTED_VERSION = "1.0"
SUPPORTED_TYPE = "reasoning_packet"
MAX_DEPTH = 8
MAX_CLAIM_LENGTH = 2000
MAX_REASONING_LENGTH = 5000

CONFIDENCE_MIN = 0.0
CONFIDENCE_MAX = 1.0


def _check_depth(value, depth=0):
    if depth > MAX_DEPTH:
        return False
    if isinstance(value, dict):
        return all(_check_depth(v, depth + 1) for v in value.values())
    if isinstance(value, list):
        return all(_check_depth(v, depth + 1) for v in value)
    return True


def validate_packet(raw_data):
    if len(raw_data) > MAX_SIZE:
        return False, "size_limit"

    try:
        packet = json.loads(raw_data)
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        return False, "invalid_json"

    if not isinstance(packet, dict):
        return False, "invalid_json"

    if packet.get("version") != SUPPORTED_VERSION:
        return False, "unsupported_version"

    if packet.get("type") != SUPPORTED_TYPE:
        return False, "unsupported_type"

    payload = packet.get("payload")

    if not isinstance(payload, dict):
        return False, "invalid_payload"

    if not _check_depth(packet):
        return False, "payload_too_deep"

    claim = payload.get("claim")
    if not isinstance(claim, str) or not claim.strip():
        return False, "invalid_claim"

    if len(claim) > MAX_CLAIM_LENGTH:
        return False, "claim_too_long"

    reasoning = payload.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        return False, "invalid_reasoning"

    if len(reasoning) > MAX_REASONING_LENGTH:
        return False, "reasoning_too_long"

    confidence = payload.get("confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool):
        return False, "invalid_confidence"

    if not (CONFIDENCE_MIN <= confidence <= CONFIDENCE_MAX):
        return False, "confidence_out_of_range"

    return True, packet
