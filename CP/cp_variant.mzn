include "globals.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m; 
int: n;   
int: time;
int : min_dist;
int : max_dist;
int : at_least_one;
array[1..m] of int: l; 
array[1..n] of int: s; 
array[1..n+1, 1..n+1] of int: distances;

%%%%%%%%% VARIABLES %%%%%%%%%%

% x[i, j1] = j2 means that the ith courier will go from the j1th node to the j2th node
% An assignment of 0 means that the courier will not start from j1
array[1..m, 1..n+1] of var 0..n+1: x;

% y[i] is the total distance travelled by courier i
array[1..m] of var min_dist..max_dist: y;

% load[i] is the total load of courier i
%array[1..m] of var 0..sum([l[i] | i in 1..m]): load;


%%%%%%%% CONSTRAINTS %%%%%%%%%%
% couriers start and end at depot (j = n+1)
constraint
    forall(i in 1..m) (
        exists(j in 1..n+1)(
            x[i, n+1] = j
        ) /\
        exists(j in 1..n+1)(
            x[i, j] = n+1
        )
    );

% there can be at most one path for a given courier
% constraint
%     forall(i in 1..m) (
%         forall(j1 in 1..n+1) (
%             x[i, j1] != 0 => exists(j2 in 1..n+1) (x[i, j2] = j1)
%         )
%     );

% variant with circuit
constraint
    forall(i in 1..m) (
        circuit([x[i, j] | j in 1..n+1])
    );

% couriers do not exceed their max load
constraint
    forall(i in 1..m) (
        sum([(if x[i, j1] == 0 then 0 else s[j1]) | j1 in 1..n]) <= l[i]
    );

% each package is delivered
constraint
    forall(j1 in 1..n) (
        exists(i in 1..m) (
            x[i, j1] != 0
        )
    );

%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m) (
        y[i] = sum([
            if x[i, j1] == 0 then
                0
            else
                distances[j1, x[i, j1]]
        | j1 in 1..])
    );

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)
%solve :: int_search(x, dom_w_deg, indomain_min)  minimize max(y); % --3.5 secondss
%solve ::int_search(x, dom_w_deg, indomain_random) :: restart_linear(10000) minimize max(y);   % FOR GECODE
solve :: int_search(x, first_fail, indomain_min) minimize max(y); % FOR CHUFFED

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