import pandas as pd, numpy as np, sys

d = pd.read_csv(sys.argv[1]); n = int(sys.argv[2])

raw, mv = d.raw_sum / n, d.mV_sum / n

print(f"fs = {1e6 / d.time_us.diff().median():.0f} Hz")
print(f"raw: mean {raw.mean():.2f}  std {raw.std():.2f} LSB  p-p {np.ptp(raw):.1f}")
print(f"mV : mean {mv.mean():.1f}  std {mv.std():.2f} mV")