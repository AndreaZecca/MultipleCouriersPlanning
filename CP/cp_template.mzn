include "globals.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between packages


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

% couriers do not exceed their max load
constraint
    forall(i in 1..m)(
        sum(k in 1..n where x[i,k] != n+1)(s[x[i,k]]) <= l[i]
    );

constraint 
    forall(j in 1..n) (
        count_eq(x, j, 1)
    )::domain;

% Other ways to express the same constraint
% -------------- Combination of alldifferent + among ----------------
% constraint alldifferent([x[i,k] | i in 1..m, k in 1..n where x[i,k] != n+1])::domain;
% constraint among(n, x, 1..n)::domain;

% -------------- Using partition_set ----------------
% constraint partition_set([array2set([x[i,k] | k in 1..n+1 where x[i,k] != n+1]) | i in 1..m],1..n);


%%%%%%%% SYMMETRY BREAKING CONSTRAINTS %%%%%%%%%%
% once a courier arrive to depot (j = n+1), it can't depart from there
constraint
    forall(i in 1..m, k in 2..n where x[i,k-1] == n+1)(
        x[i,k] = n+1
    );

% symetry breaking constraint between couriers with the same load using lex
constraint
    forall(i in 1..m, z in 1..m where i!=z /\ l[i] == l[z])(
    lex_lesseq([x[i,k] | k in 1..n] , [x[z,k] | k in 1..n])
    );

%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m)(
        y[i] = sum(k in 1..n+1)(distances[x[i,k-1],x[i,k]])
    );

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)

LINEA

% output
output 
    [
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