include "globals.mzn";
include "nosets.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between package and package

%%%%%%%% VARIABLES %%%%%%%%%%
% x[i,k] is the package taken at time k by courier i
array[1..m,0..n+1] of var 1..n+1: x; 

% y[i] is the total distance travelled by courier i
array[1..m] of var 0..n*max(distances): y;


%%%%%%%% CONSTRAINTS %%%%%%%%%%
% couriers start and end at depot (j = n+1)
constraint 
forall(i in 1..m)(
    x[i,0] = n+1 /\ x[i,n+1] = n+1
); 

% symmetry-breaking constraint
% once a courier arrive to depot (j = n+1), it can't depart from there
constraint
forall(i in 1..m, k in 2..n where x[i,k-1] == n+1)(
    x[i,k] = n+1
);

% couriers do not exceed their max load
constraint
forall(i in 1..m)(
    sum(k in 1..n where x[i,k] != n+1)(s[x[i,k]]) <= l[i]
);

% all packages must be delivered
constraint
    among(n, x, 1..n)::domain;

% constraint
%     partition_set(
%         [array2set([x[i,k] | k in 1..n where x[i,k] != n+1]) | i in 1..m], 1..n
%     );

constraint alldifferent([x[i,k] | i in 1..m, k in 1..n where x[i,k] != n+1])::domain;

% calculation of distances
constraint
forall(i in 1..m)(
    y[i] = sum(k in 1..n+1)(distances[x[i,k-1],x[i,k]])
);

solve :: int_search(x, input_order, indomain_min)  minimize max(y); %dom_w_deg, indomain_random


% output
output [
        "\nDistances traveled by each courier: \n"
    ] ++ 
    [
        "Courier \(i) = \(y[i]);\n" | i in (1..m)
    ] ++
    [
        "\nPath taken by each courier: \n"
    ] ++
    [
        "Courier \(i) at time \(k) arrives to \(j); \n"  | i in (1..m), k in (1..n+1), j in (1..n) where fix(x[i,k]) == j
    ];