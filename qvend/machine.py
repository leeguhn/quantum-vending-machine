"""The vending machine circuits.

Machine A  vending_machine()          "observed" machine
    Each coin is measured by the coin-slot sensor (mid-circuit measurement);
    classical feed-forward (qc.if_test) selects the +1 / +2 adder.

Machine B  vending_machine_coherent() "unobserved" machine
    The adder is controlled DIRECTLY by the coin qubit. Nothing observes the
    coins, so coin and balance remain in superposition / become entangled.

Machine C  vending_machine_bell()     handles both modes AND entangled pairs
    (spec entries 0, 1, -1, "D", "S").

Qubit/register layout (all machines)
    credit  : 3 qubits, binary balance in 5-cent units (q2 q1 q0)
    coin    : 1 qubit per dropped coin (Machine A recycles a single qubit)
    vend    : 1 qubit, 1 = coffee dispensed
    coin_meas : classical copy of every coin (or all-zero if unobserved)
    result  : [vend, q2, q1, q0]   (vend is the MSB)
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

from qvend.arithmetic import inc_1, inc_2, vend_logic
from qvend.coins import prep_single, prep_pair, expand_coins


def _registers(n_coin_qubits, n_coin_bits=None):
    n_coin_bits = n_coin_bits or n_coin_qubits
    state = QuantumRegister(3, "credit")
    coin = QuantumRegister(n_coin_qubits, "coin")
    vend = QuantumRegister(1, "vend")
    c_coin = ClassicalRegister(n_coin_bits, "coin_meas")
    c_final = ClassicalRegister(4, "result")
    return state, coin, vend, c_coin, c_final


def vending_machine(coin_preparations) -> QuantumCircuit:
    """Machine A: observed coins + feed-forward. specs: 0, 1 or -1."""
    n = len(coin_preparations)
    state, coin, vend, c_coin, c_final = _registers(1, n)
    qc = QuantumCircuit(state, coin, vend, c_coin, c_final)

    for i, spec in enumerate(coin_preparations):
        qc.barrier()
        prep_single(qc, coin[0], spec)
        qc.measure(coin[0], c_coin[i])               # the coin-slot sensor
        with qc.if_test((c_coin[i], 1)):             # feed-forward logic
            inc_2(qc, state)                          # dime
        with qc.if_test((c_coin[i], 0)):
            inc_1(qc, state)                          # nickel
        qc.reset(coin[0])                             # recycle the sensor qubit

    vend_logic(qc, list(state), vend[0])
    qc.measure(state, c_final[0:3])                   # q_i -> c_final[i]
    qc.measure(vend[0], c_final[3])                   # counts show [vend q2 q1 q0]
    return qc


def vending_machine_coherent(coin_preparations, final_measure=True) -> QuantumCircuit:
    """Machine B: no observation until the end; adder controlled by coin qubit."""
    return vending_machine_bell(coin_preparations, coherent=True,
                                final_measure=final_measure)


def _drop_coin_coherent(qc, coin_qubit, state):
    """Balance += 1 + coin (i.e. +1 nickel, +2 dime) fully coherently."""
    inc_1(qc, state)                                     # +1 always
    qc.mcx([coin_qubit, state[0], state[1]], state[2])   # +1 controlled: q2
    qc.mcx([coin_qubit, state[0]], state[1])             #                q1
    qc.cx(coin_qubit, state[0])                          #                q0


def vending_machine_bell(specs, coherent=False,
                         final_measure=True) -> QuantumCircuit:
    """Machine C: any mix of 0, 1, -1 and entangled pairs 'D' / 'S'.

    coherent=True   : never observe the coins (true quantum machine)
    coherent=False  : coin-slot sensor + feed-forward (observed machine)
    """
    coins, pairs = expand_coins(specs)
    n = len(coins)
    state, coin, vend, c_coin, c_final = _registers(n)
    qc = QuantumCircuit(state, coin, vend, c_coin, c_final)

    for i, spec in enumerate(coins):
        if spec != "Q":
            prep_single(qc, coin[i], spec)
    for (i, j, kind) in pairs:
        prep_pair(qc, coin[i], coin[j], kind)

    for i, spec in enumerate(coins):
        qc.barrier()
        if coherent:
            _drop_coin_coherent(qc, coin[i], list(state))
        else:
            qc.measure(coin[i], c_coin[i])
            with qc.if_test((c_coin[i], 1)):
                inc_2(qc, list(state))
            with qc.if_test((c_coin[i], 0)):
                inc_1(qc, list(state))
            qc.reset(coin[i])

    vend_logic(qc, list(state), vend[0])
    if final_measure:
        qc.measure(state, c_final[0:3])
        qc.measure(vend[0], c_final[3])
        if coherent:
            for i in range(n):
                qc.measure(coin[i], c_coin[i])
    return qc
