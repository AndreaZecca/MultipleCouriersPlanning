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

%%%%%%%%% VARIABLES %%%%%%%%%%

var min_solution..max_dist: effective_max_dist;

% x[i, j1] = j2 means that the ith courier will go from the j1th node to the j2th node
% An assignment of 0 means that the courier will not start from j1
array[1..m, 1..n+1] of var 1..n+1: x;

% y[i] is the total distance travelled by courier i
array[1..m] of var min_dist..max_dist: y;

% load[i] is the total load of courier i
% HINT: pass max_load to the model
array[1..m] of var min_load..max_load: load;

array[1..m] of var at_least_one..time: numpacks;

array[1..n] of var 1..m : bins;

%%%%%%%% PREDICATES %%%%%%%%%%
predicate at_most_one(array[int] of var bool:x) =
          forall(i,j in index_set(x) where i < j)(
            (not x[i] \/ not x[j]));

predicate exactly_one(array[int] of var bool:x) =
          at_most_one(x) /\ exists(x);

%%%%%%%% CONSTRAINTS %%%%%%%%%%
% couriers start and end at depot (j = n+1)
% constraint
%     forall(i in 1..m) (
%         x[i, n+1] = n+1 <-> (forall(j1 in 1..n)(x[i, j1] = j1))   
%     );

constraint
    forall(i in 1..m)(
        if x[i, n+1] != n+1 then count([x[i, j1] | j1 in 1..n], n+1, 1) 
        else forall(k in 1..n) (x[i, k] = k) endif
    );

% couriers do not exceed their max load
constraint
    forall(i in 1..m)(
        load[i] == sum([(if x[i, j1] == j1 then 0 else s[j1] endif) | j1 in 1..n]) /\
        load[i] <= l[i] 
    );

% there exists one path for each courier
constraint
    forall(i in 1..m) (
        subcircuit([x[i, j] | j in 1..n+1])
    );

% each package is delivered exactly once
constraint
    forall(j in 1..n) (
        exactly_one(
            [x[i, j] != j | i in 1..m]
        )
    );

% bins creation
constraint bin_packing_load(load, bins, s);

% link bins and x
constraint 
    forall(j in 1..n)(
        x[bins[j], j] != j
    );

% constraint on bins
constraint
    forall(i in 1..m)(
        count_leq(bins, i, numpacks[i])
    );

% constraint on bins
% constraint
%     forall(i in 1..m)(
%         count_leq(bins, i, time)
%     );

% triangular inequality over x
% constraint
%     forall(i in 1..m, j1 in 1..n+1, j2 in 1..n+1 where j1 != j2 /\ x[i,j1] != j1 )(
%         distances[x[i,j1], x[i,x[i,j1]]] <= distances[x[i, j1], j2] + distances[j2, x[i,x[i,j1]]] 
%     );




%%%%%%% TIME BOUNDS %%%%%%%%%
constraint
    forall(i in 1..m)(
        count_eq([x[i, j1] == j1 | j1 in 1..n], 0, numpacks[i])
    );


%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m) (
        y[i] = sum([ distances[j1, x[i, j1]] | j1 in 1..n+1])
    );

constraint
    effective_max_dist = max(y);

%%%%%%%%% SYMMETRY BREAKING %%%%%%%%%%
constraint
    forall(i in 1..m-1, z in i+1..m where l[i] >= l[z])(
        load[i] >= load[z]
    );

constraint
    forall(i in 1..m-1, z in i+1..m where l[i] == l[z])(
        lex_less([x[i,k] | k in 1..n+1] , [x[z,k1] | k1 in 1..n+1])
    );

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)
%solve :: int_search(x, dom_w_deg, indomain_min)  minimize max(y); % --3.5 secondss
%solve ::int_search(x, dom_w_deg, indomain_random) :: restart_linear(1000) minimize effective_max_dist;   % FOR GECODE
solve :: int_search(x, first_fail, indomain_min) minimize effective_max_dist; % FOR CHUFFED
% solve satisfy;

% output
% output 
    % [
    %     "\nDistances traveled by each courier: \n"
    % ] ++ 
    % [
    %     "Courier \(i) = \(y[i]);\n" | i in (1..m)
    % ] ++
    % [
    %     "\nPath taken by each courier: \n"
    % ] ++
    % [
    %     "Courier \(i) starts from \(j1) and arrives to \(j2); \n"  | i in (1..m), j1 in (1..n+1), j2 in (1..n+1) where fix(x[i,j1]) == j2 /\ x[i, j1] != j1
    % ];