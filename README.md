# Quantum Vending Machine

A coffee vend (25¢) implemented as a **quantum finite-state machine** in Qiskit —
with classical coins, quantum coins, and **entangled coin pairs** — plus an
adversarial audit proving the machine really obeys quantum principles.

```
$ python -m qvend.cli dime dime nickel
Inserting: ['dime', 'dime', 'nickel']   mode: OBSERVED (coin-slot sensor)
  credit=5 (25c)  COFFEE!   1024/1024 shots
```

## Quick start

```bash
pip install -r requirements.txt
pip install -e .                        # installs the qvend package

python examples/01_classical.py            # sanity: behaves like a real machine
python examples/02_superposition.py        # quantum coins -> probabilistic coffee
python examples/03_entangled.py            # entangled coin pairs
python examples/04_coherent_statevector.py # exact statevector of the quantum machine
python tests/audit.py                      # Bell-violation & coherence audit

python -m qvend.cli quantum quantum nickel # buy coffee from the terminal
```

## How to read the docs (logical flow)

Start at 01 and go in order; each one builds on the previous.

| # | Document | Question it answers |
|---|----------|---------------------|
| 1 | [docs/01_foundations.md](docs/01_foundations.md) | What are qubits, superposition, and how does a counter become quantum? |
| 2 | [docs/02_machine_design.md](docs/02_machine_design.md) | How is the machine actually built (registers, reversible adders, vend logic)? |
| 3 | [docs/03_observation.md](docs/03_observation.md) | What is a *measurement/observation*, and why do two different machines exist? |
| 4 | [docs/04_entangled_coins.md](docs/04_entangled_coins.md) | What happens when the coins are entangled Bell pairs? |
| 5 | [docs/05_verification_audit.md](docs/05_verification_audit.md) | How do we *know* this isn't classical randomness in disguise? (Bell test) |

**Using it, not theorizing?** → [MANUAL.md](MANUAL.md) (everything you need to
run demos, drive the CLI, write your own programs, and interpret the output).

## Project layout

```
quantum-vending-machine/
├── README.md                 ← you are here
├── MANUAL.md                 ← user manual (running & programming)
├── requirements.txt
├── docs/                     ← conceptual reading, in learning order (01→05)
├── qvend/                    ← the library
│   ├── arithmetic.py         ← reversible adders + vend logic (X/CX/CCX only)
│   ├── coins.py              ← single & entangled Bell-pair coin preparation
│   ├── machine.py            ← Machine A (observed), B (coherent), C (entangled-capable)
│   ├── reporting.py          ← readable output of counts / statevectors
│   └── cli.py                ← terminal interface (`python -m qvend.cli ...`)
├── examples/                 ← numbered, runnable, self-documenting
└── tests/audit.py            ← the adversarial quantum-behaviour audit
```

## One-paragraph summary

The machine counts money in a 3-qubit register with reversible gates and
dispenses coffee at ≥25¢. With ordinary coins it matches a real vending
machine exactly. With *quantum* coins (a Hadamard away from classical) the
balance itself enters superposition, and coffee becomes genuinely
probabilistic. With *entangled* coin pairs, relationships between coins
become definite while the coins themselves remain undecided — and a CHSH
Bell test (S ≈ 2.81 > 2) plus a coherence audit of the arithmetic confirm
this is quantum mechanics, not hidden classical randomness.
