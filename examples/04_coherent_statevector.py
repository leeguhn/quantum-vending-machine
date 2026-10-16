"""Example 4 — the coherent machine, seen exactly (statevector, no shots).

The coins are NEVER observed: the adder is controlled by the coin qubits.
With 3 quantum coins all 8 histories are computed at once; with a
'Different' pair the balance is sharp while the coins stay entangled.

Run:  python examples/04_coherent_statevector.py
"""
import numpy as np
from qiskit.quantum_info import Statevector
from qvend import vending_machine_bell, report_statevector

# 3 quantum coins: total = 3 + (#dimes), coffee when >= 5, i.e. P = 1/2
sv = Statevector.from_instruction(
    vending_machine_bell([-1, -1, -1], coherent=True, final_measure=False))
report_statevector(sv, n_coins=3,
                   title="\n3 quantum coins, coherent machine (exact statevector):")

# Different pair + dime: credit is exactly 5 in every branch,
# and the pair remains entangled (both coins undecided).
sv = Statevector.from_instruction(
    vending_machine_bell(["D", 1], coherent=True, final_measure=False))
report_statevector(sv, n_coins=3,
                   title="\nDifferent pair + dime, coherent machine:")
