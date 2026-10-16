# User Manual

Everything you need to run, drive, program, and interpret the quantum
vending machine. No theory required (that's in `docs/`).

---

## 1. Installation

```bash
cd quantum-vending-machine
python -m venv .venv && source .venv/bin/activate     # optional but tidy
pip install -r requirements.txt
pip install -e .                                      # installs the `qvend` package
```

* Python ≥ 3.10, `qiskit` ≥ 1.1, `qiskit-aer` ≥ 0.13.
* Everything runs on the included simulator. To run on a real device, keep
  the circuits identical and swap `AerSimulator` for a `BackendV2` from
  `qiskit_ibm_runtime`.

All commands below assume you run **from the project root** (so `qvend/` is
importable).

---

## 2. Buy coffee from the terminal (CLI)

```bash
python -m qvend.cli dime dime nickel           # 10+10+5  -> COFFEE!
python -m qvend.cli dime dime                  # 20c      -> no coffee
python -m qvend.cli nickel nickel nickel nickel nickel
python -m qvend.cli quantum dime               # coin undecided -> 50% coffee
python -m qvend.cli quantum quantum nickel --shots 4096
python -m qvend.cli pair-different dime --coherent   # entangled pair, unobserved
python -m qvend.cli --help
```

### Coin vocabulary

| CLI word | alias | meaning | value |
|---|---|---|---|
| `nickel`  | `n`  | classical 5¢            | +1 unit |
| `dime`    | `d`  | classical 10¢           | +2 units |
| `quantum` | `q`  | nickel **and** dime until observed | +1 *and* +2 |
| `pair-different` | `pd` | **two** entangled coins, always different when weighed | exactly +3 combined |
| `pair-same`      | `ps` | **two** entangled coins, always equal when weighed | +2 *and* +4 combined |

### Modes

| flag | machine | coin-slot sensor? |
|---|---|---|
| *(default)* | **Observed** — coins are measured, feed-forward does the adding | yes |
| `--coherent` | **Unobserved** — adder controlled by the coin qubit itself | no |

---

## 3. Reading the output

```
  credit=5 (25c)  COFFEE!       1022/4096 shots   coins=1101
  └─balance──┘   └──result┘     └──frequency──┘   └─measured coins─┘
```

* **credit** — balance in 5¢ units (the 3-qubit register, decoded).
* **COFFEE!** — the `vend` qubit was `|1⟩`: price reached (≥ 25¢).
* **n/N shots** — the experiment was repeated N times; each line is one
  observed outcome. Quantum outcomes are random *per shot* but the
  *frequencies* are the physics.
* **coins** — what the coin slot recorded (or, in `--coherent`, what the
  coins turned out to be at final readout). The string is written
  MSB-first: the **first coin you dropped appears last**. E.g. dropping
  dime, dime, nickel shows `coins=011`.

### Expectation table (sanity checks)

| coins inserted | expected outcome |
|---|---|
| `dime dime nickel` | COFFEE 100% |
| `dime dime` | never |
| `nickel ×5` | COFFEE 100% |
| `quantum dime` | COFFEE ≈ 50% |
| `quantum quantum nickel` | COFFEE ≈ 25% |
| `quantum ×3` | COFFEE ≈ 50% |
| `pair-different dime` | COFFEE 100% (random coins, certain total!) |
| `pair-same nickel` | COFFEE ≈ 50% |

If your numbers look like this, the machine works. (Frequencies are
statistical: ±1–3% fluctuation at 1024 shots is normal.)

---

## 4. Programming the machine (Python API)

```python
from qiskit_aer import AerSimulator
from qvend import vending_machine, vending_machine_bell, report

specs = [1, -1, 0]                 # dime, quantum coin, nickel
qc = vending_machine(specs)        # observed machine, Qiskit circuit
counts = AerSimulator().run(qc, shots=2048).result().get_counts()
report(counts, "my program")
```

Available builders (all return ordinary `QuantumCircuit`s you can `draw()`,
transpile, or send to real hardware):

| function | purpose |
|---|---|
| `vending_machine(specs)` | observed machine, single coins only (0/1/-1) |
| `vending_machine_coherent(specs, final_measure=True)` | unobserved machine |
| `vending_machine_bell(specs, coherent=False, final_measure=True)` | both modes + entangled pairs `"D"`/`"S"` |

Spec convention everywhere: `0`=nickel, `1`=dime, `-1`=quantum, `"D"`/`"S"` =
one entangled **pair** (occupies two coin slots).

Exact analysis without shots (no noise, all amplitudes):

```python
from qiskit.quantum_info import Statevector
from qvend import vending_machine_bell, report_statevector
sv = Statevector.from_instruction(
    vending_machine_bell(["D", 1], coherent=True, final_measure=False))
report_statevector(sv, n_coins=3)
```

---

## 5. Examples & tests

```bash
python examples/01_classical.py            # must match a real vending machine
python examples/02_superposition.py        # probabilistic coffee
python examples/03_entangled.py            # entangled pairs
python examples/04_coherent_statevector.py # exact amplitudes
python tests/audit.py                      # the full quantum-behaviour audit
```

Expected audit headline: `S = -2.81 ± 0.06  (local realism: |S| <= 2)` and
`fidelity = 1.0000000000`, `1.000 ebit`.

---

## 6. Troubleshooting

| symptom | cause / fix |
|---|---|
| `ModuleNotFoundError: qvend` | run from the project root |
| `ImportError: qiskit_aer` | `pip install qiskit-aer` |
| mid-circuit measurement error on some backends | use a device supporting the *simulator-extension* / live feed-forward, or switch to `vending_machine_bell(specs, coherent=True)` |
| coffee frequency slightly off the table | statistics; raise `--shots` |
| `pair-different` counted as one coin | it is **two** coins (one pair) by design |
