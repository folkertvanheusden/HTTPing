#! /usr/bin/python

import sys
import json
import os
import math

fin = sys.argv[1]

print "Loading from %s" % (fin)

fh = open(fin)
json_data = json.load(fh)

print "Number of rows: %d" % (len(json_data))

fdata = fin + ".dat"
print "Writing data to %s" % (fdata)

data_fh = open(fdata, "w")

host='?'

total=0
total_sd=0
n=0
avg=0
sd=0
minp = 999999999
maxp = -minp

for row in json_data:
	if row['status'] == '1':
		val = float(row['total_s'])
		data_fh.write("%f %f\n" % (float(row['start_ts']), val))
		host=row['host']
		total += val
		total_sd += val * val
		n += 1
		if val > maxp:
			maxp = val
		if val < minp:
			minp = val

print "Rows ignored: %d" % (len(json_data) - n)

data_fh.close()

if n > 0:
	avg = total / n
	sd = math.sqrt((total_sd / n) - math.pow(avg, 2.0))

print "Average ping time: %fs (%d pings)" % (avg, n)
print "Standard deviation: %fs" % (sd)
print "Minimum ping value: %fs" % (minp)
print "Maximum ping value: %fs" % (maxp)

fscript = fin + ".sh"
print "Writing script to %s" % (fscript)

fpng = fin + ".png"

script_fh = open(fscript, "w")

script_fh.write("#! /bin/sh\n\n")
script_fh.write("gnuplot <<EOF > " + fpng + "\n")
script_fh.write("set term png size 800,600 tiny\n")
script_fh.write("set autoscale\n")
script_fh.write("set timefmt \"%s\"\n")
script_fh.write("set xdata time\n")
script_fh.write("set format x \"%H:%M:%S\"\n")
script_fh.write("plot \"" + fdata + "\" using 1:2 with lines title \"" + host + "\"\n")
script_fh.write("EOF\n")

os.chmod(fscript, 0755)
script_fh.close()

print "Now invoke %s to generate %s" % (fscript, fpng)
