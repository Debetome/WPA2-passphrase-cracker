import unittest
import itertools
import string

from hcracker.utils import AttackBuilder
from hcracker.enums import Eapol
from hcracker.models import (
    Attack,
    Iteration
)

class TestAttackBuilder(unittest.TestCase):
    def test_attack_builder_instance(self):
        self.assertIsInstance(AttackBuilder(), Attack)

    def test_use_attack_builder(self):
        attack = AttackBuilder()

        try:
            attack.set_iterations()
            attack.set_eapols(eapols={Eapol.EAPOL1: "test1.bin", Eapol.EAPOL2: "test2.bin"})
            attack.set_target()
            print("[+] Attack builder setup succesful!")
        except Exception as ex:
            print(f"[-] {ex}")

    def test_use_attack_builder_with_custom_iterations(self):
        attack = AttackBuilder()
        custom_iterations = {}

        charsets = {}
        charsets["letters"] = string.ascii_letters
        charsets["lettersAndNumbers"] = string.ascii_letters + string.digits
        charsets["specialChars"] = string.ascii_letters + string.digits + "!\"#$%&/()'"

        for key, charset in charsets.items():
            custom_iterations[key] = Iteration()
            custom_iterations[key].iteration = itertools.permutations(charset, 12)

        try:
            attack.set_iterations(custom_iterations)
            attack.set_eapols(eapols={Eapol.EAPOL1: "test1.bin", Eapol.EAPOL2: "test2.bin"})
            attack.set_target()
            print("[+] Attack builder setup using custom iterations succesful!")
        except Exception as ex:
            print(f"[-] {ex}")
