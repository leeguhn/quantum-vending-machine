"""Reversible arithmetic for the 3-qubit credit register.

The credit register q[0]=LSB .. q[2]=MSB counts 5-cent units (0..7).
Every gate is unitary (X / CX / CCX only), so the adders also act
correctly on superpositions — verified exactly in tests/audit.py.
"""
from qiskit import QuantumCircuit


def inc_1(qc: QuantumCircuit, q) -> None:
    """Add 1 to a 3-bit register (ripple-carry, MSB-first so every gate
    sees the OLD bit values).

    new q0 = ~q0 ; new q1 = q1 ^ q0 ; new q2 = q2 ^ (q1 & q0)
    """
    qc.ccx(q[0], q[1], q[2])
    qc.cx(q[0], q[1])
    qc.x(q[0])


def inc_2(qc: QuantumCircuit, q) -> None:
    """Add 2 to a 3-bit register.

    Bit 1 receives +1: q1 flips; 1+1 overflows regardless of q0,
    so the carry into q2 is exactly q1(old).
    """
    qc.cx(q[1], q[2])
    qc.x(q[1])


def vend_logic(qc: QuantumCircuit, state, vend) -> None:
    """Set |vend> ^= 1 iff the credit is 5 or 6 (i.e. >= 25 cents).

    vend = (q2 & q1) ^ (q2 & q0)  ==  q2 & (q1 ^ q0)
    (values 0..6 are the reachable range; 7 is not produced by 3 coins).
    """
    qc.ccx(state[2], state[1], vend)
    qc.ccx(state[2], state[0], vend)
