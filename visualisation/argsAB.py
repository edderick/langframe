#!/usr/bin/python

# short & sweet script to generate the args needed for
# language_distance.R for AB training

iterations=25
skip=1

print " ".join(["langA,langB_%d" % i for i in range(0,iterations,skip)])
