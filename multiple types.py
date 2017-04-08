"""
This file contains experiments using more than 2 types of agents.
"""

from core import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm


n = 20 # this is n, grid size (nxnx...xn), d times
d = 2 # this is d, number of dimensions (d<=10) 
v = 1 # this is v Note: if v=1, then we care about 3x3 squares
m = 2 # this is m, number of types; type 1,2,...,m
popdist = np.array([0.6, 0.4]) # proportion of each type
rho = 0.7 # this is rho, population density

# m x m matrices
lo_thres = np.matrix([[0.33,0.],[0.,0.33]])
hi_thres = np.matrix([[1,1],[1,1]])

# number of iterations
max_iter = 200


# Number of unhappy people over time 
def unhappiness_over_time():
    unhappy_iterations = {}
    lowest = 2; highest = 8
    for i in range(lowest,highest + 1):
        m = i
        popdist = np.ones(m)/m
        results = [gridinit()]
        unhappy_list = []
        for cnt in xrange(max_iter):
            oldgrid = results[cnt]
            num_unhappy, newgrid = movegrid(oldgrid)
            if num_unhappy > 0:
                unhappy_list.append(num_unhappy)
                results.append(newgrid)
                cnt += 1
            else:
                break
        unhappy_iterations[i] = unhappy_list

    # Plotting number of unhappy people over time for various values of m
    plt.figure(1)
    plt.xlabel("Number of unhappy people")
    plt.ylabel("Iterations")
    plt.title("Number of unhappy people over time for various values of m")
    for key in unhappy_iterations.keys():
        plt.plot(unhappy_iterations[key], label=key)
    plt.legend()
    plt.show()

# Number of unhappy people over time 
def iterations_to_completion():
    lowest = 2; highest = 8
    repetitions = 5
    num_iterations = {}
    for j in range(lowest, highest + 1):
        num_iterations[j] = []
    for s in range(repetitions):
        for i in range(lowest,highest + 1):
            m = i
            popdist = np.ones(m)/m
            results = [gridinit()]
            unhappy_list = []
            for cnt in xrange(max_iter):
                oldgrid = results[cnt]
                num_unhappy, newgrid = movegrid(oldgrid)
                if num_unhappy > 0:
                    unhappy_list.append(num_unhappy)
                    results.append(newgrid)
                    cnt += 1
                else:
                    break
            num_iterations[i].append(len(unhappy_list))


    plt.figure(1)
    plt.xlabel("Number of agent types")
    plt.ylabel("Time to convergence")
    plt.title("Time to convergence vs m")
    colors = cm.rainbow(np.linspace(0, 1, highest-lowest+1))
    color_count = 0
    for key in num_iterations.keys():
        plt.scatter([key] * repetitions, num_iterations[key], color = colors[color_count], label=key)
        color_count += 1
        plt.scatter(key, np.average(num_iterations[key]), color = "black", s=40)
    plt.legend()
    plt.show()


def main():
    # RUN YOUR SIMULATION HERE
    iterations_to_completion()


if __name__ == "__main__":
    main()