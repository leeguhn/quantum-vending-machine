# 1. Foundations — from a coin counter to qubits

*Reading order: this first. Next: [02_machine_design.md](02_machine_design.md).*

## 1.1 The classical machine

A coffee vend that accepts only two coins does something trivial: it keeps a
**number** — the credit — and adds 1 (nickel) or 2 (dime) to it. At
credit ≥ 5 (i.e. 25¢) it dispenses coffee.

To build this from qubits, replace each binary *bit* of the credit counter
with a **qubit**. Three qubits hold a number 0–7 in binary:

```
|q2 q1 q0>   e.g. |101> = 5 units = 25 cents
```

A **qubit** differs from a bit in one way with big consequences: besides
`|0⟩` and `|1⟩` it can be in a **superposition**

```
|ψ⟩ = a|0⟩ + b|1⟩ ,   |a|² + |b|² = 1
```

which behaves like "0 and 1 at once" until it is measured; a measurement
returns 0 with probability |a|² or 1 with probability |b|² and *leaves* the
qubit in the answer it gave.

## 1.2 The one rule that makes it physics

Quantum evolution is **unitary**: gates are reversible and act on
superpositions *by linearity*. A gate that maps `|0⟩→|1⟩` and `|1⟩→|0⟩`
automatically maps `( |0⟩+|1⟩ )/√2 → ( |1⟩+|0⟩ )/√2`. Nothing "checks
whether the input is definite" — quantum mechanics never peeks.

Consequence for us: if the *adder* (the machine's arithmetic) is built only
from reversible gates, it automatically works on **balances that are in
superposition** — no extra physics needed, just linearity. That is why
`qvend/arithmetic.py` uses only `X`, `CX`, `CCX` gates: they are universal
for reversible classical logic, and therefore define honest unitary
operators.

## 1.3 Superposition of banknotes

Put a coin qubit through a **Hadamard** gate `H` and it becomes

```
H|0⟩ = (|0⟩ + |1⟩)/√2      "nickel AND dime at once"
```

If the machine then adds this coin's value to its credit, linearity forces
the *credit itself* into a superposition of two totals. That single
mechanism — a reversible adder acting on a superposed coin — is the whole
trick behind "quantum vending machine". Everything else (entanglement, Bell
tests) is decoration on top of this.

## 1.4 What "2048 shots" means

We cannot inspect a superposition directly: measuring it produces *one*
random outcome and destroys the rest. So we repeat the whole experiment many
times (**shots**) and study the *frequencies*. The superposition is not
missing data — as doc [05](05_verification_audit.md) shows, no
"but-it-was-really-decided" story can reproduce the observed frequencies.

## 1.5 Vocabulary for the rest of the docs

| term | means here |
|---|---|
| credit register | 3 qubits holding the balance in 5¢ units |
| adder | X/CX/CCX gate network implementing +1 / +2 reversibly |
| coin-slot sensor | a mid-circuit `measure` that observes the coin |
| feed-forward | classical `if` on that measurement result steering later gates |
| coherent mode | no sensor: gates controlled *by the coin qubit itself* |
| vend qubit | flips to |1⟩ exactly when credit ∈ {5, 6} |
