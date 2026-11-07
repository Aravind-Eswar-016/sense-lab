import sys, pandas as pd, numpy as np, matplotlib.pyplot as plt

path, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
d = pd.read_csv(path)
d["raw"] = d.raw_sum / n
d["mV"] = d.mV_sum / n
d["pass"] = np.where(d.index < len(d) // 2, "up", "down")
live = d[(d.raw > 1) & (d.raw < 4094)].copy()            # drop the clipped plateaus
live["naive"] = live.raw / 4095 * 3300
live["gap"] = live.naive - live.mV

bins = pd.cut(live.raw, np.arange(0, 4160, 128))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), constrained_layout=True)
ax[0].plot(live.raw, live.naive, ".", ms=1.5, label="naive  raw/4095 x 3300")
ax[0].plot(live.raw, live.mV, ".", ms=1.5, label="calibrated (analogReadMilliVolts)")
ax[0].set(xlabel=f"raw count (mean of {n})", ylabel="mV", title="Conversion"); ax[0].grid(alpha=.3)
ax[0].legend(markerscale=6, fontsize=8)
for name, c in (("up", "tab:blue"), ("down", "tab:red")):
    g = live[live["pass"] == name].groupby(bins[live["pass"] == name], observed=True)
    ax[1].errorbar(g.raw.mean(), g.gap.mean(), yerr=g.gap.std(), fmt="o-", ms=3, capsize=2, color=c, label=name)
ax[1].axhline(0, c="k", lw=.8); ax[1].grid(alpha=.3); ax[1].legend()
ax[1].set(xlabel=f"raw count (mean of {n})", ylabel="naive - calibrated (mV)", title="Gap, binned mean +/- 1 sigma")
plt.savefig(out, dpi=170)

g = live.groupby(bins, observed=True); x, m = g.raw.mean(), g.gap.mean()
mid = live[(live.raw >= 300) & (live.raw <= 3000)]

print(f"rows {len(d)} | fs {1e6 / d.time_us.diff().median():.0f} Hz")
print(f"clipped rows {len(d) - len(live)} ({(len(d) - len(live)) / len(d):.1%}) | clip level {d.mV.max():.0f} mV")
print(f"mid-range (raw 300-3000) mean gap {mid.gap.mean():.1f} mV")
fine = live[(live.raw > 2800) & (live.raw < 3500)]
gf = fine.groupby(pd.cut(fine.raw, np.arange(2800, 3500, 50)), observed=True).gap.mean()
print("gap crosses zero near raw", np.interp(0, gf.values, [iv.mid for iv in gf.index]))
print(f"max gap {live.gap.max():.0f} mV at raw {live.raw[live.gap.idxmax()]:.0f}")
print(f"up vs down mid-range gap: {mid[mid['pass']=='up'].gap.mean():.1f} vs {mid[mid['pass']=='down'].gap.mean():.1f} mV")