import os
import re
import numpy as np


def main():
    for instance in sorted(os.listdir("./Original_Instances")):
        if not instance.endswith(".dat"):
            continue
        # print(f"Instance: {instance}")
        with open(f"./Original_Instances/{instance}") as f:
            text = f.read()
        lines = text.split("\n")
        # regex to get a number from a string
        num_regex = r"(\d+)"
        lines = [x for x in lines if x != ""]
        lines = [x.strip() for x in lines]
        m = int(re.findall(num_regex, lines[0])[0])
        n = int(re.findall(num_regex, lines[1])[0])
        l = [int(x) for x in re.findall(num_regex, lines[2])]
        s = [int(x) for x in re.findall(num_regex, lines[3])]

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
        # print('Original:', n + 1, 'Bound1:', time_bound1, 'Bound2:', time_bound2, 'Min:', time)
        
        distances = []
        for i in range(4, 4 + n + 1):
            distances.append([int(x) for x in re.findall(num_regex, lines[i])])
        
        distances = np.array(distances)

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
            mindist = 0
        else:
            mindist = min(min1, min2)*2
        
        # calculate min_solution

        min_solution = np.max([distances[n, j] + distances[j, n] for j in range(n)])

        max_load = np.min([np.max(l), np.sum(sorted(s, reverse=True)[:time])])
        min_load = np.min(s) * each_courier_at_least_one

        text = ''
        l = [str(x) for x in l]
        s = [str(x) for x in s]

        text += f'm = {m};\n'
        text += f'n = {n};\n'
        text += f'l = [{", ".join(l)}];\n'
        text += f's = [{", ".join(s)}];\n'
        text += f'min_dist = {mindist};\n'
        text += f'max_dist = {max_dist};\n'
        text += f'min_solution = {min_solution};\n'
        text += f'time = {time};\n'
        text += f'at_least_one = {each_courier_at_least_one};\n'
        text += f'min_load = {min_load};\n'
        text += f'max_load = {max_load};\n'
        text += 'distances = [| '
        for i in range(n+1):
            text += ', '.join([str(x) for x in distances[i]])
            if i != n:
                text += ', \n \t\t     | '
        text += ' |];\n'        
        
        # change instance extension into .dzn
        instance = instance.replace(".dat", ".dzn")

        with open (f"Formatted_Instances/{instance}", "w") as f:
            f.write(text)
        # print()
if __name__ == '__main__':
    main()