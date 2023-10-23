#!/bin/python3

import subprocess
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import netcdf_file
from scipy.optimize import curve_fit


def polynomial(x, *args):
    return sum([args[i] * x**i for i in range(len(args))])


def poly_fit(x, y, n_max):
    p0 = np.zeros(n_max)
    popt, *_ = curve_fit(polynomial, x, y, p0=p0)
    return popt


def write_coefs(coefs, path_out):
    coefs_str = " ".join([f"{i:.8f}" for i in coefs]) + "\n"
    with open(path_out, "w") as outfile:
        outfile.write(coefs_str)


def fit_profile(path_in="tmp.dat", path_out=None, normalize=False, **kwargs):
    if path_out is None:
        path_out = f"{path_in}_fit"
    s, prof = np.loadtxt(path_in, **kwargs)
    print(path_in, path_out, f"{prof[0]:.7f}")
    if normalize is True:
        prof = prof / prof[0]
    coefs = poly_fit(s, prof, 10)
    write_coefs(coefs=coefs, path_out=path_out)
    # np.savetxt(path_out, coefs)


if __name__ == "__main__":
    x = np.linspace(0, 1, 100)
    y = 3 * x - x**2 + 0.25 * x**3 - 0.012 * x**4 + 3.15

    args = poly_fit(x, y, 10)

    plot = True
    if plot:
        fig, ax = plt.subplots(1, 1)
        ax.plot(x, y, "k")
        ax.plot(x, polynomial(x, *args), "r:")

        plt.show()
