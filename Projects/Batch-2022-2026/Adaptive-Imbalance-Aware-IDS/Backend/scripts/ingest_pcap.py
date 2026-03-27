"""
Offline PCAP ingestion: read a PCAP file and POST flows to the NIDS ingest API.

Usage:
  python -m scripts.ingest_pcap --pcap capture.pcap --api http://127.0.0.1:9000 [--max-packets 50000]
"""

import argparse
import sys
import time

try:
    import requests
except ImportError:
    print("Install requests: pip install requests")
    sys.exit(1)

# Add backend to path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.pcap_ingest import flows_from_pcap
from app.data.features import flow_to_features


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pcap", required=True, help="Path to PCAP file")
    parser.add_argument("--api", default="http://127.0.0.1:9000", help="NIDS ingest base URL")
    parser.add_argument("--max-packets", type=int, default=None)
    parser.add_argument("--batch-delay", type=float, default=0.1)
    args = parser.parse_args()

    url = f"{args.api.rstrip('/')}/ingest/flow"
    count = 0
    errs = 0
    for flow in flows_from_pcap(args.pcap, max_packets=args.max_packets):
        payload = {
            "src_ip": flow["src_ip"],
            "dst_ip": flow["dst_ip"],
            "src_port": flow["src_port"],
            "dst_port": flow["dst_port"],
            "protocol": flow["protocol"],
            "bytes_sent": flow["bytes_sent"],
            "bytes_received": flow["bytes_received"],
            "packets_sent": flow["packets_sent"],
            "packets_received": flow["packets_received"],
        }
        try:
            r = requests.post(url, json=payload, timeout=5)
            if r.status_code == 200:
                count += 1
            else:
                errs += 1
        except Exception as e:
            errs += 1
            print("Error:", e)
        time.sleep(args.batch_delay)
    print(f"Posted {count} flows, {errs} errors")


if __name__ == "__main__":
    main()
