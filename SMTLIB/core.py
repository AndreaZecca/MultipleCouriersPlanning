import os
from time import time as clock_time

from SMT.core import generate_smt_model

def format_smtlib_output(instance, result):
    m = instance["m"]
    time = instance["time"]
    result = result.split("\n")[1:]
    # removing () from result
    result = [x.replace("(", "").replace(")", "") for x in result if x != ""]
    couriers_step = []
    for i in range(m):
        couriers_step.append([])
        for j in range(time+1):
            # print(result[i*time+j])
            step = int(result[i*time+j].split(" ")[1])
            if step != instance["n"]:
                couriers_step[i].append(step + 1)
        couriers_step[i]
    return couriers_step


def run_smt_lib(_, instance, timeout, sb, instance_number, solver):
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
            # -1 since we need to remove (check-sat) from the generated smt-lib2
            smt2 = smt2[:-1]
            smt2 = "\n".join(smt2[:-1])
            f.write(smt2)
            f.write("\n")

        generation_time = clock_time() - generation_start_time
        residual_time = timeout - generation_time

        running_start_time = clock_time()
        m = instance['m']
        time = instance['time']
        max_dist = instance['max_dist']
        start_time = clock_time()
        result = os.popen(f"./SMTLIB/linear_search.sh {file_path} max_distance {max_dist} {solver} {m} {time+1}").read()
        elapsed = clock_time() - running_start_time
        result = format_smtlib_output(instance, result)
        return result, int(elapsed) < residual_time
    except:
        return None