import os
from pathlib import Path
from time import time

var_choices = [
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

value_choices = [
    "indomain_min",
    "indomain_max",
    # "indomain_middle",
    "indomain_median",
    "indomain",
    "indomain_random",
    "indomain_split",
    "indomain_reverse_split",
    # "indomain_interval"
]


results = []

def append_result(var_choice, value_choice, solver, elapsed):
    results.append((solver, var_choice, value_choice, elapsed))

    results_file = 'results.csv'
    if Path(results_file).exists():
        with open(results_file) as f:
            current_results = f.read()
    else:
        current_results = ''
    
    current_results += f'{solver},{var_choice},{value_choice},{elapsed}\n'

    with open(results_file, 'w') as f:
        f.write(current_results)


for solver in ['Chuffed', 'Gecode']:
    for var_choice in var_choices:
        for value_choice in value_choices:
            line = f"solve :: int_search(x, {var_choice}, {value_choice})  minimize max(y);\n"
            with open('./cp_template.mzn') as f:
                text = f.read()

            text = text.replace('LINEA', line)

            test_path = './cp_test.mzn'

            with open(test_path, 'w') as f:
                f.write(text)
            
            start_time = time()
            os.system(f'minizinc --solver {solver} --solver-time-limit 60000 cp_test.mzn ./tests/inst12.dzn')
            elapsed = time() - start_time
            # print('Elapsed:', elapsed)

            append_result(var_choice, value_choice, solver, elapsed)

        

results = sorted(results, key=lambda x: x[-1])
print('\n'.join(results))