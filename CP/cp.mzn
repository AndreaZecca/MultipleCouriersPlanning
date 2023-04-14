int m   % couriers
int n   % packages (n >= m)
array[1..m] of var int: l;   % max load of each courier
array[1..n] of var int: s;   % package sizes
array[1..n+1, 1..n+1] of var int: distances;   % distances between package and package

%%%%%%% first formalization %%%%%%%
array[1..m,0..n,0..n+1] of var 0..1: x;   % x[i,j,k] = 1 if courier i takes package j and delivers it at time k
array[1..m] of var int: y; % y[i] = distance traveled by courier i

constraint
    forall(i in 1..m) (
        x[i,0,0] = true;
    );

constraint
    forall(i in 1..m) (
        y[i] = 0;
        forall(a in 1..n) (
            forall(b in 1..n where a!=b) (
                forall(k in 1..n+1) (
                    y[i] += x[i,a,k-1] * x[i,b,k] * distances[a,b]
                )
            )
        )
    );

% solve :: int_search(s, input_order, indomain_min)  minimize max;

%%%%%%% second formalization %%%%%%%
array[1..m,1..n] of var int: xx;   % y[i,j] = k if courier i takes package j and delivers it at time k (-1 if never stops at j)