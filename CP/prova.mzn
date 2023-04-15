include "globals.mzn";

array[1..10] of int: a = [12,123,414,51,62,73,84,95,1,0];

int: b = sum(j in 1..3) (
    a[j]
);

output ["end = \(b)\n"];
