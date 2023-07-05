import json
import re

import click
import numpy as np

from SAT.core import run_sat
from MIP.core import run_mip

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
                # formatted_v = ''
                #for i,row in v:
                #    formatted_v += '[' + ', '.join([str(x) for x in row]) + '],\n'

                # v = '[|' + ((' ' * len(k) + ',\n')).join([', '.join([str(y) for y in x]) for x in v]) + '|]'
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


@click.command()
@click.argument('config_file', type=click.File('r'))
def main(config_file):
    config = json.load(config_file)

    with open(config["instance"], "r") as instance:
        instance = parse_dat(instance.read())
    
    instance = add_additional_info(instance)
    # print(instance)

    # print(to_mzn(instance))
    
    if config['method'] == 'sat':
        # print(run_sat(instance, config['pb']))

        result = utils.run_with_timeout(run_sat, config['timeout'], instance, config['pb'])
        
    elif config['method'] == 'mip':
        result = run_mip(instance, config['timeout'], config['solver'])
    else:
        raise RuntimeError('Unknown method')
    if result is not None:
        solution, optimal = result
        distances = distances_from_solution(instance, solution)
        print(f"Optimal: {optimal}")
        print(f"Distances: {distances}")
        print(f"Solution: {solution}")
        print(f"Max distance: {max(distances)}")
if __name__ == '__main__':
    main()