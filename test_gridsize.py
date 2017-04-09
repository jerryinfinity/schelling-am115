'''
AM 115 Project 2
This file contains experiments to test varying grid sizes, dimensions, and vision
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import itertools
import pickle
import core

### varying n ###
ns = [10,20,50,100]
trials = 20
results_list = []
segcoeffs_list = []
unhappys_list = []
trial_num = []
print "Number of trials for each n:",trials
for n in ns:
	for t in range(trials):
		trial_num.append(n+t*1./trials)
		[results,segcoeffs,unhappys] = core.run(n=n,max_iter=50)
		while len(unhappys)==50:
			[results,segcoeffs,unhappys] = core.run(n=n,max_iter=50)
		results_list.append(results)
		segcoeffs_list.append(segcoeffs)
		unhappys_list.append(unhappys)
		print '%.2f' % trial_num[-1]

print "Number of steps until equilibrium"
unhappys_len = [len(unhappys_list[i]) for i in range(len(unhappys_list))]
unhappys_mean = [np.mean(unhappys_len[trials*k:trials*(k+1)]) for k in range(len(ns))]
unhappys_std = [np.std(unhappys_len[trials*k:trials*(k+1)]) for k in range(len(ns))]
print('\n'.join('{}: mean {:.3f}, std {:.3f}'.format(ns[k],unhappys_mean[k],unhappys_std[k]) for k in range(len(ns))))

segcoeffs_final = [segcoeffs_list[i][-1] for i in range(len(segcoeffs_list))]
print "Average segregation at equilibrium"
seg_mean = [np.mean(segcoeffs_final[trials*k:trials*(k+1)]) for k in range(len(ns))]
seg_std = [np.std(segcoeffs_final[trials*k:trials*(k+1)]) for k in range(len(ns))]
print('\n'.join('{}: mean {:.3f}, std {:.3f}'.format(ns[k],seg_mean[k],seg_std[k]) for k in range(len(ns))))

file = open("test_n","w")
pickle.dump([ns,trials,results_list,segcoeffs_list,unhappys_list,trial_num,segcoeffs_final],file)
file.close()

# Plotting number of unhappy people over time for various values of n
plt.figure(1)
plt.xlabel("Time")
plt.ylabel("Number of unhappy people")
plt.title("Number of unhappy people over time for various values of n")
colors = cm.rainbow(np.linspace(0, 1, len(ns)))
for n in range(len(ns)):
	for t in range(trials):
		i = trials*n+t
		plt.plot(unhappys_list[i],label=trial_num[i],c=colors[n])
plt.savefig("unhappyvtime_n.png")

# Plotting segregation over time for various values of n
plt.figure(2)
plt.xlabel("Time")
plt.ylabel("Segregation Coefficient")
plt.title("Segregation over time for various values of n")
for n in range(len(ns)):
	for t in range(trials):
		i = trials*n+t
		plt.plot(segcoeffs_list[i],label=trial_num[i],c=colors[n])
plt.savefig("segvtime_n.png")

# Plotting number of steps until equilibrium against n

plt.figure(3)
plt.xlabel("n")
plt.ylabel("Steps until equilibrium")
plt.title("Steps until equilibrium over n")
plt.errorbar(ns,unhappys_mean,yerr=unhappys_std,fmt='-o')
plt.xlim(0,ns[-1]+ns[0])
plt.savefig("stepsvn.png")

# Plotting segregation at equilibrium against n
plt.figure(4)
plt.xlabel("n")
plt.ylabel("Segregation Coefficient")
plt.title("Segregation coefficient over n")
plt.errorbar(ns,seg_mean,yerr=seg_std,fmt='-o')
plt.xlim(0,ns[-1]+ns[0])
plt.savefig("segvn.png")









