# discrepant-proofs

This directory contains the two discrepant proofs presented in the paper. Both of them are intended to be refutations of the formula `formula.cnf` in DIMACS format.
The first proof is `specified.drat`. This is a correct specified DRAT refutation of `formula.cnf`, and an incorrect operational DRAT refutation of `formula.cnf`.
The second proof is `operational.drat`. This is an incorrect specified DRAT refutation of `formula.cnf`, and a correct operational DRAT refutation of `formula.cnf`.
State-of-the-art checkers produce the results expected for operational DRAT. This experiment checks these instances with `drat-trim` and `gratgen`.

Run `make.py` to download and compile `drat-trim` and `grat-gen`. To perform the experiment, run `experiment.py`.
