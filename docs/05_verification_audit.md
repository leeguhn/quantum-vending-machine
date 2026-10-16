# 5. Verification Audit — proving it's quantum, not hidden coins

*Previous: [04_entangled_coins.md](04_entangled_coins.md). This is the skeptic's doc.*
*Code: `tests/audit.py` (run: `python tests/audit.py`).*

## 5.1 Why this doc exists

Every demo in docs 1–4 uses plain coin-weighings (Z-basis measurements).
A skeptic may object: *"maybe each pair was secretly pre-painted
nickel+dime or dime+nickel."* That classical model reproduces **all** of
those demo numbers. Demanding a proof is legitimate — so we run four tests
that model cannot survive. (The audit was written after exactly this pushback,
and it immediately exposed a real adder bug — see 5.2.)

## 5.2 TEST 1 — the arithmetic is exactly quantum-mechanical

Build the full 8×8 operator of `inc_1` / `inc_2` and compare with the exact
permutation matrices |x⟩ → |x+1⟩, |x+2⟩; check the vend map is exactly
reversible.

```
inc_1: unitary=True  exactly +1 on ALL 8 basis states (max dev 0.0e+00)
inc_2: unitary=True  exactly +2 ...                    (max dev 0.0e+00)
vend_logic: exact reversible vend map for all 8 credits: True
```

Why it matters: unitaries act correctly on superpositions *by linearity*,
so the machine's bookkeeping is genuinely a quantum channel. (History: the
first `inc_2` had carry `q1&q0` instead of `q1` — 2+2 wrapped to 0. Exact
matrix comparison catches this class of bug permanently.)

## 5.3 TEST 2 — the complementary weighing

Our Different pair is |Ψ⁺⟩: always **differs** when weighed, but it is an
eigenstate of X⊗X with eigenvalue +1 — always **agrees** in the
complementary (X) weighing. Envelope coins that only pre-agree a Z-value
have *no* consistency in the X basis: P(agree) = 0.5.

```
pre-agreed classical pair : P(agree in X) = 0.500
our pair                  : P(agree in X) = 1.0000
```

## 5.4 TEST 3 — CHSH Bell test (the loophole-closer)

For ANY model in which each coin carries pre-written answers to all four
possible weighings a ∈ {Z, X}, b ∈ {(Z±X)/√2}, the correlation
E(a,b) = P(same) − P(diff) obeys |S| ≤ 2 for
S = ±E(a₀,b₀) ±E(a₀,b₁) ±E(a₁,b₀) ±E(a₁,b₁).

Methodology: the settings and sign pattern are computed from **theory**
before sampling; S is then estimated purely from sampled shots (4096/setting).

```
theory : S_theory = -2.828
sampled: S = -2.812 ± 0.06        (local realism: |S| <= 2)
-> violates Bell inequality by ~0.81, > 13 standard errors
```

This kills *every* pre-agreement story, in any basis.

## 5.5 TEST 4 — the machine itself stays coherent

With the coherent machine fed a Different pair + dime:

```
a) fidelity with exact prediction |Ψ+> ⊗ |credit=5> ⊗ |vend=1> : 1.0000000000
b) entanglement of one coin AFTER the adders:  1.000 ebit
c) X-basis agreement test THROUGH the adders:  P(agree) = 1.0000
d) observed (feed-forward) machine counterpart: collapses to the
   classical mixture, P(agree) = 0.5, entanglement 0 ebit
```

Meaning: the arithmetic is a unitary that *moved* entanglement around
without destroying it; and the difference between the two machines is
exactly one observation (doc 03), with measurable consequences.

## 5.6 Honest caveats

1. **Simulator, not lab.** Aer solves the Schrödinger equation exactly;
   these tests certify that *the circuits implement quantum predictions*.
   On real hardware the identical code tests nature (expect S ≈ 2.3–2.6
   under noise). Bell-test loopholes (locality, freedom-of-choice) are
   lab issues, not circuit issues.
2. TEST 2's 0.5 bound targets pre-agreement in the *weighing basis only*;
   TEST 3 is the general refutation. Both are included because they fail
   for different reasons.
3. The **observed** machine is genuinely classical after the sensor (TEST
   4d). Only the coherent machine deserves the label "quantum computer".

## 5.7 Re-running

```bash
python tests/audit.py
```

Headline numbers to expect: `max dev 0.0e+00`, `P(agree)=1.0000`,
`S = -2.81 ± 0.06`, `fidelity 1.0000000000`, `1.000 ebit`.
