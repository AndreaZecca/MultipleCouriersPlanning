int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between packages



output [
    "sum(max item per row) \(sum([max(distances[i,1..n+1]) | i in 1..n]))\n",
    "Max(distances)*n \(max(distances)*n)",
]