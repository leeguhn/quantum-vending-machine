"""Example 3 — entangled coin PAIRS.

'Different' pair : worth EXACTLY 15c although each coin is random
                   (one nickel + one dime, undecided which is which).
'Same' pair      : coins agree, so the total is genuinely uncertain.

Run:  python examples/03_entangled.py
"""
from qiskit_aer import AerSimulator
from qvend import vending_machine_bell, report

sim = AerSimulator()

print("Different pair + dime -> each coin random but total is CERTAIN 25c")
counts = sim.run(vending_machine_bell(["D", 1]), shots=2048).result().get_counts()
report(counts, "entangled Different pair + dime")

print("\nSame pair + nickel   -> total 15c or 25c; expect coffee ~50%")
counts = sim.run(vending_machine_bell(["S", 0]), shots=2048).result().get_counts()
report(counts, "entangled Same pair + nickel")
