"""qvend — a quantum vending machine (Qiskit).

Library layout
    qvend.arithmetic  : reversible 3-bit adders and the vend decision logic
    qvend.coins       : coin qubits, Bell-pair coin preparation
    qvend.machine     : the two machines (observed/feed-forward & coherent)
    qvend.reporting   : human-readable output helpers

Coin spec convention used everywhere:
    0   nickel          (5 cents, +1 unit)
    1   dime            (10 cents, +2 units)
   -1   quantum coin    (superposition of nickel and dime)
   "D" entangled Different pair  (two coins, one nickel one dime, undecided which)
   "S" entangled Same pair       (two coins, identical, undecided which)
"""
from qvend.arithmetic import inc_1, inc_2, vend_logic
from qvend.machine import (vending_machine, vending_machine_coherent,
                           vending_machine_bell, expand_coins)
from qvend.reporting import report, report_statevector

COFFEE_PRICE_UNITS = 5          # 5 x 5 cents = 25 cents

__all__ = [
    "inc_1", "inc_2", "vend_logic",
    "vending_machine", "vending_machine_coherent", "vending_machine_bell",
    "expand_coins", "report", "report_statevector", "COFFEE_PRICE_UNITS",
]
