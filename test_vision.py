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

### varying v ###
ds = [1,2,3]
trials = 20
results_list = []
segcoeffs_list = []
unhappys_list = []
trial_num = []
print "Number of trials for each v:",trials
for d in ds:
	for t in range(trials):
		trial_num.append(d+t*1./trials)
		[results,segcoeffs,unhappys] = core.run(n=20,v=d)
		while len(unhappys)==200:
			[results,segcoeffs,unhappys] = core.run(n=20,v=d)
		results_list.append(results)
		segcoeffs_list.append(segcoeffs)
		unhappys_list.append(unhappys)
		print '%.2f' % trial_num[-1]

print "Number of steps until equilibrium"
unhappys_len = [len(unhappys_list[i]) for i in range(len(unhappys_list))]
unhappys_mean = [np.mean(unhappys_len[trials*k:trials*(k+1)]) for k in range(len(ds))]
unhappys_std = [np.std(unhappys_len[trials*k:trials*(k+1)]) for k in range(len(ds))]
print('\n'.join('{}: mean {:.3f}, std {:.3f}'.format(ds[k],unhappys_mean[k],unhappys_std[k]) for k in range(len(ds))))

segcoeffs_final = [segcoeffs_list[i][-1] for i in range(len(segcoeffs_list))]
print "Average segregation at equilibrium"
seg_mean = [np.mean(segcoeffs_final[trials*k:trials*(k+1)]) for k in range(len(ds))]
seg_std = [np.std(segcoeffs_final[trials*k:trials*(k+1)]) for k in range(len(ds))]
print('\n'.join('{}: mean {:.3f}, std {:.3f}'.format(ds[k],seg_mean[k],seg_std[k]) for k in range(len(ds))))

file = open("test_v","w")
pickle.dump([ds,trials,results_list,segcoeffs_list,unhappys_list,trial_num,segcoeffs_final],file)
file.close()

# Plotting number of unhappy people over time for various values of v
plt.figure(1)
plt.xlabel("Time")
plt.ylabel("Number of unhappy people")
plt.title("Number of unhappy people over time for various values of v")
colors = cm.rainbow(np.linspace(0, 1, len(ds)))
for d in range(len(ds)):
	for t in range(trials):
		i = trials*d+t
		plt.plot(unhappys_list[i],label=trial_num[i],c=colors[d])
plt.savefig("unhappyvtime_v.png")

# Plotting segregation over time for various values of v
plt.figure(2)
plt.xlabel("Time")
plt.ylabel("Segregation Coefficient")
plt.title("Segregation over time for various values of v")
for d in range(len(ds)):
	for t in range(trials):
		i = trials*d+t
		plt.plot(segcoeffs_list[i],label=trial_num[i],c=colors[d])
plt.savefig("segvtime_v.png")

# Plotting number of steps until equilibrium against v

plt.figure(3)
plt.xlabel("Vision")
plt.ylabel("Steps until equilibrium")
plt.title("Steps until equilibrium over v")
plt.errorbar(ds,unhappys_mean,yerr=unhappys_std,fmt='-o')
plt.xlim(0,ds[-1]+ds[0])
plt.savefig("stepsvv.png")

# Plotting segregation at equilibrium against v
plt.figure(4)
plt.xlabel("Vision")
plt.ylabel("Segregation Coefficient")
plt.title("Segregation coefficient over v")
plt.errorbar(ds,seg_mean,yerr=seg_std,fmt='-o')
plt.xlim(0,ds[-1]+ds[0])
plt.savefig("segvv.png")









