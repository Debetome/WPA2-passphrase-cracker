from dataclasses import dataclass, field
from typing import Dict, Any

from hcracker.enums import Eapol

@dataclass
class Iteration:
    iteration: Any = None
    length: int = 10

@dataclass
class Target:
    ssid: str = field(default_factory=str)
    ap_mac: bytes = field(default_factory=bytes)
    sta_mac: bytes = field(default_factory=bytes)
    anonce: bytes = field(default_factory=bytes)
    snonce: bytes = field(default_factory=bytes)
    mic: bytes = field(default_factory=bytes)

@dataclass
class Attack:
    iterations: Dict[str, Iteration] = field(default_factory=dict)
    eapols: Dict[Eapol, bytes] = field(default_factory=dict)  # Here will be saved eapol messages 1 and 2 as bytes
    target: Target = None
