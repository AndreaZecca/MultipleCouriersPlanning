from .sat_pseudobool import *
from .sat_standard import *


def add_additional_info(instance):
    m = instance["m"]
    l = instance["l"]
    equal_matrix = np.full((m,m), Bool(False))
    for i in range(m):
        for i1 in range(m):
            if l[i] == l[i1]:
                equal_matrix[i,i1] = True
    instance["equal_matrix"] = equal_matrix

def solve_mcp(solver):
    if solver.check() == sat:
        return solver.model()
    else:  
        return unsat

def format_solution(m, n, time, model, v):
    solution = []

    for i in range(m):
        courier_solution = []

        for k in range(time):
            for j in range(n):
                if model[v[i][j][k]]:
                    courier_solution.append(j + 1)

        solution.append(courier_solution)

    return solution


def run_mcp(instance, use_pb=True):
    # copy of the instance since we will modify it
    instance = dict(instance)
    if use_pb:
        mcp = mcp_pb
        add_constraint = add_distance_constraint_pb
    else:
        mcp = mcp_standard
        add_constraint = add_distance_constraint_standard

    # add additional info to the instance
    add_additional_info(instance)
    # original upper bound -> used in the binary search to check if the problem is unsat
    original_upper_bound = instance["max_dist"]
    # lower bound for the binary search
    lower_bound = instance["min_dist"]
    # upper bound for the binary search
    upper_bound = original_upper_bound

    # pivot for the binary search
    pivot = (original_upper_bound + lower_bound) // 2

    # solver creation based on the model used
    solver, v, d = mcp(instance) 

    res = None

    best_solution = None

    # binary search using bounds
    while True:
        # print('Lower:', lower_bound, 'Upper:', upper_bound, 'Pivot:', pivot)
        # if the lower bound is equal to the upper bound, we have found the optimal solution
        if lower_bound >= upper_bound and res is not None:
            return best_solution

        # push/pop mechanism for adding new constraint and solving the problem
        solver.push()

        # add the constraint to the solver to force the distance to be lower or equal than the pivot
        add_constraint(solver, instance, v, d, pivot)

        # solve the problem with the current constraints
        res = solve_mcp(solver)

        # if the problem is unsat
        if res == unsat:
            # if we reached an ending point in the binary search
            if lower_bound >= original_upper_bound:
                # if the upper bound is equal to the original upper bound, the problem is unsat since we never found a solution
                return None
            
            # updating lower
            lower_bound = pivot + 1
            # pop the constraint since we will add a new one
            solver.pop()
            # update the pivot
            pivot = (upper_bound + lower_bound) // 2
        else:
            # if the problem is sat, we save the solution
            best_solution = format_solution(instance['m'], instance['n'], instance['time'], res, v)
            upper_bound = pivot
            pivot = (upper_bound + lower_bound) // 2