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

array [1..n] of var int: bins;
constraint 
    bin_packing_capa(
        l,
        bins,
        s
    );


output [
    "bins: \(bins)\n"
];