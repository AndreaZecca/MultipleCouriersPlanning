import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np


technologies = ["CP", "SAT", "SMT", "MIP", "SMT-LIB"]


keys_to_method = {
    "CP": {
        'Gecode_sb': 'Gecode + SB',
        'Chuffed_sb': 'Chuffed + SB',
    },
    "SAT": {
        'pb': 'SAT + Pseudo-Boolean',
    },
    "SMT": {
        "symmetry_breaking": "SMT + SB"
    },
    "MIP":{
        'cbc': 'CBC',
    },
    "SMT-LIB":{
        'z3': "SMTLIB-z3"
    }
}


for tech in technologies:
    try:
        dir_path = f"./{tech}"
        # Get all files
        files = os.listdir(dir_path)
        # Filter only json files
        files = [f"./{tech}/{file}" for file in files if file.endswith(".json")]
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
                if method in keys_to_method[tech].keys():
                    method_result = total_results[method]
                    sol_found = method_result['time']
                    to_append[keys_to_method[tech][method]] =  int(sol_found) if isinstance(sol_found, int) else sol_found.upper() 
                    to_append[f'SOL_{method}'] = method_result['sol'] is not None and method_result['optimal'] == True
                else:
                    continue
            results.append(to_append)
        df = pd.DataFrame(results)
        df.index += 1 
        df.to_csv(f"./{tech}.csv", index=True)
    except Exception as e:
        print(e)
        continue

max_instances = 10

cp_df = pd.read_csv("./CP.csv")
sat_df = pd.read_csv("./SAT.csv")
smt_df = pd.read_csv("./SMT.csv")
mip_df = pd.read_csv("./MIP.csv")
z3_df = pd.read_csv("./SMT-LIB.csv")

chuf_sb_sol = cp_df['Chuffed + SB'].tolist()[:max_instances]
chuf_sb_opt = cp_df['SOL_Chuffed_sb'].tolist()[:max_instances]
chuf_marker = np.array(['green' if c else 'red' for c in chuf_sb_opt])

gec_sb_sol = cp_df['Gecode + SB'].tolist()[:max_instances]
gec_sb_opt = cp_df['SOL_Gecode_sb'].tolist()[:max_instances]
gec_marker = np.array(['green' if c else 'red' for c in gec_sb_opt])

sat_sol = sat_df['SAT + Pseudo-Boolean'].tolist()[:max_instances]
sat_opt = sat_df['SOL_pb'].tolist()[:max_instances]
sat_marker = np.array(['green' if c else 'red' for c in sat_opt])

smt_sol = smt_df['SMT + SB'].tolist()[:max_instances]
smt_opt = smt_df['SOL_symmetry_breaking'].tolist()[:max_instances]
smt_marker = np.array(['green' if c else 'red' for c in smt_opt])

mip_sol = mip_df['CBC'].tolist()[:max_instances]
mip_opt = mip_df['SOL_cbc'].tolist()[:max_instances]
mip_marker = np.array(['green' if c else 'red' for c in mip_opt])

z3_sol = z3_df['SMTLIB-z3'].tolist()[:max_instances]
z3_opt = z3_df['SOL_z3'].tolist()[:max_instances]
z3_marker = np.array(['green' if c else 'red' for c in z3_opt])

instances = list(range(1,max_instances+1))



f, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(20,11))
# plt.figure(figsize=(40,20))

ax.plot(instances, chuf_sb_sol)
ax.plot(instances, gec_sb_sol)
ax.plot(instances, sat_sol)
ax.plot(instances, smt_sol)
ax.plot(instances, z3_sol)
ax.plot(instances, mip_sol)

ax2.plot(instances, chuf_sb_sol)
ax2.plot(instances, gec_sb_sol)
ax2.plot(instances, sat_sol)
ax2.plot(instances, smt_sol)
ax2.plot(instances, z3_sol)
ax2.plot(instances, mip_sol)

ax.scatter(instances, chuf_sb_sol, c=chuf_marker, s=100)
ax.scatter(instances, gec_sb_sol, c=gec_marker, s=100)
ax.scatter(instances, sat_sol, c=sat_marker, s=100)
ax.scatter(instances, smt_sol, c=smt_marker, s=100)
ax.scatter(instances, z3_sol, c=z3_marker, s=100)
ax.scatter(instances, mip_sol, c=mip_marker, s=100)

ax2.scatter(instances, chuf_sb_sol, c=chuf_marker, s=100)
ax2.scatter(instances, gec_sb_sol, c=gec_marker, s=100)
ax2.scatter(instances, sat_sol, c=sat_marker, s=100)
ax2.scatter(instances, smt_sol, c=smt_marker, s=100)
ax2.scatter(instances, z3_sol, c=z3_marker, s=100)
ax2.scatter(instances, mip_sol, c=mip_marker, s=100)

ax.set_ylim(60, 305)  # most of the data
ax2.set_ylim(0, 40)  # outliers only
d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass to plot, just so we don't keep repeating them
kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

ax.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax.xaxis.tick_top()
ax.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()

ax.xaxis.set_ticks(np.arange(1, 22, 1))
ax2.xaxis.set_ticks(np.arange(1, 22, 1))
# set x fontsize
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)
for tick in ax2.xaxis.get_major_ticks():
    tick.label.set_fontsize(20)

# set y fontsize
for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(20)
for tick in ax2.yaxis.get_major_ticks():
    tick.label.set_fontsize(20)
ax.grid(True)
ax2.grid(True)
plt.plot()
ax.legend(['Chuffed+SB', 'Gecode+SB', 'SAT+PB', 'SMT w/out SB', 'Z3-SMTLIB', 'MIP+CBC'],loc='upper left', fontsize=25)
plt.savefig("./chart.png")

# deleting csv files
os.remove("./CP.csv")
os.remove("./MIP.csv")
os.remove("./SAT.csv")
os.remove("./SMT.csv")
os.remove("./SMT-LIB.csv")

