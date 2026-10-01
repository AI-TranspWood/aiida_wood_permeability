# -*- coding: utf-8 -*-
"""Pre-defined overridable options for commonly used command line interface parameters."""
from aiida.cmdline.params import types
from aiida.cmdline.params.options import OverridableOption
import click


def validate_resolution(ctx, param, value):
    """Validate that the resolution is a comma-separated list of three positive integers."""
    if value is None:
        return value
    try:
        resolution = [int(v) for v in value.split(',')]
        if len(resolution) != 3 or any(v <= 0 for v in resolution):
            raise ValueError
        return resolution
    except:
        raise click.BadParameter('Resolution must be a comma-separated list of three positive integers.')


WOOD_MS_CODE = OverridableOption(
    '--wood-ms', 'wood_ms_code', type=types.CodeParamType(entry_point='core.shell'),
    help='A single code for wood_ms (e.g. wood_ms@localhost).'
)

WOOD_TYPE = OverridableOption(
    '--wood-type',
    'wood_type',
    type=click.Choice(['birch', 'spruce']),
    help='The type of wood to simulate.'
)

GENERATE_PARAMS_FILE = OverridableOption(
    '--generate-params-file',
    'generate_params_file',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help='Path to a JSON file containing the simulation parameters.'
)

FILTER_PARAMS_FILE = OverridableOption(
    '--filter-params-file',
    'filter_params_file',
    type=click.Path(exists=True, dir_okay=False, readable=True),
    help='Path to a JSON file containing the simulation parameters.'
)

WOOD_STRUCTURE_FILE = OverridableOption(
    '--wood-structure-file',
    'wood_structure_file',
    type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True),
    help='Path to a file containing the wood structure.'
)

WOOD_STRUCT_NODE = OverridableOption(
    '--wood-structure-node',
    'wood_structure_node',
    type=types.DataParamType(sub_classes=('aiida.data:singlefile',)),
    help='A SinglefileData node containing the wood structure.'
)

WOOD_MS_CELL_R = OverridableOption(
    '--cell-r',
    'cell_r',
    type=click.FloatRange(min=0.0, min_open=True),
    help='The cell_r parameter for the simulation.'
)

WOOD_MS_CELL_WALL_THICKNESS = OverridableOption(
    '--cell-wall-thickness',
    'cell_wall_thickness',
    type=click.FloatRange(min=0.0, min_open=True),
    help='The cell_wall_thickness parameter for the simulation.'
)

WOOD_MS_RESOLUTION = OverridableOption(
    '--grid-resolution',
    'grid_resolution',
    type=click.STRING,
    callback=validate_resolution,
    help='A comma-separated list of three integers representing the resolution in xyz directions (e.g., "10,10,10").'
)

PARAM_SEED = OverridableOption(
    '--seed',
    'seed',
    type=click.IntRange(min=0),
    help='The seed for the random number generator.'
)
