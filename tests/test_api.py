"""HTTP API integration tests using Flask's test client."""

import json
import unittest

from app import app


def make_packet(**overrides):
    base = {
        "claim": "The sky is blue",
        "reasoning": "Rayleigh scattering",
        "confidence": 0.9,
    }
    if "payload" in overrides:
        base = overrides["payload"]
    return {"version": "1.0", "type": "reasoning_packet", "payload": base}


class TestEvaluateEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_valid_packet_returns_admit(self):
        res = self.client.post("/api/reasoning/evaluate", json=make_packet())
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ADMIT")

    def test_low_confidence_policy_reject(self):
        res = self.client.post(
            "/api/reasoning/evaluate",
            json=make_packet(
                payload={
                    "claim": "The sky is blue",
                    "reasoning": "Rayleigh scattering",
                    "confidence": 0.5,
                }
            ),
        )
        self.assertEqual(res.status_code, 200)
        body = res.get_json()
        self.assertEqual(body["status"], "REJECT")
        self.assertEqual(body["reason"], "local_policy")

    def test_invalid_json_returns_400(self):
        res = self.client.post(
            "/api/reasoning/evaluate",
            data="{broken",
            content_type="application/json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["reason"], "invalid_json")

    def test_bad_version_returns_400(self):
        res = self.client.post("/api/reasoning/evaluate", json={"version": "9.9"})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()["reason"], "unsupported_version")

    def test_get_method_not_allowed(self):
        res = self.client.get("/api/reasoning/evaluate")
        self.assertEqual(res.status_code, 405)

    def test_health_endpoint(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")


if __name__ == "__main__":
    unittest.main()
