import itertools

var_choice = [
    "input_order",
    "first_fail",
    "anti_first_fail",
    "smallest",
    "largest",
    "occurrence",
    "most_constrained",
    "max_regret",
    "dom_w_deg"
]

value_choice = [
    "indomain_min",
    "indomain_max",
    "indomain_middle",
    "indomain_median",
    "indomain",
    "indomain_random",
    "indomain_split",
    "indomain_reverse_split",
    "indomain_interval"
]

def main():
    t = ""
    for i in var_choice:
        for j in value_choice:
            # save output to file with the format "solve :: int_search(x, {i}, {j})  minimize max(y);
            t += f"solve :: int_search(x, {i}, {j})  minimize max(y);\n"
    with open("heuristics_comb.txt", "w") as f:
        f.write(t)

if __name__ == "__main__":
    main()