import json
import re
from time import time
import os

import click
import numpy as np

from SAT.core import run_sat
from MIP.core import run_mip
from SMT.core import run_smt

import utils

def parse_dat(text):
    lines = text.split("\n")
    # regex to get a number from a string
    num_regex = r"(\d+)"
    lines = [x for x in lines if x != ""]
    lines = [x.strip() for x in lines]
    m = int(re.findall(num_regex, lines[0])[0])
    n = int(re.findall(num_regex, lines[1])[0])
    l = [int(x) for x in re.findall(num_regex, lines[2])]
    s = [int(x) for x in re.findall(num_regex, lines[3])]

    distances = []
    for i in range(4, 4 + n + 1):
        distances.append([int(x) for x in re.findall(num_regex, lines[i])])

    return {
        "m": m,
        "n": n,
        "l": l,
        "s": s,
        "distances": distances
    }

def add_additional_info(data):
    n = data["n"]
    m = data["m"]
    l = data["l"]
    s = data["s"]
    distances = np.array(data["distances"])

    # count min package per courier
    each_courier_at_least_one = 0
    sorted_packages = sorted(s, reverse=True)
    sorted_load = sorted(l, reverse=True)
    for i in range(m):
        if sorted_load[i] < sorted_packages[i]:
            break
    else:
        each_courier_at_least_one = 1
        
    time_bound1 = each_courier_at_least_one + n - each_courier_at_least_one * m + 1

    # count max package per courier 
    max_load = max(l)
    sorted_packages = sorted(s)
    max_package_count = 0
    for package in sorted_packages:
        max_load -= package
        if max_load >= 0:
            max_package_count += 1
        else:
            break
    
    time_bound2 = max_package_count + 1 # max_package_count + 2 - 1 since 0-indexed
    
    time = min(time_bound1, time_bound2)

    # calculate max_dist
    max_dist_bound1 = np.sum(np.max(distances[:n], axis=1))
    max_dist_bound2 = np.sum(sorted(distances.flatten(), reverse=True)[:time+1])

    if each_courier_at_least_one == 0:
        max_dist = max_dist_bound1
    else:
        max_dist = np.min([max_dist_bound1, max_dist_bound2])

    min1 = min(distances[n][:n])
    min2 = min([x[n] for x in distances[:n]])

    
    if each_courier_at_least_one == 0:
        min_dist = 0
    else:
        min_dist = min(min1, min2)*2
    
    # calculate min_solution

    min_solution = np.max([distances[n, j] + distances[j, n] for j in range(n)])

    # calculate min_load and max_load
    min_load = np.min(s) * each_courier_at_least_one
    max_load = min(np.max(l), np.sum(sorted(s, reverse=True)[:time]))

    return {
        **data,
        "min_dist": min_dist,
        "max_dist": max_dist,
        "min_solution": min_solution,
        "time": time,
        "at_least_one": each_courier_at_least_one,
        "min_load": min_load,
        "max_load": max_load
    }

def to_mzn(instance):
    text = ''
    n = instance["n"]
    for k, v in instance.items():
        if isinstance(v, list):
            v = np.array(v)
            if len(v.shape) == 1:        
                v = '[' + ', '.join([str(x) for x in v]) + ']'
            elif len(v.shape) == 2:
                formatted_v = '[|'
                for i,row in enumerate(v):
                    formatted_v += ', '.join([str(x) for x in row])
                    if i != n:
                        formatted_v += ', \n \t\t     | '
                formatted_v += ' |]'
                v = formatted_v
        text += f'{k} = {v};\n'

    return text

def distances_from_solution(instance, solution):
    distance = np.array(instance["distances"])
    n = instance["n"]
    m = instance["m"]
    courier_dist = np.zeros(m)
    solution = [[n+1] + x + [n+1] for x in solution]
    for i in range(m):
        for j in range(len(solution[i])-1):
            # -1 since 0-indexed
            courier_dist[i] += distance[solution[i][j]-1][solution[i][j+1]-1]
    return courier_dist

def format_output(instance, result, elapsed):
    if result is not None:
        solution, optimal = result
    else:
        solution = None
        optimal = False

    if not optimal:
        elapsed = 300

    elapsed = int(np.floor(elapsed))

    return {
        "time" : elapsed,
        "optimal" : optimal,
        "obj" : "n/a" if solution is None else int(np.max(distances_from_solution(instance, solution))),
        "sol" : [[int(x) for x in solu] for solu in solution] if solution is not None else None
    }

