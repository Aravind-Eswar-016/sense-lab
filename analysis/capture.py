import serial, time, sys, numpy as np

port, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]

hdr = sys.argv[4] if len(sys.argv) > 4 else "time_us,raw_sum,mV_sum"

ser = serial.Serial(port, 921600, timeout=1)
time.sleep(2); ser.reset_input_buffer()

rows = []
while len(rows) < n:
    p = ser.readline().decode(errors="ignore").strip().split(",")
    if len(p) == 3 and all(x.isdigit() for x in p):
        rows.append([int(x) for x in p])

d = np.array(rows)
np.savetxt(out, d, delimiter="," , fmt="%d", header=hdr, comments="")
fs = 1e6 / np.median(np.diff(d[:, 0]))

print(f"saved {len(d)} rows -> {out} | measured fs = {fs:.0f} Hz")
ser.close()