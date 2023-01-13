import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotting_styles as ps


def read_output(path):
    df = pd.read_csv(path, skiprows=[0], header=None, sep='\s+',
                     names=['rho', 'Freq [kHz]', 'm', 'n'])
    return df.sort_values(by=['n', 'm', 'rho'])


def plot_nm(df, n, m, *args, ax=None,  **kwargs):
    b = df[(df['n'] == n) & (df['m'] == m)]
    label = f"n={n}, m={m}"
    if ax is None:
        plt.plot(b['rho'], b['Freq [kHz]'], *args, label=label, **kwargs)
    else:
        ax.plot(b['rho'], b['Freq [kHz]'], *args, label=label, **kwargs)


def plot_all(df, *args, ax=None, **kwargs):
    if ax is None:
        plt.plot('rho', 'Freq [kHz]', data=df, *args, label=None, **kwargs)
    else:
        ax.plot(df['rho'], df['Freq [kHz]'], *args, label=None, **kwargs)


if __name__ == '__main__':
    path = "/home/pedro/Documents/stellgap_pruebas/test/testzero/alfven_post"
    data = read_output(path)

    with ps.rc_context(ps.pub_style_one):

        fig, ax = plt.subplots(1, 1)

        plot_all(data, '.k', ms=1, ax=ax)
        plot_nm(data, n=2, m=6, ls='', marker='.', color='r', ms=2, ax=ax)
        plot_nm(data, n=3, m=5, ls='', marker='.', color='b', ms=2, ax=ax)
        # plt.plot('rho', 'Freq [kHz]', 'or', data=data)
        ax.legend()
        ax.set(xlabel=r'$\rho$', ylabel='Freq [kHz]')
    plt.show()

    fig.savefig('tmp.pdf')
