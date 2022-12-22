from itertools import permutations
from string import ascii_lowercase, digits
from typing import Dict

from hcracker.enums import Eapol
from hcracker.models import (
    Attack,
    Target,
    Iteration
)

class AttackBuilder(Attack):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def set_iterations(self, iterations: Dict[str, Iteration] = None) -> None:
        if not iterations:
            self.iterations = iterations
            return None

        charsets = {}
        charsets["lowercase"] = ascii_lowercase
        charsets["digits"] = digits
        charsets["lowercase_digits"] = ascii_lowercase + digits

        for key, charset in charsets.items():
            self.iterations[key] = Iteration()
            self.iterations[key].iteration = permutations(charset, self.iterations[key].length)

    def set_eapols(self, eapols: Dict[Eapol, str]) -> None:
        for key, value in eapols.items():
            self.eapols[key] = open(value, "rb").read()

    def set_target(self) -> None:
        self.target = Target()

        self.target.ssid = None
        self.target.ap_mac = self.eapols[Eapol.EAPOL1][10:16]
        self.target.sta_mac = self.eapols[Eapol.EAPOL2][10:16]
        self.target.anonce = self.eapols[Eapol.EAPOL1][51:83]
        self.target.snonce = self.eapols[Eapol.EAPOL2][51:83]
        self.target.mic = self.eapols[Eapol.EAPOL2][34:][81:97]
