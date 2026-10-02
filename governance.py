"""Local admission policy.

ADMIT means only that the packet passed this node's structural and local
policy checks. It is not a truth judgement: confidence is self-reported.
"""


def evaluate(packet):
    payload = packet["payload"]

    claim = payload.get("claim", "")
    confidence = payload.get("confidence", 0)

    if confidence > 0.7 and len(claim) > 5:
        return "ADMIT", None

    return "REJECT", "local_policy"
