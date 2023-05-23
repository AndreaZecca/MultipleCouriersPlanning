import os
import numpy as np
import re

def count_zeros():
    for instance in os.listdir('./'):
        if not instance.endswith('.dat'):
            continue
        text = ''
        with open(instance) as f:
            text = f.read()
        lines = text.split("\n")
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
        distances = np.array(distances)
        for i,row in enumerate(distances):
            if np.count_nonzero(row == 0) > 1:
                print(f"Instance: {instance}, at row{i}")
        
if __name__ == '__main__':
    count_zeros()