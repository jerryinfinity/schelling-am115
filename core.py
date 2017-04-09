import numpy as np
import itertools


''' Setting up the model '''
# construct a grid
def gridinit(popdist,rho,n=10,d=2,m=2):
    assert len(popdist) == m
    grid = np.searchsorted(1-rho+np.insert(np.cumsum(rho*popdist),0,0.,axis=0),np.random.uniform(size=n**d))
    return grid

def pos_int2arr(pos,n=10,d=2):
    posarr = []
    while pos>0:
        posarr.insert(0,pos%n)
        pos = pos/n
    posarr = np.array([0]*(d-len(posarr)) + posarr)
    return posarr
    
def pos_arr2int(posarr,n=10,d=2):
    return np.sum(np.array(posarr)*np.array([n**(d-1-i) for i in xrange(d)]))

# input position pos is an integer, no neet to input grid since we only return indices
def getneighbors(pos,nhoodsize,topology="grid",n=10,d=2):
    if topology == "grid":
        # this only works with d <= 10, but larger d is not computationally feasible anyways
        ans = []        
        posarr = pos_int2arr(pos,n,d)
        offsets = itertools.product(*([range(-nhoodsize,nhoodsize+1)]*d))
        for offset in offsets:
            resarr = posarr + offset
            if (resarr >= 0).all() and (resarr <= n-1).all():
                resint = pos_arr2int(resarr,n,d)
                if resint != pos:
                    ans.append(resint)
        return ans

# I didn't directly use this but I'm sure it'd be useful.
def typecount(grid,m=2):
    # index 0 = number of empty cells, index i=1 to m = number of type i cells
    return np.array([sum(grid==i) for i in xrange(m+1)])

def ishappy(grid,pos,n=10,d=2,v=1,m=2,hi_thres=np.matrix([[1,1],[1,1]]),lo_thres = np.matrix([[0.33,0.],[0.,0.33]])):
    curr_type = grid[pos]
    if curr_type == 0:
        return True
    neighbors = grid[getneighbors(pos=pos,nhoodsize=v,n=n,d=d)]
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
def movegrid(grid,n=10,d=2,v=1,m=2,hi_thres=np.matrix([[1,1],[1,1]]),lo_thres = np.matrix([[0.33,0.],[0.,0.33]])):
    unhappy_enum = []
    unhappy_indices = []
    for pos in xrange(len(grid)):
        if not ishappy(grid,pos,n=n,d=d,v=v,m=m,hi_thres=hi_thres,lo_thres = lo_thres):
            unhappy_enum.append(grid[pos])
            unhappy_indices.append(pos)
    grid[unhappy_indices] = 0
    empty_spots = np.where(grid==0)[0]
    enum_with_dummies = unhappy_enum + [0]*(len(empty_spots)-len(unhappy_enum))
    enum_with_dummies = np.random.permutation(enum_with_dummies)
    grid[empty_spots] = enum_with_dummies
    # return number of unhappy people and new grid
    return (len(unhappy_indices), grid)
    
def neighborhood_sizes(grid,m=2,n=10,d=2):
    seen = set()
    ret = {t: [] for t in xrange(m+1)}
    while len(seen) != len(grid):
        x = set(range(len(grid))) - seen        
        queue = [list(x)[0]]
        seen.add(queue[0])
        nhood_size = 1
        while len(queue) > 0:
            ele = queue.pop()
            for idx in getneighbors(ele, 1,n=n,d=d):
                if (idx not in seen) and (grid[ele] == grid[idx]):
                    seen.add(idx)
                    queue.append(idx)
                    nhood_size += 1
        # add to dictionary
        ret[grid[ele]].append(nhood_size)
    return ret

# print grid
def printgrid(grid,n=10,d=2):
    print grid.reshape((n,)*d)

# calculates segregation based on average size
def calc_seg(grid,nhoodsize=1,n=10,d=2):
	segcoeff = np.array([])
	for pos in xrange(len(grid)):
		curr_type = grid[pos]
		neighbors = grid[getneighbors(pos,nhoodsize,n=n,d=d)]
		neighbors = neighbors[neighbors > 0]
		if curr_type == 0:
			segcoeff = np.append(segcoeff,[-1])
		elif len(neighbors) == 0:
			segcoeff = np.append(segcoeff,[1])
		else:
			ratio = sum(neighbors==curr_type)*1./len(neighbors)
			segcoeff = np.append(segcoeff,[ratio])
	return np.mean(segcoeff[segcoeff>-1])

''' Running the model '''
def run(n=10,d=2,v=1,m=2,popdist=np.array([0.6, 0.4]),rho=0.8,lo_thres=np.matrix([[0.33,0.],[0.,0.33]]),hi_thres=np.matrix([[1,1],[1,1]]),max_iter=200):
    # example, we track number of unhappy people
    # with n=10,d=2,m=2,v=1,lo_thres=diag(0.33) i.e. want at least 1/3 own,hi_thres=all ones (not binding)
    # we get [10, 4, 1, 1, 1, 1, 1, 1, 1] 
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
    results = [gridinit(popdist,rho,n,d,m)]
    
    unhappy_list = []
    segcoeffs = []
    for cnt in xrange(max_iter):
        oldgrid = results[cnt]
        num_unhappy, newgrid = movegrid(oldgrid,n=n,d=d,v=v,m=m,hi_thres=hi_thres,lo_thres = lo_thres)
        if num_unhappy > 0:
            unhappy_list.append(num_unhappy)
            results.append(newgrid)
            segcoeffs.append(calc_seg(newgrid,v,n,d))
            cnt += 1
        else:
            break
    return [results,segcoeffs,unhappy_list]


def main():
    # RUN YOUR SIMULATION HERE
    ''' Initializing parameters'''
    n = 11 # this is n, grid size (nxnx...xn), d times
    d = 2 # this is d, number of dimensions (d<=10) 
    v = 1 # this is vision Note: if v=1, then we care about 3x3 squares
    m = 2 # this is m, number of types; type 1,2,...,m

    popdist = np.array([0.6, 0.4]) # proportion of each type, changes with m
    rho = 0.8 # this is rho, population density

    # m x m matrices
    lo_thres = np.matrix([[0.33,0.],[0.,0.33]])
    hi_thres = np.matrix([[1,1],[1,1]])

    # number of iterations
    max_iter = 200

    [results,segcoeffs,unhappy_list] = run(n=11)

    print "Initial Grid:"
    printgrid(results[0],n,d)
    print "Final Grid:"
    printgrid(results[-1],n,d)
    print "Neighborhood Sizes:"
    print neighborhood_sizes(results[-1],m=m,n=n,d=d)
    print "Segregation Coefficient:"
    print("%.4f" % segcoeffs[-1])
    print "Time to Equilibrium:"
    print len(segcoeffs), "steps"


if __name__ == "__main__":
    main()
    
        

