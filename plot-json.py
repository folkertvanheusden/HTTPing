#!/usr/bin/env python3

import json
import math
import os
import stat
import sys

fin = sys.argv[1]

print(f"Loading from {fin}")

fh = open(fin)
json_data = json.load(fh)

print(f"Number of rows: {len(json_data)}")

fdata = fin + ".dat"
print(f"Writing data to {fdata}")

data_fh = open(fdata, "w")

host = "?"

total = 0
total_sd = 0
n = 0
avg = 0
sd = 0
minp = 999999999
maxp = -minp

for row in json_data:
    if row["status"] == "1":
        val = float(row["total_s"])
        data_fh.write("%f %f\n" % (float(row["start_ts"]), val))
        host = row["host"]
        total += val
        total_sd += val * val
        n += 1
        if val > maxp:
            maxp = val
        if val < minp:
            minp = val

print(f"Rows ignored: {len(json_data) - n}")

data_fh.close()

if n > 0:
    avg = total / n
    sd = math.sqrt((total_sd / n) - math.pow(avg, 2.0))

print(f"Average ping time: {avg}s ({n} pings)")
print(f"Standard deviation: {sd}s")
print(f"Minimum ping value: {minp}s")
print(f"Maximum ping value: {maxp}s")

fscript = fin + ".sh"
print(f"Writing script to {fscript}")

fpng = fin + ".png"

with open(fscript, "w") as script_fh:
    script_fh.write("#! /bin/sh\n\n")
    script_fh.write("gnuplot <<EOF > " + fpng + "\n")
    script_fh.write("set term png size 800,600 tiny\n")
    script_fh.write("set autoscale\n")
    script_fh.write('set timefmt "%s"\n')
    script_fh.write("set xdata time\n")
    script_fh.write('set format x "%H:%M:%S"\n')
    script_fh.write('plot "' + fdata + '" using 1:2 with lines title "' + host + '"\n')
    script_fh.write("EOF\n")

    os.chmod(
        fscript,
        stat.S_IREAD
        | stat.S_IWRITE
        | stat.S_IEXEC
        | stat.S_IRGRP
        | stat.S_IXGRP
        | stat.S_IROTH
        | stat.S_IXOTH,
    )

print(f"Now invoke {fscript} to generate {fpng}")
