#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-
"""Launch script for the common relax work chain demonstrator using FLEUR."""
from aiida.engine import run
from aiida.plugins import WorkflowFactory

from aiida_common_workflows.workflows.relax.generator import RelaxType
from aiida_common_workflows.workflows.relax.examples.common import rescale, structure_init

RelaxWorkChain = WorkflowFactory('common_workflows.relax.fleur')

CALC_ENGINES = {
    'relax': {
        'code': 'fleur-0.30-fleur_MPI@localhost',
        'inputgen': 'fleur-0.30-inpgen@localhost',
        'options': {
            'resources': {
                'num_machines': 1,
                'num_mpiprocs_per_machine': 1
            },
            'max_walltime': 86400,
        }
    }
}


def launch():
    """Launch the relax work chain for a basic silicon crystal structure at a range of scaling factors."""
    relaxation_type = RelaxType.ATOMS
    protocol = 'moderate'

    structure = structure_init()

    for scale in [0.94, 0.96, 0.98, 1, 1.02, 1.04, 1.06]:
        scaled = rescale(structure, scale)
        generator = RelaxWorkChain.get_inputs_generator()
        builder = generator.get_builder(scaled, CALC_ENGINES, protocol, relaxation_type, threshold_forces=0.001)
        results = run(builder)
        print(results['relaxed_structure'].get_cell_volume(), results['total_energy'].value)


if __name__ == '__main__':
    launch()
