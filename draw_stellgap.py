import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotting_styles as ps
from itertools import product
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        prog='run_stellgap', description='Parse arguments')
    parser.add_argument('--dir',
                        metavar='Directory',
                        help='Path to the directory. Can be relative or absolute',
                        default='./',
                        type=str)
    return parser.parse_args()


def read_alfven_post(path):
    path = f"{path}/alfven_post"
    df = pd.read_csv(path, skiprows=[0], header=None, sep='\s+')
    if len(df.columns) == 4:   # xstgap
        df.columns = ['rho', 'freq', 'm', 'n']
    elif len(df.columns) == 6:  # xstgap_snd
        df.columns = ['rho', 'freq', 'm', 'n', 'unk1', 'unk2']
    else: 
        raise(ValueError('File not compliant'))
    return df.sort_values(by=['n', 'm', 'rho'])

def read_ion_profile(path):
    path = f"{path}/ion_profile"
    df = pd.read_csv(path, header=None, sep='\s+')
    print(df)
    if len(df.columns) == 4:   # xstgap
        df.columns = ['rho', 'ion_density', 'iota', 'va']
    else: 
        raise(ValueError('File not compliant'))
    return df.sort_values(by=['rho'])

def plot_nm(df, n, m, *args, ax=None, quantity='freq',  **kwargs):
    b = df[(df['n'] == n) & (df['m'] == m)]
    label = f"n={n}, m={m}"
    if ax is None:
        plt.plot(b['rho'], b[quantity], *args, label=label, **kwargs)
    else:
        ax.plot(b['rho'], b[quantity], *args, label=label, **kwargs)


def plot_all(df, *args, ax=None, quantity='freq', **kwargs):
    for n, m in list(product(pd.unique(df['n']), pd.unique(df['m']))):
        data = df[(df['n'] == n) & (df['m'] == m)]
        if ax is None:
            plt.plot('rho', quantity, data=data, *
                     args, label='_nolegend_', **kwargs)
        else:
            ax.plot('rho', quantity, data=data, *
                    args, label='_nolegend_', **kwargs)
    ax.legend()
    ax.get_legend().remove()

def plot_profiles(profiles, axes=None, *args, **kwargs):
    if axes is None:
        fig, axes = plt.subplots(3,1)
    axes[0].plot('rho', 'ion_density', *args, data=profiles, **kwargs)
    axes[1].plot('rho', 'iota', *args, data=profiles, **kwargs)
    axes[2].plot('rho', 'va',  *args, data=profiles, **kwargs)
    return axes

if __name__ == '__main__':

    inargs = parse_args()

    dirpath = os.path.abspath(inargs.dir)
    print(dirpath)
    # dirpath = "/home/pedro/Documents/stellgap_pruebas/test/testone"
    data = read_alfven_post(dirpath)
    profiles_new = read_ion_profile(dirpath)
    profiles_old = read_ion_profile(dirpath+'/../testzero')

    plot = True

    if plot:
        with ps.rc_context(ps.pub_style_one):
            fig, ax = plt.subplots(1, 1)
            plot_all(data, marker='.', ls='', color='#696969', alpha=0.6,
                     ms=1, ax=ax, quantity='freq')
            plot_nm(data, n=2, m=6, ls='', marker='.',
                    color='r', ms=2, ax=ax, quantity='freq')
            plot_nm(data, n=2, m=4, ls='', marker='.',
                    color='b', ms=2, ax=ax, quantity='freq')
            # plt.plot('rho', 'Freq [kHz]', 'or', data=data)
            ax.legend()
            ax.set(xlabel=r'$\rho$', ylabel='Freq [kHz]')
            nfig, nax = plt.subplots(3,1)
            plot_profiles(profiles_new, nax, 'k')
            plot_profiles(profiles_old, nax, color='#696969')

        plt.show()
        fig.savefig('tmp.pdf')

    print(pd.unique(data['m']))
