import datetime
import logging
import os

import math as m
import numpy as np
import UnitConverter as Units

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

# Advanced Spline Curve 3D Wellbore Trajectory Model
# Abughaban, M., Eustes, A., et al. 2016. Advanced Trajectory Computational Model Improves Borehole Positioning,
# Tortuosity and Rugosity. IADC/SPE Drilling Conference and Exhibition. Fort Worth, TX, USA. 1-3 March


def survey(md, inc, azi):
    n = len(md)
    s = np.array(md)
    inc = np.array(inc)
    azi = np.array(azi)
    h = s[1:] - s[:-1]
    u = 2 * (h[1:] + h[:-1])

    lam, v, z, y_2nd = list(), list(), list(), list()
    for coord in range(0, 3):
        lam.append(lambda_vector(inc, azi, coord))
        v.append(v_vector(lam[coord], h))
        z.append(z_vector(u, h, v[coord]))
        y_2nd.append(Y_second(lam[coord], h, z[coord]))

    position = trajectory(h, lam, z, n)
    k = curvature(lam, h, z, y_2nd)
    curve = curve_rate(y_2nd, k=k)
    wbr = rugosity(lam, y_2nd, z, k=k)

    return position[0], position[1], position[2], curve[0], curve[1], curve[2], wbr


def trajectory(h, lam, z, n):
    position = [np.zeros(n), np.zeros(n), np.zeros(n)]
    for coord in range(0, 3):
        B, C, D = B_vector(lam[coord], h, z[coord]), C_vector(z[coord]), D_vector(z[coord], h)
        for i in range(1, n):
            delta = 0.
            for j in range(0, i):
                delta += delta_position(lam[coord][j], B[j], C[j], D[j], h[j])
            position[coord][i] = delta
    return position


def curve_rate(y_2nd, k=None, lam=None, h=None, z=None):
    if k is None:
        k = curvature(lam, h, z)

    dls, build, turn = list(), list(), list()
    for i in range(0, len(y_2nd[0])):
        dls.append(k[i] * 180 / np.pi * 100)
        build.append(y_2nd[0][i] * 180 / np.pi)
        turn.append(np.linalg.norm([y_2nd[0][i], y_2nd[1][i]]))
    return dls, build, turn


def rugosity(lam, y_2nd, z, h=None, k=None):
    if k is None:
        k = curvature(lam, h, z)
    wbr = list()
    for i in range(0, len(y_2nd[0])):
        det_matrix = list()
        for coord in range(0, 3):
            det_matrix.append([lam[coord][i], y_2nd[coord][i], z[coord][i]])
        np.array(det_matrix)
        wbr.append(np.linalg.det(det_matrix) / k[i]**2)
    return wbr


def curvature(lam, h, z, y_2nd=None):
    if y_2nd is None:
        y_2nd = list()
        for coord in range(0, 3):
            y_2nd.append(Y_second(lam, h, z[coord]))
    k = list()
    for i in range(0, len(y_2nd[0])):
        k.append(Units.from_si(np.linalg.norm([y_2nd[0][i], y_2nd[1][i], y_2nd[2][i]]), 'dega'))
    return k


def lambda_vector(inc, azi, xyz_dimension):
    lam = list()
    inc = inc * np.pi / 180
    azi = azi * np.pi / 180
    for i in range(0, len(azi)):
        if xyz_dimension == 0:
            lam.append(m.sin(inc[i]) * m.sin(azi[i]))
        elif xyz_dimension == 1:
            lam.append(m.sin(inc[i] * m.cos(azi[i])))
        else:
            lam.append(m.cos(inc[i]))
    return lam


def v_vector(lam, h):
    n = len(lam)
    v = np.zeros(n - 2)
    for i in range(1, n - 1):
        v[i - 1] = 6 * ((lam[i + 1] - lam[i])/h[i] - (lam[i] - lam[i - 1])/h[i - 1])
    return v


def z_vector(u, h, v):
    """Diagonal Matrix Linear Algebra Solution"""
    lin_A = np.zeros((len(u), len(u)), dtype=float)
    n = len(u)
    # First Line in A-matrix
    lin_A[0][0] = u[1] + h[0] + h[0]**2 / h[1]
    lin_A[0][1] = h[1] - h[0]**2 / h[1]

    # Setup diagonal matrix
    for i in range(1, n - 1):
        lin_A[i][i - 1] = h[i - 1]
        lin_A[i][i] = u[i]
        lin_A[i][i + 1] = h[i]

    # Last Line in A-matrix
    lin_A[n - 1][n - 2] = h[n - 2] - h[n - 1]**2 / h[n - 2]
    lin_A[n - 1][n - 1] = u[n - 1] + h[n - 1] + h[n - 1]**2 / h[n - 2]

    try:
        z_slv = np.linalg.solve(lin_A, v)
    except:
        z_slv = None

    z = list()
    z.append(z_0(z_slv, h))
    for i in range(0, len(z_slv)):
        z.append(z_slv[i])
    z.append(z_n(z_slv, h))
    np.array(z)
    return z


def B_vector(lam, h, z):
    B = np.zeros(len(z) - 1)
    for i in range(0, len(z) - 1):
        B[i] = (lam[i + 1] - lam[i]) / h[i] - h[i] * z[i + 1] / 6 - h[i] * z[i] / 3
    return B


def C_vector(z):
    C = np.zeros(len(z) - 1)
    for i in range(0, len(z) - 1 - 1):
        C[i] = z[i] / 2
    return C


def D_vector(z, h):
    D = np.zeros(len(z) - 1)
    for i in range(0, len(z) - 1):
        D[i] = (z[i + 1] - z[i]) / (6 * h[i])
    return D


def z_0(z, h):
    return z[0] - (z[1] - z[0]) * h[0] / h[1]


def z_n(z, h):
    n = len(z)
    return z[n - 2] + (z[n - 2] - z[n - 3]) * h[n - 1] / h[n - 2]


def delta_position(A, B, C, D, h):
    return h * A + h**2 / 2 * B + h**3 / 3 * C + h**4 / 4 * D


def Y_second(lam, h, z):
    n = len(lam)
    Y_dbl = list()

    for i in range(0, n - 1):
        Y_dbl.append((lam[i + 1] - lam[i]) / h[i] - h[i] * z[i + 1] / 6 - h[i] * z[i] / 3)

    Y_dbl.append((lam[n - 1] - lam[n - 2]) / h[n - 2] + h[n - 2] * z[n - 2] / 6 + h[n - 2] * z[n - 1] / 3)
    return Y_dbl
