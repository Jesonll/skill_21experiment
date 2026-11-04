#!/usr/bin/env python3
"""Generate oscilloscope waveform CSVs for pgfplots.

Three bias conditions of a common-emitter stage:
  normal     : clean sine, output inverted
  saturation : output clipped at the bottom (NPN, Q point too high)
  cutoff     : output clipped at the top    (NPN, Q point too low)

The input amplitude comes from the scope's RMS reading (A = sqrt(2)*U_rms).
The output peak is the unclipped peak read from the photo, and the clip
level is measured there too; the printed RMS is a check against the
displayed value (clipping lowers RMS below sqrt(2)*peak). CSV uses LF endings on purpose: CRLF breaks
pgfplots column detection.

Usage:
  python3 scope_waveforms.py --out data
"""
import argparse
import csv
import math
import os

F = 1.0 / 1.06e-3          # ~940 Hz, period 1.06 ms
T_END = 1.6e-3             # just over 1.5 periods


def build(name, ui_rms_mv, uo_peak_v, mode=None, clip=None, out="data"):
    """uo_peak_v is the peak of the underlying sine (before clipping)."""
    os.makedirs(out, exist_ok=True)
    ui_amp = math.sqrt(2) * ui_rms_mv * 1e-3
    uo_amp = uo_peak_v
    n = 400
    rows = []
    for i in range(n + 1):
        t = T_END * i / n
        ui = ui_amp * math.sin(2 * math.pi * F * t)
        uo = -uo_amp * math.sin(2 * math.pi * F * t)
        if mode == "bottom":
            uo = max(uo, clip)
        elif mode == "top":
            uo = min(uo, clip)
        rows.append((t * 1e3, ui * 1e3, uo))

    path = os.path.join(out, name + ".csv")
    with open(path, "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["t", "ui", "uo"])
        for t, ui, uo in rows:
            w.writerow([f"{t:.4f}", f"{ui:.3f}", f"{uo:.4f}"])

    uo_vals = [r[2] for r in rows]
    rms = math.sqrt(sum(v * v for v in uo_vals) / len(uo_vals))
    pp = max(uo_vals) - min(uo_vals)
    print(f"{name:11s} ui_pp={2*ui_amp*1e3:5.1f} mV  "
          f"uo_pp={pp:4.2f} V  uo_rms={rms:4.2f} V  -> {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data")
    a = ap.parse_args()
    build("normal", 9.71, 1.29 * math.sqrt(2), out=a.out)
    build("saturation", 9.02, 2.80, mode="bottom", clip=-1.35, out=a.out)
    build("cutoff", 19.7, 0.92, mode="top", clip=0.82, out=a.out)
