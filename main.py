import argparse

from hcracker import PassphraseCracker
from hcracker.utils import AttackBuilder
from hcracker.enums import *

def parse_arguments() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("-e1", "--eapol1", type=str, required=True, help="Eapol message 1")
    parser.add_argument("-e2", "--eapol2", type=str, required=True, help="Eapol message 2")

    return parser.parse_args()

def main(args) -> None:
    attack = AttackBuilder()

    attack.set_iterations()
    attack.set_eapols(eapols={Eapol.EAPOL1: args.eapol1, Eapol.EAPOL2: args.eapol2})
    attack.set_target()

    crack = PassphraseCracker(attack)

    try:
        crack.run()
    except KeyboardInterrupt:
        sys.exit(-1)

if __name__ == '__main__':
    args = parse_arguments()
    main(args)
