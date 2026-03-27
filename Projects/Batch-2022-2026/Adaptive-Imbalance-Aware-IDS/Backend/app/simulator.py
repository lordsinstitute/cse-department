import random
import time
from typing import Dict

import requests


def generate_flow() -> Dict:
    src_ip = f"10.0.0.{random.randint(1, 254)}"
    dst_ip = random.choice(
        ["192.168.1.10", "192.168.1.20", "203.0.113.5", "198.51.100.7"]
    )
    dst_port = random.choice([22, 23, 80, 443, 3389, 8080])
    src_port = random.randint(1024, 65535)

    # Sometimes generate "suspicious" flows
    if random.random() < 0.2:
        bytes_sent = random.randint(5_000_000, 20_000_000)
        packets_sent = random.randint(5_000, 15_000)
    else:
        bytes_sent = random.randint(500, 50_000)
        packets_sent = random.randint(10, 500)

    return {
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "protocol": "TCP",
        "bytes_sent": bytes_sent,
        "bytes_received": random.randint(0, bytes_sent),
        "packets_sent": packets_sent,
        "packets_received": random.randint(0, packets_sent),
    }


def main() -> None:
    url = "http://127.0.0.1:9000/ingest/flow"
    print(f"Sending synthetic flows to {url} (Ctrl+C to stop)...")
    while True:
        flow = generate_flow()
        try:
            resp = requests.post(url, json=flow, timeout=5)
            if resp.status_code != 200:
                print(f"Error {resp.status_code}: {resp.text}")
        except Exception as exc:
            print(f"Request failed: {exc}")
        time.sleep(0.5)


if __name__ == "__main__":
    main()

