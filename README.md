# MultipleCouriersPlanning

MultipleCouriersPlanning is a collection of various solving techniques for the Multiple Couriers Planning problem. It supports the following paradigms:
- Constraint Programming (CP)
- SAT
- Satisfiability Modulo Theory (SMT)
- Mixed Integer Programming (MIP)


## Running the Tests

In order to run the tests:
1. Build the Docker container
2. Run the `run_docker.sh` script
3. From the docker terminal, in the main directory, run the script `main.py` with the following parameters:
 - Path to the json file that defines the instances to run
 - Either `true` or `false` to run in verbose mode

We have provided some custom configurations to run the instances on the paradigms (both a specific one or all of them). It is sufficient to pass to the script one of the file present in ./configurations/.
In alternative, you can build your own configuration following the same structure provided in example_config.json or the ones in ./configutations.