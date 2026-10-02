"""Send a reasoning packet to a running node, simulating another system."""

import json

import requests

URL = "http://localhost:5000/api/reasoning/evaluate"


def main():
    with open("example_request.json", encoding="utf-8") as f:
        data = json.load(f)

    try:
        res = requests.post(URL, json=data, timeout=5)
        print(f"HTTP {res.status_code}: {res.json()}")
    except requests.ConnectionError:
        print("Could not connect. Is the node running? Start it with: python app.py")


if __name__ == "__main__":
    main()
