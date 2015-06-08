# TC_model

Implementation of the LGN-PGN-Cx loop using the NEURON simulation environment with Python interface.

**_Usage:_**

1. First, use `nrnivmodel` to compile the .mod files.
2. To run, type `python main_program.py param_file` in a terminal
   (for example: `python run_trial_lsr_small_cx.py 050_040_005_001_001_090`, for constructing the network topology with parameters speficied in parameter file `050_040_005_001_001_090.txt`. A sample parameter file is already provided.)

* Spike trains could be generated on [Virtual Retina](http://facets.inria.fr/retina/webservice.html) by using the animated gif images in `./stimuli`. Spike train files (`.dat`) are loaded `run_trial_condition_scale.py`, so the naming of the `.dat` files should be identical to that of the `run_trial_condition_scale.py` (for example, to use `spiking3='"contrast/csr'+con_number+'/csr'+con_number+'_rgccell_3976/csr'+con_number+'_rgccell_3976_0'+str(trial_num)+'.dat"'`), the `.dat` file should be placed in a folder called `./contrast`.
* Virtual Retina only gives raw data files (`.spk`) in which spike trains from all cells (normally there are thousands of them) are included. To extrace spike trains from specific cells by ID, use `getdata_mergefile.py` (`python getdata_mergefile.py`).  
* Sample raw data could be found in `./virtual_retina/spk_original`.


##### Network topologies included:
* Topology B, version 1 (`run_trial_condition_small.py`); 
* Topology B, version 2 (`run_trial_condition_larger.py`);
* Topology C, version 1 (`run_trial_condition_small_cx.py`); 
* Topology C, version 2 (`run_trial_condition_larger_cx.py`).

##### Conditions included:
* **csrall**: drifting sinusoidal gratings with varying contrast
* **lsr**: flashing light spots with varying size


