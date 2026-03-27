"""
Loaders for real-world IDS datasets: CICIDS2017 and UNSW-NB15.

Expects CSV files in data/raw/ (or paths set via env). Handles
noisy/incomplete data with safe parsing and optional sampling.
"""

import csv
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

from app.core.logging import get_logger
from app.data.features import FEATURE_NAMES, flow_to_features

logger = get_logger(__name__)

# -----------------------------------------------------------------------------
# CICIDS 2017 – column mapping (example; adjust to your CSV headers)
# See: https://www.unb.ca/cic/datasets/ids-2017.html
# -----------------------------------------------------------------------------
CICIDS_COLUMNS = [
    "dst_port",
    "protocol",
    "flow_duration",
    "tot_fwd_pkts",
    "tot_bwd_pkts",
    "tot_len_fwd_pkts",
    "tot_len_bwd_pkts",
    "label",
]
# Optional: map label to our attack_type
CICIDS_LABEL_MAP = {
    "BENIGN": "benign",
    "DoS Hulk": "dos",
    "DoS GoldenEye": "dos",
    "DoS Slowhttptest": "dos",
    "DoS slowloris": "dos",
    "Heartbleed": "web_attack",
    "Web Attack – Brute Force": "web_attack",
    "Web Attack – XSS": "web_attack",
    "Web Attack – Sql Injection": "web_attack",
    "Infiltration": "infiltration",
    "Bot": "botnet",
    "PortScan": "port_scan",
    "DDoS": "ddos",
    "FTP-Patator": "brute_force",
    "SSH-Patator": "brute_force",
}


