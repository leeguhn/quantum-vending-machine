# 4. Entangled Coins — definite relationships, undecided parts

*Previous: [03_observation.md](03_observation.md). Next: [05_verification_audit.md](05_verification_audit.md).*
*Code: `qvend/coins.py`, `vending_machine_bell`, `examples/03_*.py`, `examples/04_*.py`.*

## 4.1 Preparing entangled coins

Two coin qubits in a **Bell state** have a definite *relationship* while
neither coin has a definite value:

```
|Psi+> = (|nickel,dime> + |dime,nickel>)/√2   "Different pair"  (spec "D")
|Phi+> = (|nickel,nickel> + |dime,dime>)/√2   "Same pair"       (spec "S")
```

Both are made by two gates: `H(a); CX(a,b)` (and an `X(b)` for the
Different pair).

## 4.2 Uncertain parts, certain whole — the vending payoff

The Different pair is worth **exactly 15¢ with certainty**, although *each
coin individually* is maximally random:

```
Different pair + dime  ->  15c + 10c  ->  COFFEE on 100% of shots,
                                        coin string random (01 or 10)
```

Classically, two unknown coins are worth 10, 15 or 20¢ — you can never be
certain. The pair's *sum* is a property of the relationship, and the
relationship is physical.

The Same pair inverts the lesson: the difference is certain (0), the total
is genuinely uncertain (2 or 4 units) — so `pair-same + nickel` vends
exactly half the time.

## 4.3 What the machine does to entanglement

Run `examples/03_entangled.py` (observed mode) vs
`examples/04_coherent_statevector.py` (coherent mode):

* **Observed machine**: each coin is measured at the slot — the pair's
  entanglement is consumed by the sensor, leaving classical correlation
  (`01` or `10`, randomly, forever correlated).
* **Coherent machine**: the exact statevector shows the pair *still inside*
  a Bell state after the adders ran: the global state is
  `|Psi+> ⊗ |credit=5> ⊗ |vend=1>` — the machine performed arithmetic
  *around* the entanglement without breaking it.

This is a mini-demo of the central requirement of quantum computing:
operations must be coherent (no uncontrolled observation) if entanglement —
the computational resource — is to survive the computation.

## 4.4 But is a Bell pair more than "secretly agreed"?

A skeptic notes: a classical pair sealed in envelopes ("one nickel, one
dime, you pick which") reproduces everything in section 4.2. True — that is
why we test a *complementary* question, and then run a Bell test. Those are
in doc [05](05_verification_audit.md), with measured S ≈ 2.81 > 2, which no
envelope story can produce.

## 4.5 Try it

```bash
python -m qvend.cli pair-different dime             # observed
python -m qvend.cli pair-different dime --coherent  # unobserved
python -m qvend.cli pair-same nickel
```

| input | expectation |
|---|---|
| `pair-different dime` | COFFEE 100%, coin strings only `…01`/`…10` |
| `pair-same nickel` | COFFEE ≈ 50%, coin strings only `…00`/`…11` |
