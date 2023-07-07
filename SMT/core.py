from time import time as time_clock

from z3 import *

def maxv(vs):
  m = vs[0]
  for x in vs[1:]:
    m = If(x > m, x, m)
  return m


def get_list_of_values(ll,j):
    return([If(x==j,1,0) for l in ll for x in l])



def maxv(vs):
  m = vs[0]
  for x in vs[1:]:
    m = If(x > m, x, m)
  return m

def get_list_of_values(ll,j):
        return([If(x==j,1,0) for l in ll for x in l])

def generate_smt_mode(instance, timeout, sb):
    m = instance['m'] # couriers
    n = instance['n'] # packages
    l = instance['l'] # capacities
    time = instance['time'] # max number of packages a courier can carry
    min_dist = instance['min_dist'] # min distance for a single courier
    max_dist = instance['max_dist'] # max distance
    min_load = instance['min_load'] # min load for a single courier
    max_load = instance['max_load'] # max load for a single courier
    min_solution = instance['min_solution'] # minimum max distance
    
    # casting integers to z3 integers
    max_load = IntVal(f"{max_load}")
    min_load = IntVal(f"{min_load}")
    min_dist = IntVal(f"{min_dist}")
    max_dist = IntVal(f"{max_dist}")
    min_solution = IntVal(f"{min_solution}")

    o = Optimize()
    ####################################### DECISION VARIABLES #######################################

    # main decision variable: x[i,k] = j mean that the i-th courier is in j at time k
    x = [[Int(f'x_{i}_{k}') for k in range(0,time+1)]for i in range(m)]

    # variable for distance calculation
    y = [Int(f'y_{i}') for i in range(m)] 

    # variable for loads calculation
    load = [Int(f'load_{i}') for i in range(m)] 

    # distance to minimize
    max_distance = Int(f'max_distance')
    


    # we define distances as a z3 array because it is easier to indicize
    distances = Array('distances', IntSort(), ArraySort(IntSort(), IntSort()))
    for j in range(n+1):
        for j1 in range(n+1):
            o.add(distances[j][j1] == instance['distances'][j][j1])

    # we define s as a z3 array because it is easier to indicize
    s = Array('s', IntSort(), IntSort())
    for j in range(n):
        o.add(s[j] == instance['s'][j]  )
    o.add(s[n] == 0)

    
    ####################################### CONSTRAINTS #######################################

    # define possible value for x[i][k]
    o.add([And(x[i][k] >= 0, x[i][k] <= n) for i in range(m) for k in range(1,time)])
    o.add([And(x[i][0] == n, x[i][time] == n) for i in range(m)])

    # for each i foreach k, each x[i][k] must be different, unless it is equal to n
    for j in range(n):
        o.add([Sum(get_list_of_values([[x[i][k] for k in range(1,time+1)] for i in range(m)],j))==1])
    
    # for each i, the sum of the weights of the packages carried by the courier i must be less than the capacity of the courier i
    for i in range(m):
        o.add(load[i] == Sum([s[x[i][k]] for k in range(1,time)]))
        o.add(load[i] <= l[i])
    
    # bound to loads array
    for i in range(m):
        o.add(And(load[i] >= min_load, load[i] <= max_load))

    ####################################### SYMMETRY BREAKING CONSTRAINTS #######################################
    if sb:
        # once a courier i return to the depot, it cant deliver other packages
        for i in range(m):
            for k in range(1,time):
                o.add(Implies(x[i][k]==n, x[i][k+1]==n))
        
        # lexycographic constraint between couriers with == capacity
        for i1 in range(m-1):
            for i2 in range(i1+1,m):
                o.add(Implies(l[i1]==l[i2], If(x[i1][1]!=n, x[i1][1], -1)<=If(x[i1][1]!=n, x[i1][1], -1)))
        
        # constraint over maximum loads of the couriers
        for i1 in range(m-1):
            for i2 in range(i1+1,m):
                o.add(Implies(l[i1] <= l[i2], load[i1] <= load[i2]))

    ####################################### OBJECTIVE FUNCTION #######################################
    
    # distances array
    for i in range(m):
        o.add(y[i] == Sum([distances[x[i][k]][x[i][k+1]] for k in range(0,time)]))

    #bound to distances array
    for i in range(m):
        o.add(And(y[i] >= min_dist, y[i] <= max_dist))

    # variable to minimize
    o.add(max_distance == maxv(y))

    # bound the variable to minimize
    o.add(max_distance >= min_solution)

    return o, x, max_distance

def format_solution(instance, model, x):
    m = instance['m'] # couriers
    n = instance['n'] # packages
    # print(model)
    time = instance['time'] # max number of packages a courier can carry
    step_courier = []
    for i in range(m):
        step_courier.append([])
        for k in range(1,time+1):
            if model.eval(x[i][k]).as_long() != n:
                step_courier[i].append(model.eval(x[i][k]).as_long() + 1) 
    return step_courier

def run_smt(_, instance, timeout, sb, instance_number):
    generation_start_time = time_clock()

    o, x, max_distance = generate_smt_mode(instance, timeout, sb)

    # converting to smt-lib2 format
    
    smt2 = o.sexpr()
    # save to file
    with open(f"./SMT/smt2/smt2_{instance_number}.smt2", "w") as f:
        f.write("(set-logic ALL)\n")
        # removing last row from smt2
        smt2 = smt2.split("\n")
        smt2 = smt2[:-1]
        smt2 = "\n".join(smt2[:-1])
        f.write(smt2)

    generation_duration = time_clock() - generation_start_time
    o.set("timeout", int(timeout - generation_duration) * 1000)

    obj = o.minimize(max_distance)
    res = o.check()
    if res in [sat, unknown]:
        try:
            result_formatted = format_solution(instance, o.model(), x)
            return result_formatted, res==sat
        except:
            return None
    else:
        return None