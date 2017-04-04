"""
Essam


This is a quick sketch. NEEDS to be checked for potential bugs.

"""

import numpy as np

N = 6
percent = 0.6
radius = 2
threshold = 0.33

def create_matrix(N, percent):
    number = np.floor((percent)*(N**2))
    m = [[0 for i in range(N)] for j in range(N)]
    to_turn_1 = np.random.choice(N**2, size=int(number), replace=False)
    for k in to_turn_1:
        m[k/N][k%N] = 1

def check_happiness(matrix, x, y, radius, threshold):
    n = len(matrix)
    sum_ = 0
    
    up = x-radius
    down = x+radius
    left = y-radius
    right = y+radius
    
    if (x-radius) < 0:
        up = 0
    if (x + radius) > n:
        down = n
    if (y-radius) < 0:
        left = 0
    if (y+radius) > n:
        right = n
    
    for row in range(up, down + 1):
        sum_ += matrix[row][y]
        
    for col in range(left, right + 1):
        sum_ += matrix[x][col]

    # Subtract person's own value
    sum_ -= 1
    
    proportion = (sum_/((right-left+1)*(down-up+1)-1))
    
    if matrix[x][y] == 0:
        proportion = 1 - proportion
    
    if proportion > threshold:
        # happy
        return 1
    else:
        # sad
        return 0

# make a list of all the unhappy people
q = [(r, c) for r in range(N) for c in range(N) if check_happiness(m, r, c, radius, threshold) == 0]