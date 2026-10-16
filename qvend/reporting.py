"""Human-readable readouts of machine runs."""

UNIT_CENTS = 5


def _parse(bits):
    """counts key = '<result> <coin_meas>'; result = [vend q2 q1 q0] MSB-first."""
    final, meas = (bits.split() + [""])[:2]
    return final[0], int(final[1:], 2), meas


def report(counts, title=""):
    """Print shot statistics from a run of any of the machines."""
    if title:
        print(f"\n=== {title} ===")
    total = sum(counts.values())
    for bits, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        vend, credit, meas = _parse(bits)
        coffee = "COFFEE!" if vend == "1" else "(no coffee)"
        line = (f"  credit={credit} ({credit*UNIT_CENTS:2d}c)  {coffee:11s}"
                f"  {n:5d}/{total} shots")
        if meas:
            line += f"   coins={meas}"
        print(line)


def report_statevector(sv, n_coins, title=""):
    """Print the exact amplitudes of a measurement-free machine state."""
    if title:
        print(title)
    print("  label: vend | coin_n ... coin1 | q2 q1 q0   (left -> right)")
    for label, p in sorted(sv.probabilities_dict().items(), key=lambda kv: -kv[1]):
        if p < 1e-9:
            continue
        vend = label[0]
        coins = label[1:1 + n_coins][::-1]
        credit = int(label[1 + n_coins:4 + n_coins], 2)
        coffee = "COFFEE!" if vend == "1" else ""
        print(f"  coins={coins}  credit={credit} ({credit*UNIT_CENTS:2d}c)"
              f"  P={p:.4f}  {coffee}")
