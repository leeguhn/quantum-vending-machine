"""Example 1 — the machine must behave classically for classical coins.

Run:  python examples/01_classical.py     (from the project root)
"""
from qiskit_aer import AerSimulator
from qvend import vending_machine, report

sim = AerSimulator()

print("dime, dime, nickel  (10+10+5 = 25c)  -> expect COFFEE, 100%")
counts = sim.run(vending_machine([1, 1, 0]), shots=1024).result().get_counts()
report(counts, "exact change")

print("dime, dime          (20c)            -> expect NO coffee, 100%")
counts = sim.run(vending_machine([1, 1]), shots=1024).result().get_counts()
report(counts, "not enough")

print("five nickels        (25c)            -> expect COFFEE, 100%")
counts = sim.run(vending_machine([0] * 5), shots=1024).result().get_counts()
report(counts, "slow payment")
