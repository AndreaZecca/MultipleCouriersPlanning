include "globals.mzn";

int: m;   % couriers
int: n;   % packages (n >= m)
array[1..m] of int: l;   % max load of each courier
array[1..n] of int: s;   % package sizes
array[1..n+1, 1..n+1] of int: distances;   % distances between package and package

%%%%%%% first formalization %%%%%%%
array[1..m,0..n+1,0..n+1] of var 0..1: x;   % x[i,j,k] = 1 if courier i takes package j and delivers it at time k

% define and initialize y to 0
array[1..m] of var 0..sum(distances): y; % y[i] = distance traveled by courier i

% all the couriers start from the origin at time 0
constraint
    forall(i in 1..m) (
        x[i,0,0] = 1
    );

% all the couriers are back to the origin at the end
constraint
    forall(i in 1..m) (
        x[i,n+1,n+1] = 1
    );

% in each moment k each courier i must be in a position j
constraint
    forall(i in 1..m) (
        forall(k in 0..n+1) (
            sum(j in 0..n+1) (
                x[i,j,k]
            ) = 1
        )
    );

% initial position only at time 0
constraint
    forall(i in 1..m) (
        forall(k in 1..n+1) (
            x[i,0,k] = 0
        )
    );

% each package must be delivered exactly once
constraint
    forall(j in 1..n) (
        sum(i in 1..m) (
            sum(k in 1..n) (
                x[i,j,k]
            )
        ) = 1
    );

% each courier can deliver at most l[i] units of packages

constraint
    forall(i in 1..m) (
        sum(j in 1..n) (
            sum(k in 1..n) (
                x[i,j,k]*s[j]
            )
        ) <= l[i]
    );

% distances calculation
% constraint
%     forall(i in 1..m) (
%         forall(a in 1..n) (
%             forall(b in 1..n where a!=b) (
%                 forall(k in 1..n+1) (
%                     if k = 1 then
%                         y[i] = y[i] + x[i,b,k] * distances[b,n+1]
%                     else 
%                         y[i] = y[i] + x[i,a,k-1] * x[i,b,k] * distances[a,b]
%                     endif
%                 )
%             )
%         )
%     );

solve :: int_search(y, input_order, indomain_min)  minimize max(y);

output [
        "Distances traveled by each courier: \n"
    ] ++ 
    [
        "Courier \(i) = \(y[i]);\n" | i in (1..m)
    ] ++
    [
        "Path taken by each courier: \n"
    ] ++
    [
        "Courier \(i) at time \(k) takes the package \(j); \n"  | i in (1..m), k in (0..n+1), j in (0..n+1) where fix(x[i,j,k]) == 1
    ];


