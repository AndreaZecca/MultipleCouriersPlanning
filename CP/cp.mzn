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
array[1..m] of var 0..n*sum([max(distances[i,1..n+1]) | i in 1..n]): y;  % check if it's more correct | i in 1..n+1
% another possible upperbound is n*max(distances)

array[1..m] of var 0..sum([l[i] | i in 1..m]): load;

%%%%%%%% CONSTRAINTS %%%%%%%%%%
% couriers start and end at depot (j = n+1)
constraint 
    forall(i in 1..m)(
        x[i,0] = n+1 /\ x[i,n+1] = n+1
    ); 

% couriers do not exceed their max load
constraint
    forall(i in 1..m)(
        load[i] == sum(k in 1..n where x[i,k] != n+1)(s[x[i,k]]) /\
        load[i] <= l[i] 
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

% symetry breaking constraint between couriers with specified load using lex
constraint
    forall(i in 1..m-1, z in i+1..m where l[i] == l[z])(
        lex_lesseq([x[i,k] | k in 1..n] , [x[z,k1] | k1 in 1..n])
    );

% symmetry breaking constraint between couriers with >= max load
constraint
    forall(i in 1..m-1, z in i+1..m where l[i] >= l[z])(
        load[i] >= load[z]
    );

%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m)(
        y[i] = sum(k in 1..n+1)(distances[x[i,k-1],x[i,k]])
    );

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)
%solve :: int_search(x, dom_w_deg, indomain_min)  minimize max(y); % --3.5 secondss
solve :: int_search(x, input_order, indomain_min)  minimize max(y);

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