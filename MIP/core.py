from mip import *
import numpy as np

def generate_mip_model(instance, solver_name):
    print(solver_name)
    n = instance["n"]
    m = instance["m"]
    l = instance["l"]
    s = instance["s"]
    min_dist = instance["min_dist"]
    max_dist = instance["max_dist"]
    min_solution = instance["min_solution"]
    time = instance["time"]
    at_least_one = instance["at_least_one"]
    min_load = instance["min_load"]
    max_load = instance["max_load"]

    # model = Model() # uses Gurobi as default
    model = Model(solver_name=solver_name)

    # x[i, j1, j2] is 1 if the courier i travels from node j1 to node j2
    x = model.add_var_tensor((m, n + 1, n + 1), var_type=BINARY, name="x")

    # y[i] is the distance traveled by the courier i
    y = model.add_var_tensor((m,), var_type=INTEGER, lb=min_dist, ub=max_dist, name="y")

    # t[i, j] is 1 if the courier i carries the package j
    t = model.add_var_tensor((m, n), var_type=BINARY, name="t")

    # z is a path counter where z[i, j] is the number of the node j in the path of the courier i
    z = model.add_var_tensor((m, n + 1), var_type=INTEGER, lb=0, ub=time, name="z")

    # v is the maximum distance traveled by a courier
    v = model.add_var(name="v", var_type=INTEGER, lb=min_solution, ub=max_dist)

    # M is a sufficiently large value for the path counter
    M = n + 3

    # The counter is 0 for the deposit
    model += z[:, n] == 0

    # x[i, j1, j2] = 1 means that the courier i travels from node j1 to node j2, so 
    # z[i, j2] = z[i, j1] + 1 since the time at which courier i arrives to node j2 is 
    # one unit larger than the time at which it arrives to node j1
    for i in range(m):
        for j1 in range(n + 1):
            for j2 in range(n): # Note that j2 cannot be n + 1 (i.e. the deposit)
                # if x[i, j1, j2] = 1, then z[i, j2] = z[i, j1] + 1
                model += z[i, j2] - z[i, j1] <= M * (1 - x[i, j1, j2]) + 1
                model += z[i, j1] - z[i, j2] <= M * (1 - x[i, j1, j2]) - 1

    # Each courier moves at least one time (even if it does not carry any package he has to go back to the deposit)
    for i in range(m):
        model += np.sum(x[i, n, :]) == 1
        model += np.sum(x[i, :, n]) == 1

    # If we know that each courier has to carry at least one package, then we can add the following constraints
    if at_least_one == 1:
        for i in range(m):
            model += np.sum(x[i, n, :n]) == 1

    # t[i, j] is 1 if the courier i carries the package j
    for i in range(m):
        for j in range(n):
            model += np.sum(x[i, j, :]) == t[i, j]

    # All packages are carried by exactly one courier
    for j in range(n):
        model += np.sum(t[:, j]) == 1

    # If a courier arrives to a package, it has to leave from that package
    for i in range(m):
        for j in range(n):
            courier_arrives = np.sum(x[i, :, j])
            courier_leaves = np.sum(x[i, j, :])
            # (not arrives) or leaves
            model += (1 - courier_arrives) + courier_leaves >= 1


    # Each courier does not exceed its capacity
    for i in range(m):
        model += (t[i, :] @ s) <= max_load
        model += (t[i, :] @ s) <= l[i]
        model += (t[i, :] @ s) >= min_load

    # y[i] is the distance traveled by the courier i
    for i in range(m):
        model +=  np.sum(x[i, :, :] * np.array(instance["distances"])) == y[i]

    # You cannot travel from a node to itself
    for i in range(m):
        for j in range(n):
            model += x[i, j, j] == 0

    # The maximum distance traveled by a courier is v
    for i in range(m):
        model += v >= y[i]

    # setting the number of threads to -1 uses all the available threads
    model.threads = -1
    model.verbose = 0
    model.objective = minimize(v)
    model.optimize()
    return model, x

def find_next(x, i, node, n):
    for j in range(n + 1):
        if x[i, node, j].x == 1:
            return j

def format_solution(instance, x):
    m = instance["m"]
    n = instance["n"]
    solution = []
    for i in range(m):
        solution.append([])
        current_node = n
        current_node = find_next(x, i, current_node, n)
        while current_node != n:
            solution[i].append(current_node + 1)
            current_node = find_next(x, i, current_node, n)
    return solution

def run_mip(instance, timeout, solver):
    print(timeout)
    model, x = generate_mip_model(instance, solver)  
    model.timeLimit = timeout
    model.optimize() 
    print("fine ottimizzazione")
    print(model.status)
    if model.status in [OptimizationStatus.OPTIMAL, OptimizationStatus.FEASIBLE]:
        solution = format_solution(instance, x)
        isOptimal = model.status == OptimizationStatus.OPTIMAL
        return solution, isOptimal
    else:
        return None

