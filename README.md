# TC_model

Implementation of the LGN-PGN-Cx loop.

**_Usage:_**

1. First, use `nrnivmodel` to compile the .mod files.
2. To run, type `python main_program.py param_file` in a terminal
   (for example: `python run_trial_lsr_small_cx.py 050_040_005_001_001_090`, for constructing the network topology with parameters speficied in parameter file `050_040_005_001_001_090.txt`)

* Spike trains could be generated on [Virtual Retina](http://facets.inria.fr/retina/webservice.html) by using the animate gif images in `./stimuli`. Spike train files (`.dat`) are loaded `run_trial_condition_scale.py`, so the naming of the `.dat` files should be identical to that of the `run_trial_condition_scale.py`. 


##### Network topologies included:
Topology B, version 1 (`run_trial_condition_small.py`); Topology B, version 2 (`run_trial_condition_larger.py`)
Topology C, version 1 (`run_trial_condition_small_cx.py`); Topology C, version 2 (`run_trial_condition_larger_cx.py`)

##### Conditions included:
**csrall**: drifting sinusoidal gratings with varying contrast

**lsr**: flashing light spots with varying size


