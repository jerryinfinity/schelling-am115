# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import itertools


n = 8 # this is n, grid size (nxnx...xn), d times
d = 2 # this is d, number of dimensions (d<=10) 
v = 1 # this is v Note: if v=1, then we care about 3x3 squares
m = 2 # this is m, number of types; type 1,2,...,m
popdist = np.array([0.6, 0.4]) # proportion of each type
rho = 0.7 # this is rho, population density

# m x m matrices
lo_thres = np.matrix([[0.33,0.],[0.,0.33]])
hi_thres = np.matrix([[1,1],[1,1]])

# number of iterations
num_iter = 100


# construct a grid
def gridinit():
    assert len(popdist) == m
    grid = np.searchsorted(1-rho+np.insert(np.cumsum(rho*popdist),0,0.,axis=0),np.random.uniform(size=n**d))
    return grid

def pos_int2arr(pos):
    posarr = [int(x) for x in np.base_repr(pos,base=n)]
    posarr = np.array([0]*(d-len(posarr)) + posarr)
    return posarr
    
def pos_arr2int(posarr):
    return np.sum(np.array(posarr)*np.array([n**(d-1-i) for i in xrange(d)]))

# input position pos is an integer, no neet to input grid since we only return indices
def getneighbors(pos,topology="grid"):
    if topology == "grid":
        # this only works with d <= 10, but larger d is not computationally feasible anyways
        ans = []        
        posarr = pos_int2arr(pos)
        offsets = itertools.product(*([range(-v,v+1)]*d))
        for offset in offsets:
            resarr = posarr + offset
            if (resarr >= 0).all() and (resarr <= n-1).all():
                resint = pos_arr2int(resarr)
                if resint != pos:
                    ans.append(resint)
        return ans

# I didn't directly use this but I'm sure it'd be useful.
def typecount(grid):
    # index 0 = number of empty cells, index i=1 to m = number of type i cells
    return np.array([sum(grid==i) for i in xrange(m+1)])

def ishappy(grid,pos):
    curr_type = grid[pos]
    if curr_type == 0:
        return True
    neighbors = grid[getneighbors(pos)]
    neighbors = neighbors[neighbors > 0]
    # alone = happy
    if len(neighbors) == 0:
        return True
    else:
        # not alone
        for neighbor_type in range(1,m+1):            
            ratio = sum(neighbors==neighbor_type)*1./len(neighbors)
            if ratio > hi_thres[curr_type-1,neighbor_type-1] or ratio < lo_thres[curr_type-1,neighbor_type-1]:
                return False
        return True

# return a new grid after agents move
def movegrid(grid):
    unhappy_enum = []
    unhappy_indices = []
    for pos in xrange(len(grid)):
        if not ishappy(grid,pos):
            unhappy_enum.append(grid[pos])
            unhappy_indices.append(pos)
    grid[unhappy_indices] = 0
    empty_spots = np.where(grid==0)[0]
    enum_with_dummies = unhappy_enum + [0]*(len(empty_spots)-len(unhappy_enum))
    enum_with_dummies = np.random.permutation(enum_with_dummies)
    grid[empty_spots] = enum_with_dummies
    # return number of unhappy people and new grid
    return (len(unhappy_indices), grid)
    


# print grid
def printgrid(grid):
    print grid.reshape((n,)*d)


def example():
    # example, we track number of unhappy people, we get [10, 4, 1, 1, 1, 1, 1, 1, 1] 
    # terminates in 9 steps
    # final result is
    #[[2 2 0 2 1 1 0 1]
    # [0 2 2 2 0 1 0 1]
    # [0 2 2 2 1 0 1 1]
    # [2 0 2 0 1 0 1 1]
    # [2 0 0 1 1 1 1 0]
    # [2 2 2 2 1 1 1 1]
    # [2 0 2 0 2 2 2 0]
    # [0 0 0 0 0 0 2 0]]
    # which is completely segregated
    results = [gridinit()]
    unhappy_list = []
    for cnt in xrange(num_iter):
        oldgrid = results[cnt]
        num_unhappy, newgrid = movegrid(oldgrid)
        if num_unhappy > 0:
            unhappy_list.append(num_unhappy)
            results.append(newgrid)
            cnt += 1
        else:
            break

def main():
    # RUN YOUR SIMULATION HERE
    example()




if __name__ == "__main__":
    main()
    
        
printgrid(gridinit())
