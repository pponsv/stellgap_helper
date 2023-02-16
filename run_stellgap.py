#!/bin/python3

import subprocess
import os
import argparse
import sys
from scipy.io import netcdf_file


def parse_args():
    parser = argparse.ArgumentParser(
        prog='run_stellgap', description='Parse arguments')
    parser.add_argument('--dir',
                        metavar='Directory',
                        help='Path to the directory. Can be relative or absolute',
                        default='./',
                        type=str)
    parser.add_argument('--ext',
                        metavar='Extension',
                        help='Extension name of the VMEC file')
    parser.add_argument('--sound',
                        help='Run STELLGAP with sound coupling. If not present, defaults to xstgap.',
                        action='store_true')
    parser.add_argument('--rw',
                        help='Run STELLGAP rewrite. If not present, defaults to xstgap.',
                        action='store_true')
    parser.add_argument('--vmec',
                        help='Run VMEC on input.ext',
                        action='store_true')
    parser.add_argument('--booz',
                        help='Run BOOZ_XFORM',
                        action='store_true')
    parser.add_argument('--xst',
                        help='Run STELLGAP',
                        action='store_true')
    parser.add_argument('--xmetric',
                        help='Run XMETRIC',
                        action='store_true')
    parser.add_argument('--fine',
                        metavar='ir_fine',
                        help='Number of surfaces for fine structure',
                        default=300,
                        type=int)
    return parser.parse_args()


def get_surfaces_file(wout_vmec):
    with netcdf_file(wout_vmec, 'r') as wfile:
        nsurf = wfile.variables['ns'].data.copy()
    return nsurf


def make_xform_input(folderpath, ext, woutname, s=None):
    in_file = f'{folderpath}/in_booz.{ext}'
    with netcdf_file(woutname, 'r') as wout:
        ntor = wout.variables['ntor'].data.copy()
        mpol = wout.variables['mpol'].data.copy()
        ns = wout.variables['ns'].data.copy()
    if s is None:
        s = list(range(1, ns))
    with open(in_file, 'w') as f:
        f.write(f'{mpol} {ntor}\n')
        f.write(f'{ext}\n')
        [f.write(f'{i} ') for i in s]
    return in_file


def call_xform(dirpath, in_file):
    cwd = os.getcwd()
    os.chdir(dirpath)
    result = subprocess.call(['xbooz_xform', os.path.basename(in_file)])
    os.chdir(cwd)
    return result


def call_xvmec(dirname, extname):
    cwd = os.getcwd()
    os.chdir(dirname)
    result = subprocess.call(['xvmec2000', extname])
    os.chdir(cwd)
    return result


def call_xmetric(dirname, boozmn_file):
    cwd = os.getcwd()
    os.chdir(dirname)
    result = subprocess.call(['xmetric', os.path.basename(boozmn_file)])
    os.chdir(cwd)
    return result


def call_xstgap(dirname, irads, ir_fine_scl, sound=False, logname='log.tmp', rw=False):
    if sound==True:
        executable = 'xstgap_snd'
    elif rw==True:
        executable = 'xstgap_new'
    else:
        executable= 'xstgap'
    cwd = os.getcwd()
    os.chdir(dirname)
    result = subprocess.call(
        [executable, str(irads), str(ir_fine_scl), f'> {logname}'])
    os.chdir(cwd)
    return result


def run_all(dirname, extname, num_fine=300, VMEC=False, BOOZ=False, XMETRIC=False, XSTGAP=False, SOUND=False, RW=False):
    dirname = os.path.abspath(inargs.dir)
    extname = inargs.ext

    wout_vmec = f'{dirname}/wout_{extname}.nc'
    wout_boozmn = f'{dirname}/boozmn_{extname}.nc'

    if VMEC:
        print('\nRun VMEC\n')
        result_vmec = call_xvmec(dirname, extname)

    nsurf = get_surfaces_file(wout_vmec)

    if BOOZ:
        print('\nMake booz_xform input\n')
        in_file_booz = make_xform_input(dirname, extname, wout_vmec)
        print('\nCall booz_xform\n')
        result_xform = call_xform(dirname, in_file_booz)

    if XMETRIC:
        print('\nCall xmetric\n')
        result_xmetric = call_xmetric(dirname, wout_boozmn)

    if XSTGAP:
        print('\nCall xstgap\n')
        result_xstgap = call_xstgap(dirname,
                                    irads=(nsurf-2),
                                    ir_fine_scl=num_fine,
                                    sound=SOUND, 
                                    rw=RW)


if __name__ == "__main__":
    """
    Runs stellgap on a VMEC output (wout_vmec file). In order:

    - Reads the VMEC equilibrium, finds the number of surfaces
    - Makes booz_xform input file, for surfaces 2:(ns-1) (both included)
        Output:
            - in_booz.{ext}
    - Runs booz_xform
        Output:
            - boozmn_{ext}.nc
    - Runs xmetric on the boozmn output.
        Output: 
            - tae_data_boozer
    - Runs xstgap
        Input:
            - fourier.dat 
                (fourier modes to represent the continuum eigenmodes)
            - plasma.dat
                (info and profiles for the plasma)
        Output:
            - ??
    """

    inargs = parse_args()
    print(inargs)

    dirname = os.path.abspath(inargs.dir)
    extname = inargs.ext

    run_all(dirname, extname,
            num_fine=inargs.fine,
            VMEC=inargs.vmec,
            BOOZ=inargs.booz,
            XMETRIC=inargs.xmetric,
            XSTGAP=inargs.xst,
            SOUND=inargs.sound,
            RW=inargs.rw)