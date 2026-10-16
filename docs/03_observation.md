# 3. Observation — what a measurement physically is, and the two machines

*Previous: [02_machine_design.md](02_machine_design.md). Next: [04_entangled_coins.md](04_entangled_coins.md).*
*Code: `qvend/machine.py` (`vending_machine` vs `vending_machine_coherent`).*

## 3.1 Observation = creation of a record

"Observation" sounds mystical; in this project it is a component with a line
number. A quantum system keeps evolving in superposition **as long as no
record exists anywhere of which alternative happened**. The moment some
device irreversibly copies the information into something macroscopic — a
detector latch, a classical bit, the environment — the two branches can
never again interfere. That interaction is what we call a measurement.

Two ingredients make it "an observation":

1. **Copying out**: the alternative (nickel? dime?) is written into a stable
   classical carrier.
2. **Irreversibility**: the information spreads to ~Avogadro's worth of
   degrees of freedom (**decoherence**), so no one can un-write it.

Not required: a human, a brain, an "observer". A coin sensor is enough.
On real hardware, `measure` is a microwave pulse read out by a warm
amplifier — the bulkiest thing a qubit ever touches.

## 3.2 Where observation sits in our machine

| circuit location | what it observes | role |
|---|---|---|
| `qc.measure(coin, c_coin[i])` inside the coin loop | the coin | the **coin-slot sensor** |
| `qc.measure(state/vend, c_final...)` at the end | balance & vend | the odometer / "did coffee come out?" |

In the **observed machine** (`vending_machine`, `coherent=False`), the
sensor *must* see every coin — the feed-forward `if_test` logic is built on
that sight. The spinning coin lands at the sensor; only the *choice* is
random.

In the **coherent machine** (`vending_machine_coherent`) the sensor is
**removed**: the extra +1 is applied by `mcx` gates whose control is the
coin qubit itself. The machine reacts to the coin without ever seeing it —
so coin and balance stay in superposition, and (with prepared pairs)
**entangled**, until the final readout.

## 3.3 Same arithmetic, different physics

Both machines compute "credit += 1 + coin". Compare them with identical
inputs and the raw `coins=` column:

```
observed :  balance always matches the measured coins   (sensor decided first)
coherent :  all coin-histories coexist; only the final readout resolves them
```

The audit (`tests/audit.py`, TEST 4) shows this is not rhetoric:

* coherent machine: one coin still shares **1.000 ebit** of entanglement
  *after* the adders have acted on it;
* observed machine: the same quantity is **0** — observation converted
  quantum correlation into mere classical correlation.

That is the operational meaning of "observation": it is the only thing that
turns the coherent machine into the observed one, and the two are otherwise
bit-for-bit the same circuit.

## 3.4 A useful intuition pump

Drop a spinning coin into two machines:

* **Vending machine A** has a glass slot with a light sensor → the coin is
  forced to fall before the counter moves. The counter learns a fact.
* **Vending machine B** is a sealed crystal: the coin's *value* merges into
  the balance while the coin keeps spinning inside. Nothing learned, nothing
  decided — until you finally read the balance, and the coin's fate is read
  with it, consistently, because they share one quantum state.

Which machine are you building is an engineering choice (`coherent=True/False`).
Nature honors whichever you choose.