def _read_csv_rows(
    path: str,
    delimiter: str = ",",
    max_rows: Optional[int] = None,
    skip_errors: bool = True,
) -> Generator[Dict[str, str], None, None]:
    """Yield rows as dicts; skip malformed rows if skip_errors."""
    path_obj = Path(path)
    if not path_obj.exists():
        logger.warning("Dataset file not found: %s", path)
        return
    with open(path_obj, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        headers = reader.fieldnames or []
        for i, row in enumerate(reader):
            if max_rows is not None and i >= max_rows:
                break
            if not row or not any(str(v).strip() for v in row.values()):
                if skip_errors:
                    continue
            yield row


def parse_cicids_row(row: Dict[str, str]) -> Optional[Tuple[Dict[str, float], str]]:
    """
    Parse one CICIDS-style row into (feature_dict, label).
    Returns None if row cannot be parsed (noisy data).
    """
    try:
        # Adapt keys to your actual CICIDS CSV; these are common names
        duration = float(row.get("flow_duration", 0) or 0)
        if duration < 0:
            duration = 0
        tot_fwd = int(float(row.get("tot_fwd_pkts", 0) or 0))
        tot_bwd = int(float(row.get("tot_bwd_pkts", 0) or 0))
        len_fwd = int(float(row.get("tot_len_fwd_pkts", 0) or 0))
        len_bwd = int(float(row.get("tot_len_bwd_pkts", 0) or 0))
        dst_port = int(float(row.get("dst_port", 0) or 0))
        proto = str(row.get("protocol", "TCP")).upper()
        if proto not in ("TCP", "UDP", "ICMP"):
            proto = "TCP"
        label = str(row.get("label", "BENIGN")).strip()
    except (ValueError, TypeError) as e:
        logger.debug("Skip CICIDS row %s: %s", row, e)
        return None

    features = flow_to_features(
        src_ip="0.0.0.0",
        dst_ip="0.0.0.0",
        src_port=0,
        dst_port=dst_port,
        protocol=proto,
        bytes_sent=len_fwd,
        bytes_received=len_bwd,
        packets_sent=tot_fwd,
        packets_received=tot_bwd,
        duration_sec=duration if duration > 0 else 1.0,
    )
    attack_type = CICIDS_LABEL_MAP.get(label, "unknown" if label != "BENIGN" else "benign")
    return features, attack_type


def load_cicids_csv(
    path: str,
    max_rows: Optional[int] = None,
) -> Generator[Tuple[Dict[str, float], str], None, None]:
    """
    Yield (features dict, attack_type) from a CICIDS2017-style CSV.

    Path can be set via env CICIDS_CSV or passed explicitly.
    """
    for row in _read_csv_rows(path, max_rows=max_rows):
        parsed = parse_cicids_row(row)
        if parsed:
            yield parsed


def parse_unsw_row(row: Dict[str, str]) -> Optional[Tuple[Dict[str, float], str]]:
    """
    Parse one UNSW-NB15-style row into (feature_dict, label).
    UNSW uses attack_cat (category) and label (0/1).
    """
    try:
        # UNSW-NB15 column names vary; adjust to your file
        duration = float(row.get("dur", 0) or row.get("duration", 0) or 0)
        if duration < 0:
            duration = 0
        spkts = int(float(row.get("spkts", 0) or 0))
        dpkts = int(float(row.get("dpkts", 0) or 0))
        sbytes = int(float(row.get("sbytes", 0) or 0))
        dbytes = int(float(row.get("dbytes", 0) or 0))
        sport = int(float(row.get("sport", 0) or 0))
        dport = int(float(row.get("dport", 0) or 0))
        proto = str(row.get("proto", "tcp")).upper()
        if proto not in ("TCP", "UDP", "ICMP"):
            proto = "TCP"
        label = str(row.get("label", "0")).strip()
        attack_cat = str(row.get("attack_cat", "")).strip()
    except (ValueError, TypeError) as e:
        logger.debug("Skip UNSW row: %s", e)
        return None

    features = flow_to_features(
        src_ip="0.0.0.0",
        dst_ip="0.0.0.0",
        src_port=sport,
        dst_port=dport,
        protocol=proto,
        bytes_sent=sbytes,
        bytes_received=dbytes,
        packets_sent=spkts,
        packets_received=dpkts,
        duration_sec=duration if duration > 0 else 1.0,
    )
    if label == "1" or label == "1.0":
        attack_type = attack_cat if attack_cat else "malicious"
        # Normalize known UNSW categories
        if "DoS" in attack_type or "DoS" in attack_cat:
            attack_type = "dos"
        elif "Recon" in attack_type or "Scan" in attack_type:
            attack_type = "port_scan"
        elif "Fuzz" in attack_type:
            attack_type = "web_attack"
        elif "Backdoor" in attack_type or "Shellcode" in attack_type:
            attack_type = "botnet"
        elif "Exploit" in attack_type or "Analysis" in attack_type:
            attack_type = "exploit"
    else:
        attack_type = "benign"
    return features, attack_type


def load_unsw_csv(
    path: str,
    max_rows: Optional[int] = None,
) -> Generator[Tuple[Dict[str, float], str], None, None]:
    """
    Yield (features dict, attack_type) from a UNSW-NB15-style CSV.
    """
    for row in _read_csv_rows(path, max_rows=max_rows):
        parsed = parse_unsw_row(row)
        if parsed:
            yield parsed


# -----------------------------------------------------------------------------
# NSL-KDD – column mapping (KDD Cup 99 style)
# -----------------------------------------------------------------------------
NSLKDD_LABEL_MAP = {
    "normal": "benign",
    "back": "botnet",
    "buffer_overflow": "exploit",
    "ftp_write": "exploit",
    "guess_passwd": "brute_force",
    "imap": "exploit",
    "ipsweep": "port_scan",
    "land": "dos",
    "loadmodule": "exploit",
    "multihop": "infiltration",
    "neptune": "dos",
    "nmap": "port_scan",
    "perl": "exploit",
    "phf": "web_attack",
    "pod": "dos",
    "portsweep": "port_scan",
    "rootkit": "exploit",
    "satan": "port_scan",
    "smurf": "dos",
    "spy": "data_exfiltration",
    "teardrop": "dos",
    "warezclient": "botnet",
    "warezmaster": "exploit",
}


def parse_nslkdd_row(row: Dict[str, str]) -> Optional[Tuple[Dict[str, float], str]]:
    """Parse one NSL-KDD row into (feature_dict, attack_type)."""
    try:
        duration = float(row.get("duration", 0) or 0)
        if duration < 0:
            duration = 0
        src_bytes = int(float(row.get("src_bytes", 0) or 0))
        dst_bytes = int(float(row.get("dst_bytes", 0) or 0))
        protocol = str(row.get("protocol_type", "tcp")).upper()
        if protocol not in ("TCP", "UDP", "ICMP"):
            protocol = "TCP"
        sport = int(float(row.get("src_port", 0) or row.get("sport", 0) or 0))
        dport = int(float(row.get("dst_port", 0) or row.get("dport", 0) or 0))
        label = str(row.get("label", "normal")).strip().lower()
        # NSL-KDD has 41 features; we map to flow-level
        tot_fwd = int(float(row.get("count", 0) or row.get("wrong_fragment", 0) or 0)) + 1
        tot_bwd = int(float(row.get("serror_rate", 0) or 0)) + 1
        tot_fwd = max(1, tot_fwd)
        tot_bwd = max(1, tot_bwd)
        features = flow_to_features(
            src_ip="0.0.0.0",
            dst_ip="0.0.0.0",
            src_port=sport,
            dst_port=dport,
            protocol=protocol,
            bytes_sent=src_bytes,
            bytes_received=dst_bytes,
            packets_sent=tot_fwd,
            packets_received=tot_bwd,
            duration_sec=duration if duration > 0 else 1.0,
        )
        attack_type = NSLKDD_LABEL_MAP.get(label, "unknown" if label != "normal" else "benign")
        return features, attack_type
    except (ValueError, TypeError) as e:
        logger.debug("Skip NSL-KDD row: %s", e)
        return None


def load_nslkdd_csv(
    path: str,
    max_rows: Optional[int] = None,
) -> Generator[Tuple[Dict[str, float], str], None, None]:
    """Yield (features dict, attack_type) from NSL-KDD-style CSV."""
    for row in _read_csv_rows(path, max_rows=max_rows):
        parsed = parse_nslkdd_row(row)
        if parsed:
            yield parsed


# -----------------------------------------------------------------------------
# CIC-IDS2018 – similar to CIC-IDS2017, different column names possible
# -----------------------------------------------------------------------------
CICIDS2018_LABEL_MAP = {
    **CICIDS_LABEL_MAP,
    "Benign": "benign",
    "Bot": "botnet",
    "DDoS attacks-HOIC": "ddos",
    "DDoS attacks-LOIC-UDP": "ddos",
    "DoS attacks-Hulk": "dos",
    "DoS attacks-SlowHTTPTest": "dos",
    "FTP-BruteForce": "brute_force",
    "SSH-BruteForce": "brute_force",
    "Infiltration": "infiltration",
    "SQL Injection": "web_attack",
    "Brute Force -Web": "web_attack",
    "Brute Force -XSS": "web_attack",
}


def parse_cicids2018_row(row: Dict[str, str]) -> Optional[Tuple[Dict[str, float], str]]:
    """Parse CIC-IDS2018 row; fallback to CICIDS column names."""
    try:
        duration = float(
            row.get("Flow Duration", 0) or row.get("flow_duration", 0) or 0
        )
        if duration < 0:
            duration = 0
        tot_fwd = int(float(row.get("Total Fwd Packets", 0) or row.get("tot_fwd_pkts", 0) or 0))
        tot_bwd = int(float(row.get("Total Bwd Packets", 0) or row.get("tot_bwd_pkts", 0) or 0))
        len_fwd = int(float(row.get("Total Length of Fwd Packets", 0) or row.get("tot_len_fwd_pkts", 0) or 0))
        len_bwd = int(float(row.get("Total Length of Bwd Packets", 0) or row.get("tot_len_bwd_pkts", 0) or 0))
        dst_port = int(float(row.get("Destination Port", 0) or row.get("dst_port", 0) or 0))
        proto = str(row.get("Protocol", 0) or row.get("protocol", "TCP")).upper()
        if proto not in ("TCP", "UDP", "ICMP"):
            proto = "TCP"
        label = str(row.get("Label", "") or row.get("label", "BENIGN")).strip()
        features = flow_to_features(
            src_ip="0.0.0.0",
            dst_ip="0.0.0.0",
            src_port=0,
            dst_port=dst_port,
            protocol=proto,
            bytes_sent=len_fwd,
            bytes_received=len_bwd,
            packets_sent=tot_fwd,
            packets_received=tot_bwd,
            duration_sec=duration if duration > 0 else 1.0,
        )
        attack_type = CICIDS2018_LABEL_MAP.get(label, "unknown" if label and label.upper() != "BENIGN" else "benign")
        return features, attack_type
    except (ValueError, TypeError) as e:
        logger.debug("Skip CIC-IDS2018 row: %s", e)
        return None


def load_cicids2018_csv(
    path: str,
    max_rows: Optional[int] = None,
) -> Generator[Tuple[Dict[str, float], str], None, None]:
    """Yield (features dict, attack_type) from CIC-IDS2018 CSV."""
    for row in _read_csv_rows(path, max_rows=max_rows):
        parsed = parse_cicids2018_row(row)
        if parsed:
            yield parsed


# -----------------------------------------------------------------------------
# BoT-IoT – UNSW BoT-IoT dataset
# -----------------------------------------------------------------------------
BOTIOT_LABEL_MAP = {
    "Normal": "benign",
    "Benign": "benign",
    "DDoS": "ddos",
    "DoS": "dos",
    "Reconnaissance": "port_scan",
    "Theft": "data_exfiltration",
}


def parse_botiot_row(row: Dict[str, str]) -> Optional[Tuple[Dict[str, float], str]]:
    """Parse BoT-IoT CSV row (column names vary)."""
    try:
        duration = float(row.get("duration", 0) or row.get("dur", 0) or 0)
        if duration < 0:
            duration = 0
        sbytes = int(float(row.get("sbytes", 0) or row.get("src_bytes", 0) or 0))
        dbytes = int(float(row.get("dbytes", 0) or row.get("dst_bytes", 0) or 0))
        spkts = int(float(row.get("spkts", 0) or row.get("pkts_sent", 0) or 0))
        dpkts = int(float(row.get("dpkts", 0) or row.get("pkts_received", 0) or 0))
        sport = int(float(row.get("sport", 0) or row.get("src_port", 0) or 0))
        dport = int(float(row.get("dport", 0) or row.get("dst_port", 0) or 0))
        proto = str(row.get("proto", "tcp") or row.get("protocol", "tcp")).upper()
        if proto not in ("TCP", "UDP", "ICMP"):
            proto = "TCP"
        label = str(row.get("label", "") or row.get("attack", "Normal")).strip()
        features = flow_to_features(
            src_ip="0.0.0.0",
            dst_ip="0.0.0.0",
            src_port=sport,
            dst_port=dport,
            protocol=proto,
            bytes_sent=sbytes,
            bytes_received=dbytes,
            packets_sent=spkts,
            packets_received=dpkts,
            duration_sec=duration if duration > 0 else 1.0,
        )
        attack_type = BOTIOT_LABEL_MAP.get(label, "unknown" if label and label != "Normal" else "benign")
        return features, attack_type
    except (ValueError, TypeError) as e:
        logger.debug("Skip BoT-IoT row: %s", e)
        return None


def load_botiot_csv(
    path: str,
    max_rows: Optional[int] = None,
) -> Generator[Tuple[Dict[str, float], str], None, None]:
    """Yield (features dict, attack_type) from BoT-IoT CSV."""
    for row in _read_csv_rows(path, max_rows=max_rows):
        parsed = parse_botiot_row(row)
        if parsed:
            yield parsed


def get_dataset_path(name: str) -> Optional[str]:
    """
    Return path for dataset CSV. Checks env and data/raw/.
    Supports: cicids, unsw, nsl_kdd, cicids2018, botiot.
    """
    name_lower = name.lower().replace("-", "_")
    env_map = {
        "cicids": "CICIDS_CSV",
        "cicids2017": "CICIDS_CSV",
        "unsw": "UNSW_CSV",
        "nsl_kdd": "NSLKDD_CSV",
        "nslkdd": "NSLKDD_CSV",
        "cicids2018": "CICIDS2018_CSV",
        "botiot": "BOTIOT_CSV",
        "bot_iot": "BOTIOT_CSV",
    }
    env_key = env_map.get(name_lower)
    if env_key:
        path = os.getenv(env_key)
        if path and os.path.isfile(path):
            return path
    base = Path(__file__).resolve().parent.parent.parent
    for sub in ("data/raw", "data"):
        candidate = base / sub
        if not candidate.exists():
            continue
        if name_lower in ("cicids", "cicids2017"):
            for f in candidate.glob("*.csv"):
                if "CICIDS" in f.name or "cicids" in f.name:
                    return str(f)
        if name_lower == "unsw":
            for f in candidate.glob("UNSW*.csv"):
                return str(f)
        if name_lower in ("nsl_kdd", "nslkdd"):
            for f in candidate.glob("*.csv"):
                if "KDD" in f.name or "nsl" in f.name.lower():
                    return str(f)
        if name_lower == "cicids2018":
            for f in candidate.glob("*.csv"):
                if "2018" in f.name:
                    return str(f)
        if name_lower in ("botiot", "bot_iot"):
            for f in candidate.glob("*.csv"):
                if "Bot" in f.name or "bot" in f.name or "IoT" in f.name:
                    return str(f)
    return None
