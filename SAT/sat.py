from sat_pseudobool import *
from sat_standard import *


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

def run_mcp(instance, use_pb=True):
    # copy of the instance since we will modify it
    instance = dict(instance)
    if use_pb:
        mcp = mcp_pb
        add_constraint = add_distance_constraint_pb
    else:
        mcp = mcp_standard
        add_constraint = add_distance_constraint_standard

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

    # binary search using bounds
    while True:
        # if the lower bound is equal to the upper bound, we have found the optimal solution
        if lower_bound == upper_bound:
            if res is None:
                # the instance has never been run before
                res = solve_mcp(solver, instance, v, verbose)
            if res is unsat:
                res = None
            return upper_bound, res

        # push/pop mechanism for adding new constraint and solving the problem
        solver.push()

        # add the constraint to the solver to force the distance to be lower or equal than the pivot
        add_constraint(solver, instance, v, d, pivot)

        # solve the problem with the current constraints
        res = solve_mcp(solver, instance, v, verbose)

        # if the problem is unsat
        if res is unsat:
            # if we reached an ending point in the binary search
            if lower_bound > upper_bound:
                # if the upper bound is equal to the original upper bound, the problem is unsat since we never found a solution
                if upper_bound == original_upper_bound:
                    return None
                # otherwise, the upper bound is the optimal solution
                else:
                    return upper_bound, res
            # updating lower
            lower_bound = pivot + 1
            # pop the constraint since we will add a new one
            solver.pop()
            # update the pivot
            pivot = (upper_bound + lower_bound) // 2
        else:
            upper_bound = pivot
            pivot = (upper_bound + lower_bound) // 2