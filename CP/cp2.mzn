include "globals.mzn";

int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between package and package

%%%%%
% x[i,k] is the package taken at time k by courier i
array[1..m,0..n+1] of var 1..n+1: x; 

% y[i] is the total distance travelled by courier i
array[1..m] of var 0..sum(distances): y;

% couriers start and end at depot
constraint 
forall(i in 1..m)(
    x[i,0] = n+1 /\ x[i,n+1] = n+1
); 

% couriers do not exceed their max load
constraint
forall(i in 1..m)('
    sum(k in 1..n)(s[x[i,k]]) <= l[i]         % ?????????
);

% no package is delivered by more than one courier
constraint
forall(i in 1..m, k in 1..n)(
    forall(j in 1..m, t in 1..n)(
        (x[i,k] = n+1 /\ x[j,t] = n+1) \/ (i != j) -> (x[i,k] != x[j,t])
    )
);

% no package is delivered twice from the same courier
constraint
forall(i in 1..m, k,t in 1..n where k != t)(
    (x[i,k] = n+1) \/ (x[i,k] != x[i,t])
);

% calculate y
constraint
forall(i in 1..m)(
    y[i] = sum(k in 1..n)(distances[x[i,k-1],x[i,k]])
);

solve :: int_search(y, input_order, indomain_min)  minimize max(y);

