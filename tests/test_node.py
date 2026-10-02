"""Tests for the reasoning exchange node."""

import json
import unittest

from governance import evaluate
from protocol import validate_packet


def make_packet(**overrides):
    base = {
        "claim": "The sky is blue",
        "reasoning": "Rayleigh scattering",
        "confidence": 0.9,
    }
    if "payload" in overrides:
        base = overrides["payload"]
    return {
        "version": "1.0",
        "type": "reasoning_packet",
        "payload": base,
        **overrides.get("extra", {}),
    }


def dumps(obj):
    return json.dumps(obj)


class TestProtocolValidation(unittest.TestCase):
    def test_valid_packet_passes(self):
        valid, result = validate_packet(dumps(make_packet()))
        self.assertTrue(valid)
        self.assertEqual(result["payload"]["claim"], "The sky is blue")

    def test_invalid_json_rejected(self):
        valid, reason = validate_packet("{not json")
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_json")

    def test_non_object_root_rejected(self):
        valid, reason = validate_packet(dumps([1, 2, 3]))
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_json")

    def test_wrong_version_rejected(self):
        valid, reason = validate_packet(dumps(make_packet(extra={"version": "2.0"})))
        self.assertFalse(valid)
        self.assertEqual(reason, "unsupported_version")

    def test_wrong_type_rejected(self):
        valid, reason = validate_packet(dumps(make_packet(extra={"type": "other"})))
        self.assertFalse(valid)
        self.assertEqual(reason, "unsupported_type")

    def test_missing_payload_rejected(self):
        valid, reason = validate_packet(dumps({"version": "1.0", "type": "reasoning_packet"}))
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_payload")

    def test_payload_not_object_rejected(self):
        valid, reason = validate_packet(
            dumps({"version": "1.0", "type": "reasoning_packet", "payload": []})
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_payload")

    def test_missing_claim_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"reasoning": "x", "confidence": 0.9}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_claim")

    def test_blank_claim_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": "   ", "reasoning": "r", "confidence": 0.9}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_claim")

    def test_claim_not_string_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": 42, "reasoning": "r", "confidence": 0.9}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_claim")

    def test_claim_too_long_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": "x" * 3000, "reasoning": "r", "confidence": 0.9}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "claim_too_long")

    def test_missing_reasoning_rejected(self):
        valid, reason = validate_packet(dumps(make_packet(payload={"claim": "claim!", "confidence": 0.9})))
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_reasoning")

    def test_confidence_not_number_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": "claim!", "reasoning": "r", "confidence": "0.9"}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_confidence")

    def test_boolean_confidence_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": "claim!", "reasoning": "r", "confidence": True}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "invalid_confidence")

    def test_confidence_out_of_range_rejected(self):
        valid, reason = validate_packet(
            dumps(make_packet(payload={"claim": "claim!", "reasoning": "r", "confidence": 1.5}))
        )
        self.assertFalse(valid)
        self.assertEqual(reason, "confidence_out_of_range")

    def test_oversized_packet_rejected(self):
        packet = make_packet(payload={"claim": "x" * 11000, "reasoning": "r", "confidence": 0.9})
        valid, reason = validate_packet(dumps(packet))
        self.assertFalse(valid)
        self.assertEqual(reason, "size_limit")

    def test_deeply_nested_payload_rejected(self):
        packet = make_packet()
        node = packet["payload"].setdefault("meta", {})
        for _ in range(20):
            node["next"] = {}
            node = node["next"]
        valid, reason = validate_packet(dumps(packet))
        self.assertFalse(valid)
        self.assertEqual(reason, "payload_too_deep")


class TestGovernance(unittest.TestCase):
    def test_high_confidence_long_claim_admitted(self):
        decision, reason = evaluate(make_packet())
        self.assertEqual(decision, "ADMIT")
        self.assertIsNone(reason)

    def test_low_confidence_rejected(self):
        decision, reason = evaluate(make_packet(payload={"confidence": 0.5}))
        self.assertEqual(decision, "REJECT")
        self.assertEqual(reason, "local_policy")

    def test_short_claim_rejected(self):
        decision, reason = evaluate(make_packet(payload={"claim": "hi", "confidence": 0.9}))
        self.assertEqual(decision, "REJECT")
        self.assertEqual(reason, "local_policy")


if __name__ == "__main__":
    unittest.main()
