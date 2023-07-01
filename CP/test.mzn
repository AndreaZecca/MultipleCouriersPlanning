include "globals.mzn";

%%%%%%%%% DATA %%%%%%%%%%
int: m; % number of couriers
int: n; % number of packages  
int: time;
int : min_dist;
int : max_dist;
int : at_least_one;
array[1..m] of int: l; % max load of each courier
array[1..n] of int: s; % size of each package
array[1..n+1, 1..n+1] of int: distances; % distances between packages and depot   

%%%%%%%% VARIABLES %%%%%%%%%%

% courier assigned to each package
%array[1..n] of var 1..m: x; 

% packages assigned to each courier
array[1..m, 1..n] of var 0..1: y;

% order of packages considering all the couriers
array[1..n] of var 1..n: order; 

% number of packages assigned to each courier
array[1..m] of var at_least_one..time-1: numpack; %[sum(j in 1..n)(x[j] = i) | i in 1..m];

% y[i] is the total distance travelled by courier i
array[1..m] of var min_dist..max_dist: dist;  

% note: the depot is represented by n+1 element in the distance matrix

% order variable works in this way: 
% to the firts courier are assigned the first numpack[1] packages of the array order, 
% to the second courier are assigned the next numpack[2] packages of the array order,
% and so on...

% start index of the packages assigned to each courier
array[1..m] of var 1..n: start_index = [sum(i in 1..k-1)(numpack[i]) + 1 | k in 1..m];


%%%%%%%% CONSTRAINTS %%%%%%%%%%

% each courier has a maximum load
constraint forall(i in 1..m)(sum(j in 1..n)(s[j] * y[i,j]) <= l[i]);  % old forall(i in 1..m)(sum(j in 1..n)(s[j] * (x[j] = i)) <= l[i]);

% the assignment of order should respect the packages assigned to each courier
constraint forall(i in 1..m)(
  (y[i,order[start_index[i]]]*sum(j in start_index[i]..(start_index[i] + numpack[i] - 1))( y[i,order[j]] )) = numpack[i]
);

% numpack[i] is the number of packages assigned to courier i
constraint forall(i in 1..m)(numpack[i] = sum(j in 1..n)(y[i,j]));

% calculation of distance travelled by each courier taking into accout that each of them start from the depot and must end to the depot
constraint 
  forall(i in 1..m)(
    dist[i] = y[i,order[start_index[i]]]*(
      distances[n+1, order[start_index[i]]] + 
      sum(j in start_index[i]..(start_index[i] + numpack[i] - 2))(distances[order[j], order[j+1]]) + 
      distances[order[start_index[i] + numpack[i] - 1], n+1] 
      )
  );

% the elements of order must be all different
constraint all_different(order);

% the sum of numpack must be equal to the number of packages
constraint sum(i in 1..m)(numpack[i]) = n;

% the sum of y[i] must be equal to the number of packages
constraint sum(i in 1..m, j in 1..n)(y[i,j]) = n;

% numpack[i] must be lower or equal to n-start_index[i]+1
constraint forall(i in 1..m)(numpack[i] <= n-start_index[i]+1);

% we want to minimize the maximum distance travelled by any courier
%solve :: int_search(order, dom_w_deg, indomain_random)  :: restart_linear(10000) minimize max(dist);   % FOR GECODE
solve :: int_search(y, first_fail, indomain_min) minimize max(dist); % FOR CHUFFED

output 
    [
        "\nDistances traveled by each courier: \n"
    ] ++ 
    [
        "Courier \(i) = \(dist[i]);\n" | i in (1..m)
    ] ++
    [
        "\n\nPath taken by each courier: \n"
    ] ++
    [
        "numpacks for courier \(i) = \(numpack[i]);\n" | i in (1..m)
    ]++
    [
        "start_index for courier \(i) = \(start_index[i]);\n" | i in (1..m)
    ]++
    % [
    %     "y for courier \(i) and \(j)= \(y[i,j]);\n" | i in (1..m), j in (1..n)
    % ]++
    % [
    %     "x for package \(i) = \(x[i]);\n" | i in (1..n)
    % ]++
    [
        "order = \(order);\n"
    ];