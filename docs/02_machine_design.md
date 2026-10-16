# 2. Machine Design — registers, reversible adders, vend logic

*Previous: [01_foundations.md](01_foundations.md). Next: [03_observation.md](03_observation.md).*
*Code: `qvend/arithmetic.py`, `qvend/machine.py`.*

## 2.1 Register layout (every machine)

```
QuantumCircuit
├── credit  : QuantumRegister(3)  balance in 5c units, q0 = LSB
├── coin    : QuantumRegister(n)  one qubit per dropped coin
├── vend    : QuantumRegister(1)  1 = coffee dispensed
├── c_coin  : ClassicalRegister(n)   coin-slot records
└── c_final : ClassicalRegister(4)   [vend, q2, q1, q0]
```

Price = 5 units (25¢). Values 0–6 are reachable with ≤3 coins.

## 2.2 Reversible ripple adders (`arithmetic.py`)

A quantum adder must be unitary, so we build the same truth table as a
classical ripple-carry adder from `X/CX/CCX` gates. Applying carries **MSB
first** guarantees every gate sees the *old* bit values:

```python
def inc_1(q):                      # +1:  q2 ^= q1&q0 ; q1 ^= q0 ; q0 ^= 1
    ccx(q0, q1, q2); cx(q0, q1); x(q0)

def inc_2(q):                      # +2:  q1 flips; carry to q2 is exactly q1(old)
    cx(q1, q2); x(q1)
```

Two design notes worth remembering:

* `inc_2`'s carry is `q1` alone, **not** `q1 & q0`: 1+1 overflows bit 1
  regardless of bit 0. (Our first version used `q1 & q0` and `dime, dime`
  wrapped 4¢→0¢. The audit in doc 05 exists because of that bug — exact
  matrix comparison catches such errors instantly.)
* Because these are unitaries `|x⟩ → |x+k⟩`, they are *also* correct on
  superpositions — verified against the full 8×8 permutation matrices in
  `tests/audit.py` (deviation exactly 0).

## 2.3 Vend logic

Coffee iff credit ∈ {5, 6}, and with bits `q2 q1 q0` that set is exactly

```
vend = (q2 ∧ q1) ⊕ (q2 ∧ q0)   ==   q2 ∧ (q1 ⊕ q0)
```

implemented as two `CCX`s into the vend qubit — again reversible, again
linear on superpositions. So "coffee" itself can be in superposition.

## 2.4 Coin-drop = one controlled addition

Dropping a coin means: credit += 1 + coin, where coin is 0 (nickel) or 1
(dime). There are two ways to wire this, and they are *physically
different* — the subject of the next doc:

```
Machine A (observed):   measure the coin, then classical if/else adds +1/+2
Machine B (coherent):   add +1 always, and a second +1 gated by mcx with the
                        COIN QUBIT as control — nothing ever looks at the coin
```

Machine C (`vending_machine_bell`) handles both modes and additionally
accepts entangled coin *pairs*.

## 2.5 Circuit anatomy (observed machine, one coin)

```
        ┌───┐┌─────────┐┌──────────────────────┐┌─────────┐
credit ─┤   ├┤ if c==1 ├┤ inc_2 (3 gates)      │┤         ├──────────
        │   ├┤ if c==0 ├┤ inc_1 (3 gates)      ││ measure ├─ c_final
coin   ─┤ H ├┤ measure ├┤  ...feed-forward...  ││         │
        └───┘└─────────┘└──────────────────────┘└─────────┘
         prep   sensor        adds +1 or +2       vend logic
```

Draw any circuit yourself — they are ordinary Qiskit circuits,
portable to real devices as-is:

```python
from qvend import vending_machine
print(vending_machine([-1, 1]).draw("text"))
```
