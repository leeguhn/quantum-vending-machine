"""Coin preparation: single coins and entangled Bell pairs of coins.

Basis convention: |0> = NICKEL (5c), |1> = DIME (10c).

    single nickel   : |0>
    single dime     : |1>
    quantum coin    : H|0> = (|0> + |1>)/sqrt2      (both at once)
    Different pair  : |Psi+> = (|01> + |10>)/sqrt2  (always differ when weighed,
                      always AGREE in the complementary X basis -> entangled)
    Same pair       : |Phi+> = (|00> + |11>)/sqrt2  (always agree when weighed)
"""
from qiskit import QuantumCircuit


def prep_single(qc: QuantumCircuit, qubit, spec: int) -> None:
    if spec == 1:
        qc.x(qubit)          # dime
    elif spec == -1:
        qc.h(qubit)          # quantum coin
    # spec == 0 -> nickel: leave in |0>


def prep_pair(qc: QuantumCircuit, a, b, kind: str) -> None:
    """Prepare an entangled pair of coins on qubits a, b."""
    qc.h(a)
    qc.cx(a, b)              # (|00> + |11>)/sqrt2  == Same pair
    if kind == "D":
        qc.x(b)              # -> (|01> + |10>)/sqrt2 == Different pair


def expand_coins(specs):
    """Expand coin specs into per-qubit entries + pair links.

    Returns (coins, pairs):
        coins: one entry per coin qubit ('D'/'S' entries become two 'Q'
               placeholders), pairs: list of (i, j, kind).
    """
    coins, pairs = [], []
    for item in specs:
        if item in ("D", "S"):
            i = len(coins)
            coins += ["Q", "Q"]
            pairs.append((i, i + 1, item))
        else:
            coins.append(item)
    return coins, pairs
