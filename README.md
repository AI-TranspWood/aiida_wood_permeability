# AITW - AiiDA workchain for wood permeability

[AiiDA](https://aiida.readthedocs.io/projects/aiida-core/en/stable/) workflow for automated calculation of the wood permeability using the lattice Boltzmann method (LBM) implemented in [OpenLB](https://www.openlb.net/).

## Features

- Generate the wood structure using the [AITW microstructure generator](https://github.com/AI-TranspWood/AITW_microstructures)
- Apply the porosity filter to prepared the structure for the permeability calculation (included in the generator and ported from https://github.com/AI-TranspWood/aitw_filter_structure)
-  Run the [OpenLB](https://www.openlb.net/) permeability calculation using the code from https://github.com/AI-TranspWood/olb_permeability

## Installation

```bash
cd <PATH to folder with pyproject.toml>
pip install .[tui]
```

The extra dependencies are optional and used for:

- `tui`: for adding an `aitw-permeability tui` subcommand launching a text user interface (TUI) to help setting up the workchain inputs.

## Usage

The package provides the following AiiDA entry point that can be used to load the workchains

### Main workchain

Workchains performing the full calculations advertised by the package.

- `aitw.wood_permeability.wood_permeability`: Perform a full calculation from the microstructure generation to computing its permeability

### Sub-workchains

Workchains performing smaller parts of the full calculation that can also be used independently.


- `aitw.wood_permeability.wood_structure_generator` Run the microstructure generator to create a wood structure with the desired properties.
- `aitw.wood_permeability.structure_filter` Apply the porosity filter to the generated structure to prepare it for the permeability calculation.
- `aitw.wood_permeability.olb_permeability` Run the OpenLB permeability calculation on the filtered structure to compute its permeability. Submits 3 OpenLB calculations for the 3 principal directions of the structure.

### CLI

The tool makes available 2 main cli commands grouped following the normal aiida CLI style.

- `aitw-permeability workflow launch generate_permeability`: Launch the viscosity workchain from the command line.

For all commands you can use the `-h` / `--help` flag to get more information about the available options.

example

```bash
aitw-permeability workflow launch generate_permeability \
    --wood-ms <WOOD_MS_CODE_IDENTIFIER> \
    --permeability-code <PERMEABILITY_CODE_IDENTIFIER> \
    --wood-type birch \
    --generate-params-file <JSON_GENERATOR_PARAMS_FILE> \
    --filter-params-file <JSON_FILTER_PARAMS_FILE> \
    --resolution 40
```

Replace the `<CODE IDENTIFIER>` with the actual code identifiers (PK or label) of the installed codes in your AiiDA database. \
Adjust the other parameters as needed.

OUTPUT:

``` bash
# ...
# REPORT
# ...
# Report: [3284|OLBPermeabilityWorkChain|inspect_lb_permeability]: ✓ Permeability tensor calculated:
# Report: [3284|OLBPermeabilityWorkChain|inspect_lb_permeability]:   k_x = 2.018e-11 m²
# Report: [3284|OLBPermeabilityWorkChain|inspect_lb_permeability]:   k_y = 2.046e-11 m²
# Report: [3284|OLBPermeabilityWorkChain|inspect_lb_permeability]:   k_z = 5.176e-11 m²
# ...
# Output link               Node pk and type
# ------------------------------------------------------------
# filter__actual_porosity   Float<3283>
# filter__params            Dict<3281>
# filter__parsed_params     Dict<3279>
# filter__structure         SinglefileData<3276>
# generator__distortion     ArrayData<3263>
# generator__parsed_params  Dict<3262>
# generator__volume__after_global SinglefileData<3257>
# generator__volume__after_local SinglefileData<3258>
# generator__volume__final  SinglefileData<3260>
# generator__volume__initial SinglefileData<3259>
# permeability__permeability_tensor Dict<3307>

```

**NOTE**: Not all possible inputs to the workchain are exposed through the CLI. For more advanced usage, consider running the workchain programmatically.

### Programmatically

See the [CLI file](aiida_wood_permeability/cli/workflows/full.py) for an example of how to run the workchain programmatically.

EG: The same code in the function `launch_workflow` could be adjusted and used in a python script to automate launching the workflow for multiple molecules/parameters at once.
Using the daemon (requires AiiDA to be configured with RabbitMQ with ZeroMQ and a database, or AiiDA>=2.9.x) is required to run all the submitted workchains in parallel.
