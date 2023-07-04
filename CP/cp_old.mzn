include "globals.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m; 
int: n;   
int: time;
int : min_dist;
int : max_dist;
int: min_solution;
int : at_least_one;
array[1..m] of int: l; 
array[1..n] of int: s; 
int : min_load;
int : max_load;
array[1..n+1, 1..n+1] of int: distances;

%%%%%%%% VARIABLES %%%%%%%%%%
% x[i,k] is the package taken at time k by courier i
array[1..m,0..time] of var 1..n+1: x; 

% y[i] is the total distance travelled by courier i
array[1..m] of var min_dist..max_dist: y;  

% load[i] is the total load of courier i
array[1..m] of var min_load..max_load: load;

% max(y) is the maximum distance travelled by a courier
var min_solution..max_dist: effective_max_dist;

% bins[j] = i means that package j is taken by courier i (used in bin_packing)
array[1..n] of var 1..m : bins;

%%%%%%%% CONSTRAINTS %%%%%%%%%%
% couriers start and end at depot (j = n+1)
constraint 
    forall(i in 1..m)(
        x[i,0] = n+1 /\ x[i,time] = n+1
    ); 

% couriers do not exceed their max load
constraint
    forall(i in 1..m)(
        load[i] == sum(k in 1..time-1 where x[i,k] != n+1)(s[x[i,k]]) /\
        load[i] <= l[i] 
    );

% each package is delivered
constraint 
    forall(j in 1..n) (
        count_eq(x, j, 1)
    );

% if we know that each courier must deliver at least one package:
constraint 
        at_least_one == 1 ->
        forall(i in 1..m)(
            x[i,1] < n+1 /\
            load[i] > 0
        );

% bin packing constraint
constraint
    bin_packing_load(load, bins, s);

% link bins with x
constraint
    forall(j in 1..n)(
        exists(k in 1..time)(
            x[bins[j],k] = j
        )
    );

%%%%%%%% SYMMETRY BREAKING CONSTRAINTS %%%%%%%%%%
% once a courier arrive to depot (j = n+1), it can't depart from there
constraint
    forall(i in 1..m, k in 2..time-1 where x[i,k-1] == n+1)(
         x[i,k] = n+1
    );

% symetry breaking constraint between couriers with specified load using lex
constraint
    forall(i in 1..m-1, z in i+1..m where l[i] == l[z])(
        lex_lesseq([x[i,k] | k in 1..time-1] , [x[z,k1] | k1 in 1..time-1])
    );

% symmetry breaking constraint between couriers with >= max load
constraint
    forall(i in 1..m-1, z in i+1..m where l[i] >= l[z])(
        load[i] >= load[z]
    );

% alldifferent on all the elements of x different from n+1
constraint
    alldifferent([x[i,k] | i in 1..m, k in 1..time-1 where x[i,k] != n+1]);

%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m)(
        y[i] = sum(k in 1..time)(distances[x[i,k-1],x[i,k]])
    );

constraint
    effective_max_dist == max(y);

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)
%solve :: int_search(x, dom_w_deg, indomain_min)  minimize max(y); % --3.5 secondss
%solve ::int_search(x, dom_w_deg, indomain_random) :: restart_linear(1000) minimize effective_max_dist;   % FOR GECODE
solve :: int_search(x, first_fail, indomain_min) minimize effective_max_dist; % FOR CHUFFED
  
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
        "Courier \(i) at time \(k) arrives to \(j); \n"  | i in (1..m), k in (1..time), j in (1..n) where fix(x[i,k]) == j
    ];