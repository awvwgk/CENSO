# CENSO - Commandline ENergetic SOrting of Conformer-Rotamer Ensembles
![censo_logo_300dpi](https://github.com/user-attachments/assets/0e6bac6a-2637-4207-8eca-3122ab90112a)
CENSO is a Python package meant to automate refinement of Conformer-Rotamer ensembles on DFT level, as well as calculation of ensemble properties, e.g. NMR parameters.
It can be used from the command line as well as using custom wrapper scripts.

## NEW: CENSO 2.0
This is the updated version of the former CENSO 1.3 program. New features include the possibility to use CENSO as a package from within Python, template files, json outputs, and more! For more information about the use and the capabilities of CENSO 2.0 visit the documentation [here](https://xtb-docs.readthedocs.io/en/latest/CENSO_docs/censo.html).

## CENSO 2.1.3 
In the most recent version of CENSO 2.1, the code was cleaned up and many bug fixes were implemented. When it comes to functionality, the multitemp mode and constraints for the geometry optimization were removed, since they did not work (reliably). Also, a new system for solvent lookup was implemented, which is also going to be used for CENSO 2.2, and completes all solvent name mappings. This way, all solvents should be callable using a multitude of different aliases (if they are available for the respective solvation model). Also, printouts at the end of the UV/Vis and NMR calculations were added.

For usage via the CLI, it is now no longer necessary to provide `--maxcores` or `-i`, since default values are now defined for both cases. It is now also possible to change the minimum number of threads when calling external programs using `--omp-min`. The same can be achieved by modifying `Config.OMPMIN` in Python.

# Installation
Can be installed using `pip` by running

    pip install .

If you want to install and run `CENSO` without `pip` you can add the `CENSO/src` directory to your `$PYTHONPATH` and add `CENSO` to your `$PATH`.

# Usage
After installing CENSO via `pip`, it can be called using either
```
python -m censo
```
or 
```
censo
```
as now the CLI is implemented as entry point. As of version 2.1.3, it is also no longer necessary to call CENSO using `--maxcores` or `-i`, since both have default values now.

For information about command line options use the `-h` option.

If you chose not to install it using `pip` and you added the `CENSO` directory to your `$PATH`, you can also just invoke `censo`.

CENSO can also be used as a package. A basic setup for a CENSO run in a Python file could look like this:
```python
from censo.ensembledata import EnsembleData
from censo.configuration import configure
from censo.ensembleopt import Prescreening, Screening, Optimization
from censo.properties import NMR
from censo.params import Config

# CENSO will put all files in the current working directory (os.getcwd())
input_path = "rel/path/to/your/inputfile" # path relative to the working directory
ensemble = EnsembleData(input_file=input_path) 
# the above can be used if you molecule is neutral and closed shell, otherwise
# it is necessary to proceed with e.g.
# ensemble = EnsembleData()
# ensemble.read_input(input_path, charge=-1, unpaired=1)

# If the user wants to use a specific rcfile:
configure("/abs/path/to/rcfile")

# Get the number of available cpu cores on this machine
# This is also the default value that CENSO uses
# This number can also be set to any other integer value and automatically checked for validity
Config.NCORES = os.cpu_count()

# Another possibly important setting is OMP, which will get used if you disabled the automatic 
# load balancing in the settings
Config.OMP = 4

# The user can also choose to change specific settings of the parts
# Please take note of the following:
# - the settings of certain parts, e.g. Prescreening are changed using set_setting(name, value)
# - general settings are changed by using set_general_setting(name, value) (it does not matter which part you call it from)
# - the values you want to set must comply with limits and the type of the setting
Prescreening.set_setting("threshold", 5.0)
Prescreening.set_general_setting("solvent", "dmso")

# It is also possible to use a dict to set multiple values in one step
settings = {
    "threshold": 3.5,
    "func": "pbeh-3c",
    "implicit": True,
}
Screening.set_settings(settings, complete=False)  
# the complete kwarg tells the method whether to set the undefined settings using defaults or leave them on their current value


# Setup and run all the parts that the user wants to run
# Running the parts in order here, while it is also possible to use a custom order or run some parts multiple times
# Running a part will return an instance of the respective type
# References to the resulting part instances will be appended to a list in the EnsembleData object (ensemble.results)
# Note though, that currently this will lead to results being overwritten in your working directory
# (you could circumvent this by moving/renaming the folders)
results, timings = zip(*[part.run(ensemble) for part in [Prescreening, Screening, Optimization, NMR]])

# You access the results using the ensemble object
# You can also find all the results the <part>.json output files
print(ensemble.results[0].data["results"]["CONF5"]["sp"]["energy"])
```

# License

``CENSO`` is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

``CENSO`` is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose. See the
GNU Lesser General Public License for more details.
