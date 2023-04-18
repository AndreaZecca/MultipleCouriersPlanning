include "globals.mzn";
include "nosets.mzn";

% ------------------------------------------------------------ %
% Testing sum function

% array[1..10] of int: a = [12,123,414,51,62,73,84,95,1,0];

% int: b = sum(j in 1..3) (
%     a[j]
% );
% output ["end = \(b)\n"];


% ------------------------------------------------------------ %
% Testing partition_set predicate
% 8,2,4,5,8,8,8,8,8
% 8,3,6,8,8,8,8,8,8
% 8,1,7,8,8,8,8,8,8

int: m;
int: n;

% array[1..m,0..n+1] of int: x = array2d(1..m,0..n+1,[8,2,4,5,8,8,8,8,8,8,3,6,8,8,8,8,8,8,8,1,7,8,8,8,8,8,8]); 
array[1..m, 1..n+2] of int: x;


constraint 
    partition_set([array2set([x[i,k] | k in 1..n+1 where x[i,k] != n+1])| i in 1..m],1..n);

solve satisfy;