from sat_pseudobool import *
from sat_standard import *


def solve_mcp(solver, instance, v, verbose=False):
    m = instance["m"] # couriers
    n = instance["n"] # packages
    time = instance["time"] # time
    if not verbose:
        if solver.check() == sat:
            return solver.model()
        else:  
            return False
    else:
        print(solver.check())
        if solver.check() == sat:
            model = solver.model()
            for i in range(m):
                print()
                print(f"Courier {i+1}:")
                for k in range(time+1):
                    for j in range(n+1):
                        if model[v[i][j][k]]:
                            print(f"Time {k} Place {j} : {model[v[i][j][k]]}")
            return solver.model()
        else:
            return False

def run_mcp(instance, use_pb=True):
    if use_pb:
        mcp = mcp_pb
        add_constraint = add_distance_constraint_pb
    else:
        mcp = mcp_standard
        add_constraint = add_distance_constraint_standard

    m = instance["m"]
    l = instance["l"]
    equal_matrix = np.full((m,m), Bool(False))
    for i in range(m):
        for i1 in range(m):
            if l[i] == l[i1]:
                equal_matrix[i,i1] = True
    instance["equal_matrix"] = equal_matrix

    original_upper_bound = instance["max_dist"]
    lower_bound = instance["min_dist"]
    upper_bound = original_upper_bound

    pivot = (original_upper_bound + lower_bound) // 2

    solver, v, d = mcp(instance) # create basic solver

    # binary search using bounds
    print("searching...")
    while True:
        if lower_bound == upper_bound:
            return upper_bound
        print("pivot:", pivot)

        solver.push()
        add_constraint(solver, instance, v, d, pivot)

        res = solve_mcp(solver, instance, v, verbose)
        if(res == False):
            print("fail")
            if lower_bound > upper_bound:
                if upper_bound == original_upper_bound:
                    return unsat
                else:
                    return upper_bound
            lower_bound = pivot + 1

            solver.pop()

            pivot = (upper_bound + lower_bound) // 2
        else:
            print("success")
            upper_bound = pivot
            pivot = (upper_bound + lower_bound) // 2