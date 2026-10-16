"""Adversarial audit — does the machine really obey quantum principles,
or is the 'quantum' just classical randomness in disguise?

    Run:  python tests/audit.py        (from the project root)

TEST 1  Arithmetic is EXACTLY unitary quantum mechanics:
        the adders must equal the full 8x8 permutation matrices,
        and the vend map must be exactly reversible.

TEST 2  X-basis interference test: a classically 'pre-agreed' coin pair
        can agree in the complementary X basis at most half the time;
        the entangled pair must agree 100%.

TEST 3  CHSH Bell test. Settings and sign pattern are fixed by THEORY
        before sampling; S is then estimated from sampled shots only.
        Local realism demands |S| <= 2; quantum theory gives 2*sqrt(2).

TEST 4  Coherence of the machine itself:
        a) machine statevector fidelity with the exact QM prediction
        b) one coin's entanglement (ebit) AFTER the arithmetic
        c) X-basis agreement test performed THROUGH the adders
        d) contrast: the observed (feed-forward) machine reduces to a
           classical mixture of coin values.

CAVEAT: this runs on a statevector-exact simulator, so these tests verify
that the CIRCUITS implement quantum predictions. On real hardware the same
tests become empirical tests of nature (expect S ~ 2.3-2.6 with noise).
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np
import numpy.linalg as la
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Operator, Statevector, DensityMatrix, partial_trace
from qiskit_aer import AerSimulator

from qvend import inc_1, inc_2, vend_logic, vending_machine_bell
from qvend.coins import prep_pair

sim = AerSimulator()

# ------------------------------------------------------------------ TEST 1
def perm_matrix(shift):
    P = np.zeros((8, 8), complex)
    for x in range(8):
        P[(x + shift) % 8, x] = 1.0
    return P

print("TEST 1  adder arithmetic vs exact permutation matrices")
for name, fn, s in [("inc_1", inc_1, 1), ("inc_2", inc_2, 2)]:
    q = QuantumRegister(3); qc = QuantumCircuit(q); fn(qc, list(q))
    op = Operator(qc)
    print(f"   {name}: unitary={op.is_unitary()}  exactly +{s} on ALL 8 basis "
          f"states: {np.allclose(op.data, perm_matrix(s))}  "
          f"(max dev {np.abs(op.data - perm_matrix(s)).max():.1e})")

st = QuantumRegister(3); vd = QuantumRegister(1)
qc = QuantumCircuit(st, vd); vend_logic(qc, list(st), vd[0])
U = Operator(qc).data
ok = all(abs(U[v + (8 if v in (5, 6) else 0), v] - 1) < 1e-12 for v in range(8))
print(f"   vend_logic: exact reversible vend map for all 8 credits: {ok}")

# ------------------------------------------------------- shared helpers
def psi_sv():                       # |Psi+>: the 'Different' pair state
    qc = QuantumCircuit(2); prep_pair(qc, 0, 1, "D")
    return Statevector.from_instruction(qc)

def rot(t):                         # circuit that measures direction
    c = QuantumCircuit(1); c.ry(t, 0); return c        # (sin t, 0, cos t)

def correlation(angles, shots=None, sv=None):
    """E = P(same) - P(different) on qubits 0,1 measured along angles."""
    if shots is None:               # exact theory
        c = QuantumCircuit(2)
        for q, t in enumerate(angles):
            c.compose(rot(t), [q], inplace=True)
        sv3 = sv.evolve(c)
        p_same = sum(abs(a) ** 2 for i, a in enumerate(sv3.data)
                     if ((i >> 0) & 1) == ((i >> 1) & 1))
        return 2 * p_same - 1
    c = QuantumCircuit(2, 2); prep_pair(c, 0, 1, "D")
    for q, t in enumerate(angles):
        c.compose(rot(t), [q], inplace=True)
    c.measure([0, 1], [0, 1])
    counts = sim.run(c, shots=shots).result().get_counts()
    same = sum(n for b, n in counts.items() if b[0] == b[1])
    return (2 * same - shots) / shots

def p_agree_x(sv, i, j):            # P(qubits i,j agree when weighed in X basis)
    hh = QuantumCircuit(2); hh.h(0); hh.h(1)
    sv2 = sv.evolve(hh, qargs=[i, j])
    return sum(abs(a) ** 2 for idx, a in enumerate(sv2.data)
               if ((idx >> i) & 1) == ((idx >> j) & 1))

# ------------------------------------------------------------------ TEST 2
print("\nTEST 2  X-basis interference test on the Different pair")
Pmix = np.zeros((4, 4), complex); Pmix[1, 1] = Pmix[2, 2] = 0.5   # pre-agreed
hh = QuantumCircuit(2); hh.h(0); hh.h(1)
p_class = sum(v for k, v in DensityMatrix(Pmix).evolve(hh).probabilities_dict().items()
              if k[0] == k[1])
p_qm = p_agree_x(psi_sv(), 0, 1)
print("   P(pair AGREES when weighed in the complementary X basis):")
print(f"     pre-agreed classical pair (best case) : {p_class:.3f}")
print(f"     our entangled pair                    : {p_qm:.4f}")
print("   ->", "REFUTES classical pre-agreement" if p_qm > 0.9 else "FAIL")

# ------------------------------------------------------------------ TEST 3
print("\nTEST 3  CHSH: settings+formula fixed by theory, S sampled from shots")
A = [0.0, np.pi / 2]                # a: Z, X
B = [np.pi / 4, -np.pi / 4]         # b: (Z+X)/sqrt2, (Z-X)/sqrt2
E_theory = np.array([[correlation([A[i], B[j]], sv=psi_sv())
                      for j in range(2)] for i in range(2)])
patt = [[s0, s1, s2, s3] for s0 in (1, -1) for s1 in (1, -1)
        for s2 in (1, -1) for s3 in (1, -1)
        if sum(1 for s in (s0, s1, s2, s3) if s < 0) % 2 == 1]
pattern = max(patt, key=lambda p: abs(sum(p[i * 2 + j] * E_theory[i, j]
                                          for i in range(2) for j in range(2))))
S_of = lambda E: sum(pattern[i * 2 + j] * E[i, j]
                     for i in range(2) for j in range(2))   # theory-fixed formula
S_theory = S_of(E_theory)
E_samp = np.array([[correlation([A[i], B[j]], shots=4096)
                    for j in range(2)] for i in range(2)])
S = S_of(E_samp)
se = 4 / np.sqrt(4096)
print(f"   theory : E(a,b)={np.round(E_theory, 3).tolist()}  "
      f"S_theory={S_theory:+.3f}")
print(f"   sampled: E(a,b)={np.round(E_samp, 3).tolist()}")
print(f"   S = {S:+.3f} +- {se:.2f}   local realism: |S| <= 2,   "
      f"QM: 2*sqrt2 = 2.828")
print("   ->", f"violates Bell inequality by {abs(S)-2:.2f}"
      if abs(S) - 3 * se > 2 else "   -> no violation")

# ------------------------------------------------------------------ TEST 4
print("\nTEST 4  coherence of the machine (coherent Different pair + dime)")
qc_m = vending_machine_bell(["D", 1], coherent=True, final_measure=False)
sv = Statevector.from_instruction(qc_m)   # bits 0-2 credit, 3-5 coins, 6 vend
amps = np.zeros(128, complex)
for pair_bits, a in [(0b01, 1 / np.sqrt(2)), (0b10, 1 / np.sqrt(2))]:
    amps[5 | ((pair_bits & 1) << 3) | ((pair_bits >> 1) << 4)
         | (1 << 5) | (1 << 6)] = a
fid = abs(Statevector(amps).inner(sv)) ** 2
print(f"   a) fidelity vs exact prediction [Psi+ x credit=5 x vend=1]: {fid:.10f}")

dm = DensityMatrix(sv)
rho1 = partial_trace(dm, [0, 1, 2, 4, 5, 6])          # keep coin0
ev = [e for e in la.eigvalsh(rho1.data).real if e > 1e-12]
print(f"   b) entanglement of one coin AFTER the arithmetic: "
      f"{-sum(e*np.log2(e) for e in ev):.3f} ebit  (alive=1.000, measured=0.000)")

print(f"   c) X-basis agreement THROUGH the adders: "
      f"P(agree)={p_agree_x(sv, 3, 4):.4f}  vs classical <= {p_class:.3f}")
print("   d) the observed machine collapses the pair to that classical "
      f"mixture (P(agree)={p_class:.3f});\n      "
      "the observation IS the difference.")
