# unit-deletions

This directory contains the experiment on the occurrence of unit clause deletion instructions in DRAT proofs generated by SAT solvers. The obtained results are contained in `results.txt`. We provide below instructions to reproduce this experiment.

Run `make.py BENCHMARKS OUTPUT PROOFS` to configure and compile all necessary software. `BENCHMARKS` is the directory where benchmarks should be downloaded (this is not done in this step). `OUTPUT` is the directory where the output of stdout and stderr streams for each run will be generated. `PROOFS` is the temporary directory where proofs will be stored during execution.

If benchmarks need to be downloaded, run `benchmarks.py`; this will take some time, go grab a coffee. This stores the benchmarks in the directory provided in the previous step.

To run the experiments through `sbatch`, run `submit.sh`. If instead you want to run the experiments sequentially, run `sequential.py`. There are 3144 benchmarks, so you probably do not want to run all of them. In that case, run `sequential.py N` to run the experiment for N randomly selected benchmarks.

Once the experiment has run for all benchmarks, run `extract.py RESULTS` to generate a TSV table containing the obtained results in `RESULTS`. To analyze this file, run `analyze.py RESULTS`.
