#! /usr/bin/env python
from eboss_qso.fits import RSDFitRunner, parametrize
from eboss_qso import EBOSS_SPECTRA
import os
from argparse import Action

class BoxNumber(Action):
    def __call__(self, parser, namespace, box, option_string=None):
        add_commands(box=box)
        setattr(namespace, self.dest, box)

ITERATIONS = 500
ZBINS = [(0.8, 2.2)]
fixed_params = ['b1', 'sigma_fog', 'f', 'sigma8_z']
all_params = fixed_params + ['alpha_par', 'alpha_perp']

@parametrize({'sample':['N', 'S'], 'params': [all_params, fixed_params]})
def add_commands(box, sample, params):
    VERSION = 'v1.8e-no'
    HASHES = ['bba5aabfa6'] # no z-weights
    params = " ".join(params)

    dirname = os.path.join(EBOSS_SPECTRA, 'mocks', 'ezmock', VERSION)
    for i, hashstr in enumerate(HASHES):
        filename = os.path.join(dirname, f'poles_zevoEZmock_{VERSION}_QSO-{sample}_{box:04d}-{hashstr}.json')
        command = f"eboss-qso-fit nlopt -f {filename} --vary {params}  --stats P0 P2 -i {ITERATIONS}"

        tag = {'sample':sample, 'params':params, 'zbin':ZBINS[i]}
        RSDFitRunner.register(command, tag=tag)


if __name__ == '__main__':

    # the box number
    RSDFitRunner.update_preparser('--box', required=True, type=int, action=BoxNumber)
    RSDFitRunner.execute()