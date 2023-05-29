%%%%%%%%% DATA %%%%%%%%%%
int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between packages
int: mindist;
int: max_dist;
int: time;

int: bound_dist_1 = sum([max(distances[i,1..n+1]) | i in 1..n]);
int: bound_dist_2 = max(distances) * (n-m+1);

% output of the two bounds
output [
    "Sum of max for each row of distances: \(bound_dist_1)\n",
    "Max of distances * (n-m+1): \(bound_dist_2)\n"
]