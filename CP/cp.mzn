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

% once a courier arrive to j = n+1, it can't depart from there
constraint
forall(i in 1..m, k in 2..n where x[i,k-1] == n+1)(
    x[i,k] = n+1
);

% couriers do not exceed their max load
constraint
forall(i in 1..m)(
    sum(k in 1..n where x[i,k] != n+1)(s[x[i,k]]) <= l[i]
);

% no package j is delivered by more than one courier i at each time k
constraint
forall(j in 1..n)(
    sum(i in 1..m, k in 1..m where x[i,k] = j )(1) = 1
);

% calculate y
constraint
forall(i in 1..m)(
    y[i] = sum(k in 1..n+1)(distances[x[i,k-1],x[i,k]])
);

solve :: int_search(y, input_order, indomain_min)  minimize max(y);

