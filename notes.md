# SENSE-LAB lab notes

## E1.1 Accuracy sweep

### Question
How do the naive and calibrated conversions differ across the range, and where does the ADC clip?

### Predict (written before capturing)
- Gap in the middle (raw 300-3000): ~22 mV
- Gap crosses zero near raw 0 (meant the upper crossing; see check)
- Max gap: ~100 mV at raw 4095
- Clip level: ~3100 mV
- Averaging 8 reads: error bars shrink ~2.8x (1/sqrt(N))
- Up and down passes overlap because there is no capacitor

### Setup
- N_AVG = 8, PERIOD_US = 4000 (250 Hz), no capacitor, ~18 s sweep up then down
- Files: data/e1-1.csv, figures/e1-1.png | measured fs: 250 Hz
- Extra: data/e1-1_fastrun.csv (N_AVG = 1, 1 kHz, single 2 s sweep)

### Result
| Item | Value |
|---|---|
| Clipped rows | 3063 (25.5%) |
| Clip level | 3098 mV |
| Mid-range gap (raw 300-3000) | -23.1 mV |
| Upper zero crossing | raw ~3145 |
| Max gap | 201 mV at raw 4093 |
| Up vs down mid-range gap | -22.8 vs -23.3 mV |
| Scatter N=8 vs N=1 | 3.13 vs 3.11 mV (predicted 2.8x smaller) |

### Why
- Mid gap: gap builds in the first ~500 counts (0 to -22 mV), then constant; calibrated is steeper at the bottom (~0.86 vs 0.805 mV/count)
- Bend above ~2.4 V is ADC compression; clip at 3098 mV is saturation
- Calibrated is factory-corrected, not true; only a reference (multimeter) can say what is true

### Prediction check
- Mid gap ~22: right (-23.1) | Clip ~3100: right (3098)
- Zero crossing "near 0": wrong, I meant the upper crossing; actual raw 3145
- Max gap ~100: wrong, actual 201 mV
- Error bars 2.8x smaller: wrong, 3.13 vs 3.11 mV
- Up/down overlap: right, wrong reason (ADC has no memory, knob has no backlash)

### Mistakes and surprises
- Plot script had n = 8 while the sketch had N_AVG = 1: both axes shrunk 8x
- Notes had Predict and Result swapped for max gap; fixed in a later commit

### Open question
- sqrt(8) prediction not confirmed; about half the scatter repeats between up and down passes (corr 0.51), so it is systematic. E1.2 and E1.5 will test the rest.

### Next
- How noisy is one reading when the knob is still? (E1.2)