def parse_cp_output(cp_output, instance):
    m = instance["m"]
    n = instance["n"]
    x = cp_output.split('\n')[0]
    x = x.split('[')[1].split(']')[0].split(', ')
    x = np.array([int(y) for y in x])
    x = x.reshape((m, n+1))
    courier_step = []
    for i in range(m):
        first_step = x[i, -1]
        if first_step == n+1:
            courier_step.append([])
        else:                
            courier_step.append([first_step])
            while first_step != n+1:
                first_step = x[i, first_step-1]
                if first_step != n+1:
                    courier_step[i].append(first_step)
    return courier_step

@click.command()
@click.argument('config_file', type=click.File('r'))
@click.argument('verbose', type=bool, default=False)
def main(config_file, verbose):
    configurations = json.load(config_file)
    for config in configurations:

        instance_number = config["instance"].split('/')[-1]
        instance_number = int(re.findall(r"(\d+)", instance_number)[0])
        
        if verbose:
            debug_info = f"- Instance:{instance_number} - Method:{config['method']}"
            if config['method'].lower() == 'cp':
                debug_info += f" - Solver:{config['solver']}"
                debug_info += f" - SB:{config['symmetry_breaking']}"
            elif config['method'].lower() == 'mip':
                debug_info += f" - Solver:{config['solver']}"
            elif config['method'].lower() == 'sat':
                debug_info += f" - PB:{config['pseudo_boolean']}"
            elif config['method'].lower() == 'smt':
                debug_info += f" - SB:{config['symmetry_breaking']}"
            print(debug_info)


        start_time = time()
        try:
            with open(config["instance"], "r") as instance:
                instance = parse_dat(instance.read())
        except FileNotFoundError:
            print("Instance file not found")
            return
        instance = add_additional_info(instance)

        output_field_name = ''
        
        if config['method'].lower() == 'cp':
            cp_instance = to_mzn(instance)
            with open('./data.dzn', 'w') as f:
                f.write(cp_instance)
            cp_to_call = "cp_sb.mzn" if config['symmetry_breaking'] else "cp.mzn" 
            cp_output = os.popen(f"minizinc ./CP/{cp_to_call} --solver {config['solver']} --solver-time-limit {config['timeout'] * 1_000} -d data.dzn").read()
            time_spent = time() - start_time
            if "UNSATISFIABLE" in cp_output or "=UNKNOWN=" in cp_output:
                result = None
            else:
                cp_result = parse_cp_output(cp_output, instance)
                isOptimal = time_spent <= config['timeout']
                result = (cp_result, isOptimal)
            os.remove('./data.dzn')

            output_field_name = config['solver']
            if config['symmetry_breaking']:
                output_field_name += '_sb'
        elif config['method'].lower() == 'sat':
            result = utils.run_with_timeout(run_sat, config['timeout'] + 1, instance, config['pseudo_boolean'])
            output_field_name = 'pb' if config['pseudo_boolean'] else 'standard'
        elif config['method'].lower() == 'smt':
            result = utils.run_with_timeout(run_smt, config['timeout'] + 1, instance, config['timeout'], config['symmetry_breaking'])
            output_field_name = 'symmetry_breaking' if config['symmetry_breaking'] else 'standard'
        elif config['method'] == 'mip':
            result = utils.run_with_timeout(run_mip, config['timeout'] + 1, instance, config['timeout'], config['solver'])
            output_field_name = config['solver']
        else:
            raise RuntimeError('Unknown method')

        elapsed = time() - start_time
        formatted_output = format_output(instance, result, elapsed)
        # print(formatted_output)    

        json_file_path = f'./res/{config["method"].upper()}/{instance_number}.json'
        if not os.path.exists(json_file_path):
            with open(json_file_path, 'w') as f:
                f.write('{}')
                f.close()

        with open(json_file_path, "r") as jsonFile:
            json_file_content = json.load(jsonFile)
        json_file_content[output_field_name] = formatted_output
        with open(json_file_path, "w") as jsonFile:
            json.dump(json_file_content, jsonFile, indent=4, separators=(',', ': '))
if __name__ == '__main__':
    main()