from pathlib import Path
import os

import click
import numpy as np

@click.command()
@click.argument('max_couriers', type=int)
@click.argument('max_packages', type=int)
@click.argument('max_max_load', type=int)
@click.argument('max_weight', type=int)
@click.argument('max_distance', type=int)
@click.argument('count', type=int)
def main(max_couriers, max_packages, max_max_load, max_weight, max_distance, count):
    for i in range(count):
        m = np.random.randint(max_couriers // 3, max_couriers + 1)
        n = np.random.randint(max_packages // 3, max_packages + 1)
        l = np.random.randint(max_max_load // 3, max_max_load + 1, m, dtype=int)
        s = np.random.randint(max_weight // 3, max_weight + 1, size=(n), dtype=int)
        while np.sum(s) >= np.sum(l):
            s = np.random.randint(max_weight // 3, max_weight + 1, size=(n), dtype=int)
        distances = np.random.randint(1, max_distance + 1, size=(n+1, n+1), dtype=int)
        np.fill_diagonal(distances, 0)
        
        l = [str(x) for x in l]
        s = [str(x) for x in s]
        text = ''

        text += f'm = {m};\n'
        text += f'n = {n};\n'
        text += f'l = [{", ".join(l)}];\n'
        text += f's = [{", ".join(s)}];\n'

        text += 'distances = [| '
        for i in range(n + 1):
            text += ', '.join([str(x) for x in distances[i]])
            if i != n:
                text += ', \n \t\t     | '
        text += ' |];\n'        
        
        instances = os.listdir('./tests')
        instances = [x for x in instances if x.startswith('inst') and x.endswith('.dzn')]
        instances = [int(x[4:-4]) for x in instances]
        if len(instances) == 0:
            k = 0
        else:
            k = max(instances)

        # Save text in inst{k}.dzn
        with open(f'./tests/inst{k+1}.dzn', 'w') as f:
            f.write(text)

        
        


if __name__ == '__main__':
    main()