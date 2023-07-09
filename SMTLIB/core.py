import os
from time import time as clock_time
import numpy as np

from SMT.core import generate_smt_model


def run_with_pivot(solve_type, file_path, pivot, min_distance, m, time):
    smt2 = ""
    with open(file_path, "r") as f:
            smt2 = f.read()
            smt2 = smt2.split("\n")
    smt2.append(f"(assert (<= max_distance {pivot}))")
    smt2.append(f"(assert (>= max_distance {min_distance}))")
    smt2.append("(check-sat)")
    for i in range(m):
        for j in range(time):
            smt2.append(f"(get-value (x_{i}_{j}))")
    smt2 = "\n".join(smt2)

    with open(file_path, "w") as f:
        f.write(smt2)
    result = os.popen(f"{solve_type} {file_path}").read()
    result = result.split("\n")
    return result

def format_smtlib_output(instance, result):
    try:
        m = instance["m"]
        n = instance["n"]
        time = instance["time"]
        result = result[1:]
        # removing () from result
        result = [x.replace("(", "").replace(")", "") for x in result if x != ""]
        result = [x.split(" ")[1] for x in result]
        courier_result = np.array(result, dtype=int)
        courier_result = np.reshape(courier_result, (m, time+1)).tolist()
        courier_result = [[x+1 for x in l if x!=n] for l in courier_result]
        return courier_result
    except:
        return None

def run_binary_search(add_intermediate_result, file_path, min_dist, max_dist, solver, m, time, instance):
    solve_type = ""
    match solver:
        case "z3":
            solve_type = "z3"
        case "cvc4":
            solve_type = "cvc4 --lang smt --produce-models --incremental"
        case "cvc5":
            solve_type = "cvc5 --produce-models --incremental"
        case _:
            raise Exception("Solver not supported")

    last_result = None

    lower = min_dist
    upper = max_dist
    pivot = None

    is_sat = False
    is_first = True
    while lower <= upper:
        pivot = (upper + lower) // 2
        with open(file_path, "r") as f:
            smt2 = f.read()
            smt2 = smt2.split("\n")
        if not is_first:
            smt2 = smt2[:-(m*time+3)]
        smt2 = "\n".join(smt2)
        
        with open(file_path, "w") as f:
            f.write(smt2)
        result = run_with_pivot(solve_type, file_path, pivot, lower, m, time)
        is_first = False
        if result[0] == "unsat":
            lower = pivot + 1
            pivot = (upper + lower) // 2
        else:
            is_sat = True
            formatted_result = format_smtlib_output(instance, result)
            if formatted_result is None:
                return None
            add_intermediate_result(formatted_result)
            last_result = formatted_result
            upper = pivot - 1
            pivot = (upper + lower) // 2

    return last_result

def run_smt_lib(add_intermediate_result, instance, timeout, sb, instance_number, solver):
    try:
        generation_start_time = clock_time()
        model, _, _ = generate_smt_model(instance, timeout, sb)
        # converting to smt-lib2 format
        smt2 = model.sexpr()
        # save to file
        file_path = f"./SMTLIB/instances/smt2_{instance_number}.smt2"
        # get absolute path of file_path
        # file_path = os.path.abspath(file_path)
        # if file not exists, create it
        with open(file_path, "w") as f:
            f.write("(set-logic ALL)\n")
            # removing last row from smt2
            smt2 = smt2.split("\n")
            # -2 since we need to remove (check-sat) and the last empty row from the generated smt-lib2
            smt2 = smt2[:-2]
            smt2 = "\n".join(smt2)
            f.write(smt2)
            f.write("\n")

        generation_time = clock_time() - generation_start_time
        residual_time = timeout - generation_time

        running_start_time = clock_time()
        m = instance['m']
        time = instance['time']
        min_dist = instance['min_dist']
        max_dist = instance['max_dist']
        result = run_binary_search(add_intermediate_result, file_path, min_dist, max_dist, solver, m, time + 1, instance)
        # result = os.popen(f"./SMTLIB/linear_search.sh {file_path} max_distance {max_dist} {solver} {m} {time+1}").read()
        elapsed = clock_time() - running_start_time
        # result = format_smtlib_output(instance, result)
        if result is None:
            return None
        elif result == "unsat":
            return "unsat"
        else:
            return result, int(elapsed) < residual_time
    except:
        return None