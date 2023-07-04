# imports
import click
import numpy as np
from z3 import *

from utils import *


############ support functions ############
def min_index(array):
    for i in range(len(array)):
        if array[i] == True:
            return i
    return 0

def max_index(array):
    for i in range(len(array)-1, -1, -1):
        if array[i] == True:
            return i
    return len(array)

def indeces(array):
    indeces = []
    indeces.append(len(array))
    for i in range(len(array)-1, -1, -1):
        if array[i] == True:
            indeces.append(i)
    return indeces

############ Pseudo Boolean model ############
def mcp_pb(instance):
    m = instance["m"] # courriers
    n = instance["n"] # packages
    l = instance["l"] # weigths
    s = instance["s"] # sizes of courriers
    time = instance["time"] # time
    min_load = instance["min_load"] # min load of each courrier
    max_load = instance["max_load"] # max load of each courrier
    at_least_one = instance["at_least_one"] # if each courrier must deliver at least one package
    equal_load_matrix = instance["equal_matrix"]

    solver = Solver()

    # To codify that courrier i deliver package j at time k
    v = [[[Bool(f"x_{i}_{j}_{k}") for k in range(time+1)] for j in range (n+1)] for i in range(m)]

    d = [[[Bool(f"d_{i}_{start}_{end}") for end in range(n+1)]
          for start in range(n+1)] for i in range(m)]

    for i in range(m):
        for k in range(time):
            for startj in range(n+1):
                for endj in range(n+1):
                    solver.add(
                        Implies(And(v[i][startj][k], v[i][endj][k+1]), d[i][startj][endj])
                    )

    # Constraints
    # 1. Each courier can carry at most l[i] kg
    # Pb version
    for i in range(m):
       solver.append(PbLe([(v[i][j][k],s[j]) for j in range(n) for k in range(1,time)], min(l[i], max_load)))
       solver.append(PbGe([(v[i][j][k],s[j]) for j in range(n) for k in range(1,time)], min_load))


    # 2. Each courier i starts and ends at position j = n
    for i in range(m):
        # solver.add(And(v[i][n][0], v[i][n][time]))
        solver.add(v[i][n][0])
        solver.add(v[i][n][time])


    # 3. Each courier can't be in two places at the same time 
    for i in range(m):
        for k in range(time+1):
            solver.add(exactly_one_seq([v[i][j][k] for j in range(n+1)], f"amo_package_{k}_{i}")) #(PbEq([(v[i][j][k],1) for j in range(n+1)],1))
    
    # 4. Each package j is delivered exactly once
    for j in range(n):
        solver.add(exactly_one_seq([v[i][j][k] for k in range(1,time) for i in range(m)], f"exactly_once_{j}")) #(PbEq([(v[i][j][k],1) for k in range(1,n+1) for i in range(m)],1))    
    
    # 5. If we know that each courier must deliver at least one package
    if at_least_one == 1:
        for i in range(m):
            solver.add(Or([v[i][j][1] for j in range(n)]))

    # Symmetry breaking constraints
    # 6. once a courier arrive to depot (j = n+1), it can't depart from there
    for i in range (m):
        for k in range(1, time-1):
            solver.add(
                Implies(v[i][n][k], v[i][n][k+1])
            )
    
    # 7. symmetry breaking for courriers with equal capacity
    assignments_array = [[Bool(f"aa_{i}_{j}") for j in range(n)] for i in range (m)]

    # aa true if the package j is assigned to i at any k
    for i in range(m):
        for j in range(n):
            solver.add(
                assignments_array[i][j] == Or([v[i][j][k] for k in range(1,time)]) 
            )

    for i in range(m):
        for i1 in range(i+1,m):
            for j in range(1,min_index([assignments_array[i][jj] for jj in range(n)])+1):
                solver.add(
                    Implies(
                        equal_load_matrix[i][i1],
                        Implies( Or(And(assignments_array[i][j-1], assignments_array[i1][j-1]), And(Not(assignments_array[i][j-1]),Not(assignments_array[i1][j-1]))) ,
                            Or(And(assignments_array[i][j], assignments_array[i1][j]), And(Not(assignments_array[i][j]),Not(assignments_array[i1][j])), assignments_array[i][j])
                        )
                    )
                )

    return solver, v, d

############ function for push pop ############
def add_distance_constraint_pb(solver, instance, v, d, upperBound):
    m = instance["m"] # courriers
    n = instance["n"] # packages
    time = instance["time"] # time
    distances = instance["distances"] # distances between packages

    # distance calculation
    # Pb version
    for i in range(m):
        solver.append(PbLe([(d[i][j1][j2],distances[j1][j2]) for j1 in range (n+1) for j2 in range (n+1)], upperBound))
    
    flattened_distances = np.array(instance['distances']).flatten()
    flattened_distances = flattened_distances[flattened_distances != 0]
    flattened_distances = np.sort(flattened_distances)

    max_k = 0

    while np.sum(flattened_distances[:max_k]) <= upperBound and max_k < n:
        max_k += 1

    if max_k < time:
        for i in range(m):
            solver.add(v[i][n][max_k + 1])