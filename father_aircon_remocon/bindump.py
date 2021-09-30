#!/usr/bin/env python
import sys

line_1 = []
line_2 = []

hexs = sys.argv[1]
for hex in hexs.split(", "):
    bin8 = "{:08b}".format(int(hex, 0))
    line_1.append("     " + hex)
    line_2.append(bin8[0:4] + " " + bin8[4:8])

print(" ".join(line_1) + "\n" + " ".join(line_2))
