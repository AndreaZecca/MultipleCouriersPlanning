import os
import pandas as pd
import json

technologies = ["CP", "SAT", "SMT", "SMT-LIB", "MIP"]


keys_to_method = {
    "CP": {
        'Gecode': 'Gecode w/out SB',
        'Gecode_sb': 'Gecode + SB',
        'Chuffed': 'Chuffed w/out SB',
        'Chuffed_sb': 'Chuffed + SB',
    },
    "SAT": {
        'pb': 'SAT + Pseudo-Boolean',
        'standard': 'SAT'
    },
    "SMT": {
        "symmetry_breaking": "SMT + SB",
        "standard": "SMT w/out SB"
    },
    "SMT-LIB":{
        'z3': 'Z3',
        'cvc4': 'cvc4',
        'cvc5': 'cvc5',
    },
    "MIP":{
        'cbc': 'CBC',
        'grb': 'Gurobi'
    }
}


for tech in technologies:
    try:
        dir_path = f"./{tech}"
        # Get all files
        files = os.listdir(dir_path)
        # Filter only json files
        files = [f"./{tech}/{file}" for file in files if file.endswith(".json")]
        columns = ['ID', *keys_to_method[tech].values()]
        # Create dataframe

        results = []

        for file_name in sorted(files, key=lambda x: int(x.split("/")[2].split(".")[0])):
            # Read json file
            # to_append = {
            #     "ID": file_name.split("/")[2].split(".")[0]
            # }
            to_append = {}
            total_results = json.load(open(file_name))
            for method in total_results:
                method_result = total_results[method]
                sol_found = method_result['obj']
                to_append[keys_to_method[tech][method]] =  int(sol_found) if isinstance(sol_found, int) else sol_found.upper() 
                to_append[f"Optimallty_{keys_to_method[tech][method]}"] = True if method_result['optimal'] else False 
            results.append(to_append)

        df = pd.DataFrame(results)
        df.index += 1 
        df.to_csv(f"./tables/{tech}.csv", index=True)
    except Exception as e:
        print(e)
        continue
