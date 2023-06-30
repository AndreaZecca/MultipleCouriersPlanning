import os
import re
import numpy as np

def main():
    for instance in os.listdir("../Formatted_Instances/"):
        if not instance.endswith(".dzn"):
            continue
        with open(f"../Formatted_Instances/{instance}") as f:
            text = f.read()
        num_regex = r"(\d+)"
        lines = text.split("\n")
        lines = [x for x in lines if x != ""]
        lines = [x.strip() for x in lines]
        m = int(re.findall(num_regex, lines[0])[0])
        n = int(re.findall(num_regex, lines[1])[0])
        l = [int(x) for x in re.findall(num_regex, lines[2])]
        s = [int(x) for x in re.findall(num_regex, lines[3])]
        min_dist = int(re.findall(num_regex, lines[4])[0])
        max_dist = int(re.findall(num_regex, lines[5])[0])
        time = int(re.findall(num_regex, lines[6])[0])
        at_least_one = int(re.findall(num_regex, lines[7])[0])
        distances = []
        for i in range(8, 8 + n + 1):
            distances.append([int(x) for x in re.findall(num_regex, lines[i])])
        distances = np.array(distances)

        py_inst = ""

        inst_number = instance[4:6]

        py_inst += f"inst{inst_number} = "
        py_inst += "{\n"
        py_inst += f"    'm': {m},\n"
        py_inst += f"    'n': {n},\n"
        py_inst += f"    'l': {l},\n"
        py_inst += f"    's': {s},\n"
        py_inst += f"    'min_dist': {min_dist},\n"
        py_inst += f"    'max_dist': {max_dist},\n"
        py_inst += f"    'time': {time},\n"
        py_inst += f"    'at_least_one': {at_least_one},\n"
        py_inst += f"    'distances': {distances.tolist()}\n"
        py_inst += "}"

        with open(f"../Python_Instances/inst{inst_number}.txt", "w") as f:
            f.write(py_inst)

if __name__ == "__main__":
    main()