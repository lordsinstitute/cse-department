"""
PCAP file ingestion for offline analysis.

Reads pcap/pcapng and aggregates packets into flow-like records with
feature extraction. Requires scapy or dpkt (optional dependency).
"""

import socket
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple

from app.core.logging import get_logger
from app.data.features import flow_to_features

logger = get_logger(__name__)


def _ip_to_str(ip_bytes: bytes) -> str:
    """Convert 4-byte IPv4 address to string."""
    try:
        return socket.inet_ntoa(ip_bytes)
    except (OSError, TypeError):
        return "0.0.0.0"

try:
    import scapy.all as scapy
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

try:
    import dpkt
    HAS_DPKT = True
except ImportError:
    HAS_DPKT = False


def _flow_key(
    src_ip: str,
    dst_ip: str,
    src_port: int,
    dst_port: int,
    protocol: str,
) -> Tuple[str, str, int, int, str]:
    """Canonical key for a flow (normalize direction)."""
    if (src_ip, src_port) > (dst_ip, dst_port):
        return dst_ip, src_ip, dst_port, src_port, protocol
    return src_ip, dst_ip, src_port, dst_port, protocol


def flows_from_pcap_scapy(
    pcap_path: str,
    max_packets: Optional[int] = None,
) -> Generator[Dict[str, Any], None, None]:
    """
    Aggregate PCAP into flow records using Scapy.

    Yields dicts with keys compatible with flow_to_features (src_ip, dst_ip,
    src_port, dst_port, protocol, bytes_sent, bytes_received, packets_sent,
    packets_received, duration_sec). Each flow is one direction (client->server
    bytes/packets vs server->client).
    """
    if not HAS_SCAPY:
        logger.warning("Scapy not installed; install with: pip install scapy")
        return

    path = Path(pcap_path)
    if not path.exists():
        logger.warning("PCAP file not found: %s", pcap_path)
        return

    flows: Dict[
        Tuple[str, str, int, int, str],
        Dict[str, Any],
    ] = {}
    count = 0

    try:
        for pkt in scapy.rdpcap(str(path)):
            if max_packets is not None and count >= max_packets:
                break
            count += 1

            if not pkt.haslayer("IP"):
                continue
            ip = pkt["IP"]
            src_ip = ip.src
            dst_ip = ip.dst
            proto = "OTHER"
            src_port = 0
            dst_port = 0
            length = len(pkt)

            if pkt.haslayer("TCP"):
                proto = "TCP"
                src_port = pkt["TCP"].sport
                dst_port = pkt["TCP"].dport
            elif pkt.haslayer("UDP"):
                proto = "UDP"
                src_port = pkt["UDP"].sport
                dst_port = pkt["UDP"].dport
            elif pkt.haslayer("ICMP"):
                proto = "ICMP"

            key = _flow_key(src_ip, dst_ip, src_port, dst_port, proto)
            if key not in flows:
                flows[key] = {
                    "src_ip": key[0],
                    "dst_ip": key[1],
                    "src_port": key[2],
                    "dst_port": key[3],
                    "protocol": key[4],
                    "bytes_sent": 0,
                    "bytes_received": 0,
                    "packets_sent": 0,
                    "packets_received": 0,
                    "start_time": None,
                    "end_time": None,
                }
            f = flows[key]
            # Direction: first packet direction as "sent"
            if (src_ip, src_port) == (key[0], key[2]):
                f["bytes_sent"] += length
                f["packets_sent"] += 1
            else:
                f["bytes_received"] += length
                f["packets_received"] += 1
            if f["start_time"] is None:
                f["start_time"] = pkt.time
            f["end_time"] = pkt.time

    except Exception as e:
        logger.exception("Error reading PCAP with Scapy: %s", e)
        return

    for rec in flows.values():
        start = rec.get("start_time")
        end = rec.get("end_time")
        duration = (end - start) if (start and end) else 1.0
        rec["duration_sec"] = max(0.0, duration)
        yield rec


def flows_from_pcap_dpkt(
    pcap_path: str,
    max_packets: Optional[int] = None,
) -> Generator[Dict[str, Any], None, None]:
    """
    Aggregate PCAP into flow records using dpkt.

    Yields same structure as flows_from_pcap_scapy.
    """
    if not HAS_DPKT:
        logger.warning("dpkt not installed; install with: pip install dpkt")
        return

    path = Path(pcap_path)
    if not path.exists():
        logger.warning("PCAP file not found: %s", pcap_path)
        return

    flows: Dict[Tuple[str, str, int, int, str], Dict[str, Any]] = {}
    count = 0

    try:
        with open(path, "rb") as f:
            pcap = dpkt.pcap.Reader(f)
            for ts, buf in pcap:
                if max_packets is not None and count >= max_packets:
                    break
                count += 1
                try:
                    eth = dpkt.ethernet.Ethernet(buf)
                    if not isinstance(eth.data, dpkt.ip.IP):
                        continue
                    ip = eth.data
                    src_ip = _ip_to_str(ip.src)
                    dst_ip = _ip_to_str(ip.dst)
                    proto = "OTHER"
                    src_port = 0
                    dst_port = 0
                    length = len(buf)

                    if isinstance(ip.data, dpkt.tcp.TCP):
                        proto = "TCP"
                        src_port = ip.data.sport
                        dst_port = ip.data.dport
                    elif isinstance(ip.data, dpkt.udp.UDP):
                        proto = "UDP"
                        src_port = ip.data.sport
                        dst_port = ip.data.dport
                    elif isinstance(ip.data, dpkt.icmp.ICMP):
                        proto = "ICMP"

                    key = _flow_key(src_ip, dst_ip, src_port, dst_port, proto)
                    if key not in flows:
                        flows[key] = {
                            "src_ip": key[0],
                            "dst_ip": key[1],
                            "src_port": key[2],
                            "dst_port": key[3],
                            "protocol": key[4],
                            "bytes_sent": 0,
                            "bytes_received": 0,
                            "packets_sent": 0,
                            "packets_received": 0,
                            "start_time": None,
                            "end_time": None,
                        }
                    f = flows[key]
                    if (src_ip, src_port) == (key[0], key[2]):
                        f["bytes_sent"] += length
                        f["packets_sent"] += 1
                    else:
                        f["bytes_received"] += length
                        f["packets_received"] += 1
                    if f["start_time"] is None:
                        f["start_time"] = ts
                    f["end_time"] = ts
                except (AttributeError, IndexError, dpkt.dpkt.UnpackError):
                    continue
    except Exception as e:
        logger.exception("Error reading PCAP with dpkt: %s", e)
        return

    for rec in flows.values():
        start = rec.get("start_time")
        end = rec.get("end_time")
        duration = (end - start) if (start and end) else 1.0
        rec["duration_sec"] = max(0.0, duration)
        yield rec


import socket  # noqa: E402


def flows_from_pcap(
    pcap_path: str,
    max_packets: Optional[int] = None,
    prefer: str = "scapy",
) -> Generator[Dict[str, Any], None, None]:
    """
    Read PCAP and yield flow-like records. Uses scapy or dpkt.

    Each yielded dict can be passed to flow_to_features() for ML input.
    """
    if prefer == "scapy" and HAS_SCAPY:
        yield from flows_from_pcap_scapy(pcap_path, max_packets)
    elif HAS_DPKT:
        yield from flows_from_pcap_dpkt(pcap_path, max_packets)
    elif HAS_SCAPY:
        yield from flows_from_pcap_scapy(pcap_path, max_packets)
    else:
        logger.warning("Install scapy or dpkt for PCAP support: pip install scapy")
