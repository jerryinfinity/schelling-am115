'''
AM 115 Project 2
This file contains experiments to test varying grid sizes, dimensions, and vision
'''

import numpy as np
import matplotlib.pyplot as plt
import itertools
import core

### varying n ###
ns = [5,10,20]
trials = 3
results_list = []
segcoeffs_list = []
unhappys_list = []
trial_num = []
for n in ns:
	for t in range(trials):
		trial_num.append(n+t/10.)
		[results,segcoeffs,unhappys] = core.run(n=n)
		results_list.append(results)
		segcoeffs_list.append(segcoeffs)
		unhappys_list.append(unhappys)
	print n

print "Number of steps until equilibrium"
print [len(x) for x in unhappys_list]

# Plotting number of unhappy people over time for various values of n
plt.figure(1)
plt.xlabel("Time")
plt.ylabel("Number of unhappy people")
plt.title("Number of unhappy people over time for various values of n")
for i in enumerate(unhappys_list):
    plt.plot(unhappys_list[i],label=trial_num[i])
plt.legend()
plt.show()

# Plotting segregation over time for various values of n
plt.figure(1)
plt.xlabel("Time")
plt.ylabel("Segregation Coefficient")
plt.title("Segregation over time for various values of n")
for i in enumerate(segcoeffs_list):
    plt.plot(segcoeffs_list[i],label=trial_num[i])
plt.legend()
plt.show()








