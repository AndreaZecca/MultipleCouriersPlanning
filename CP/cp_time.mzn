include "globals.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m;   % couriers
int: n;   % packages (n >= m)
int: time;
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between packages

int :mindist;%= min(distances[n,0..n]) + min(distances[0..n,n]); % minimum distance to travel when all courriers must deliver at least one package
int : max_dist;
%%%%%%%% VARIABLES %%%%%%%%%%
% x[i,k] is the package taken at time k by courier i
array[1..m,0..time] of var 1..n+1: x; 

% y[i] is the total distance travelled by courier i
array[1..m] of var mindist..max_dist: y;  

% TODO: Do we actually need this variable?
array[1..m] of var 0..sum([l[i] | i in 1..m]): load;

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
    )::domain;
    
% each courier must deliver at least one package
% TODO: check this constraint. With this => lower performance
% constraint 
%     forall(i in 1..m) (
%         x[i,1] != n+1
%     );

% Other ways to express the same constraint
% -------------- Combination of alldifferent + among ----------------
% constraint alldifferent([x[i,k] | i in 1..m, k in 1..time-1 where x[i,k] != n+1])::domain;
% constraint among(n, x, 1..n)::domain;

% -------------- Using partition_set ----------------
% constraint partition_set([array2set([x[i,k] | k in 1..n+1 where x[i,k] != n+1]) | i in 1..m],1..n);


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
    )::domain;

%%%%%%%% OBJECTIVE %%%%%%%%%%
constraint
    forall(i in 1..m)(
        y[i] = sum(k in 1..time)(distances[x[i,k-1],x[i,k]])
    );


% extra:
constraint
    forall(i in 1..m)(
        x[i,1] < n+1 /\
        load[i] > 0
    )::domain;
    
% constraint
%     forall(i in 1..m, k in n-m+1..n)(
%         x[i,k] = n+1
%     );
    
% constraint
%     forall(i in 1..m)(
%         y[i] >= mindist
%     );

%%%%%%%% SEARCH STRATEGY %%%%%%%%%% (Gecode on inst12)
%solve :: int_search(x, dom_w_deg, indomain_min)  minimize max(y); % --3.5 secondss
%solve :: int_search(x, dom_w_deg, indomain_random)  :: restart_linear(10000) minimize max(y);   % FOR GECODE
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