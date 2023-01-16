import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotting_styles as ps
from itertools import product


def read_output(path):
    df = pd.read_csv(path, skiprows=[0], header=None, sep='\s+')
    if len(df.columns) == 4:   # xstgap
        df.columns = ['rho', 'freq', 'm', 'n']
    elif len(df.columns) == 6:  # xstgap_snd
        df.columns = ['rho', 'freq', 'm', 'n', 'unk1', 'unk2']
    return df.sort_values(by=['n', 'm', 'rho'])


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


if __name__ == '__main__':
    path = "/home/pedro/Documents/stellgap_pruebas/test/testone/alfven_post"
    data = read_output(path)

    plot = True

    if plot:
        with ps.rc_context(ps.pub_style_one):
            fig, ax = plt.subplots(1, 1)
            plot_all(data, marker='.', ls='', color='k',
                     ms=1, ax=ax, quantity='freq')
            plot_nm(data, n=2, m=6, ls='', marker='.',
                    color='r', ms=2, ax=ax, quantity='freq')
            plot_nm(data, n=2, m=5, ls='', marker='.',
                    color='b', ms=2, ax=ax, quantity='freq')
            # plt.plot('rho', 'Freq [kHz]', 'or', data=data)
            ax.legend()
            ax.set(xlabel=r'$\rho$', ylabel='Freq [kHz]')
        plt.show()
        fig.savefig('tmp.pdf')

    print(pd.unique(data['m']))
