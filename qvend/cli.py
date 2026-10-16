"""Command-line interface: buy coffee from the terminal.

    python -m qvend.cli dime dime nickel
    python -m qvend.cli quantum quantum nickel --shots 4096
    python -m qvend.cli pair-different dime --coherent
    python -m qvend.cli --help
"""
import argparse

from qiskit_aer import AerSimulator

from qvend.machine import vending_machine_bell
from qvend.reporting import report

ALIASES = {
    "nickel": 0, "n": 0,
    "dime": 1, "d": 1,
    "quantum": -1, "q": -1,
    "pair-different": "D", "pd": "D",
    "pair-same": "S", "ps": "S",
}


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="qvend", description="Quantum vending machine (25c = COFFEE!)")
    ap.add_argument("coins", nargs="+", choices=sorted(ALIASES),
                    help="nickel/dime/quantum coins, entangled pairs "
                         "pair-different/pair-same (each pair = TWO coins)")
    ap.add_argument("--shots", type=int, default=1024)
    ap.add_argument("--coherent", action="store_true",
                    help="do NOT observe the coins (fully quantum machine)")
    args = ap.parse_args(argv)

    specs = [ALIASES[c] for c in args.coins]
    label = ("COHERENT (unobserved coins)" if args.coherent
             else "OBSERVED (coin-slot sensor)")
    print(f"Inserting: {args.coins}   mode: {label}")

    qc = vending_machine_bell(specs, coherent=args.coherent)
    counts = AerSimulator().run(qc, shots=args.shots).result().get_counts()
    report(counts, "machine readout")


if __name__ == "__main__":
    main()
