import os

for inst_name in sorted(os.listdir()):
    if not inst_name.endswith(".dzn"):
        continue
    print(inst_name)
    os.system(f'minizinc distance.mzn ./{inst_name}')
