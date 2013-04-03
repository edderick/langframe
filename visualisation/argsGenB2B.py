#!/usr/bin/python

# short & sweet script to generate the args needed for
# language_distance.R for AB training

iterations=15
skip=1

print " ".join(["langL_%d,langL_%d" % (i,i+1) for i in range(0,iterations-1,skip)])
