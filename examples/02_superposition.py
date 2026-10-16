"""Example 2 — quantum coins: a superposition of totals.

A 'quantum coin' is a nickel AND a dime until the slot sensor observes it.
Two quantum coins + one nickel -> the balance is a superposition of
15c / 20c / 20c / 25c, so coffee appears ~1/4 of the time.

Run:  python examples/02_superposition.py
"""
from qiskit_aer import AerSimulator
from qvend import vending_machine, report

sim = AerSimulator()

print("quantum, quantum, nickel -> expect coffee ~25%")
counts = sim.run(vending_machine([-1, -1, 0]), shots=4096).result().get_counts()
report(counts, "OBSERVED machine: 2 quantum coins + nickel")

print("\nquantum, dime            -> expect coffee ~50%")
counts = sim.run(vending_machine([-1, 1]), shots=4096).result().get_counts()
report(counts, "OBSERVED machine: 1 quantum coin + dime")
