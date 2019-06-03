from Utilities import mylogging
import numpy as np
from numpy import linalg as la

# Advanced Spline Curve 3D Wellbore Trajectory Model
# Abughaban, M., Eustes, A., et al. 2016. Advanced Trajectory Computational Model Improves Borehole Positioning,
# Tortuosity and Rugosity. IADC/SPE Drilling Conference and Exhibition. Fort Worth, TX, USA. 1-3 March


def survey(md, inc, azi, err_model=(0, 0, 0)):
    """Calculates well survey using Advanced Spline Curve Method

    :param md: Array of Measured Depth (m)
    :type md: np.array
    :param inc: Array of Inclination (dega)
    :type inc: np.array
    :param azi: Array of Azimuth (dega)
    :type azi: np.array
    :param err_model: 2-sigma uncertainty in measurement (MD, Inc, Azi)
    :type err_model: tuple
    :return [easting (m), northing (m), tvd (m), dls (dega/m), build (dega/m), turn (dega/m), rugosity]
    :rtype: [float, float, float, float, float, float, float]
    """
    mylogging.runlog.info('Calculating the survey using Advanced Spline Curvature.')
    mylogging.alglog.info('ASC Advanced Spline Curve')

    # md = np.delete(md, 0)
    # inc = np.delete(inc, 0)
    # azi = np.delete(azi, 0)

    n = len(md)
    h = md[1:] - md[:-1]

    lam, v, z, y_2nd, err = list(), list(), list(), list(), list()
    for coord in range(0, 3):
        lam.append(lambda_vector(inc, azi, coord))
        v.append(v_vector(lam[coord], h))
        z.append(z_vector(h, v[coord]))
        y_2nd.append(Y_second(lam[coord], h, z[coord]))
        err0, err1, err2 = error_model(lam[coord], h, z[coord], inc, azi, coord)
        err.append(err_model[0] * err0 + err_model[1] * err1 + err_model[2] * err2)

    position = trajectory(h, lam, z, n, md)
    position[0] = np.delete(position[0], 0)
    position[1] = np.delete(position[1], 0)
    position[2] = np.delete(position[2], 0)

    errV, errN, errE = [0], [0], [0]
    for i in range(len(err[0])):
        errN.append(errN[i] + np.abs(err[0][i]))
        errE.append(errE[i] + np.abs(err[1][i]))
        errV.append(errV[i] + np.abs(err[2][i]))

    k = curvature(lam, h, z, y_2nd)
    curve = curve_rate(y_2nd, k=k)
    wbr = rugosity(lam, y_2nd, z, k=k)
    return position[2], position[1], position[0], np.degrees(curve[0]) * 100, \
           np.degrees(curve[1]) * 100, np.degrees(curve[2]) * 100, np.degrees(wbr) * 100, \
           errN, errE, errV


def trajectory(h, lam, z, n, md):
    position = [np.zeros(n + 1), np.zeros(n + 1), np.zeros(n + 1)]
    for coord in range(0, 3):
        B, C, D = B_vector(lam[coord], h, z[coord]), C_vector(z[coord]), D_vector(z[coord], h)
        for i in range(1, n + 1):
            delta = 0.
            if coord == 2:
                delta += md[0]
            for j in range(0, i - 1):
                delta += delta_position(lam[coord][j], B[j], C[j], D[j], h[j])
            position[coord][i] = delta
    return position


def lambda_derivative(inc, azi):
    """
    Well vector derivative for a given inc / azi
    :param inc: inclination (rad)
    :type inc: float
    :param azi: azimuth (rad)
    :type azi: float
    :return: lambda derivative matrix
    """

    dldp = np.zeros((3, 3))
    dldp[1][0] = np.cos(inc) * np.sin(azi)
    dldp[1][1] = np.cos(inc) * np.cos(azi)
    dldp[1][2] = - np.sin(inc)
    dldp[2][0] = np.sin(inc) * np.cos(azi)
    dldp[2][1] = - np.sin(inc) * np.cos(azi)
    return dldp


def lambda_vector(inc, azi, xyz_dimension):
    """
    :param inc: Inclination (rad)
    :type inc: np.array
    :param azi: Azimuth (rad)
    :type azi: np.array
    :param xyz_dimension:
    :type xyz_dimension: int
    :return:
    """

    lam = list()
    for i in range(0, len(azi)):
        if xyz_dimension == 0:
            lam.append(np.sin(inc[i]) * np.sin(azi[i]))
        elif xyz_dimension == 1:
            lam.append(np.sin(inc[i]) * np.cos(azi[i]))
        else:
            lam.append(np.cos(inc[i]))
    return lam


def v_vector(lam, h):
    n = len(lam) - 2
    v = np.zeros(n)
    for i in range(1, n + 1):
        v[i - 1] = 6 * ((lam[i + 1] - lam[i])/h[i] - (lam[i] - lam[i - 1])/h[i - 1])
    return v


def z_matrix_inv(h):
    """
    Sets up the Z-matrix inverse

    :param h: delta MD, h
    :type h: np.array
    :return: inverse Z-matrix, Z**(-1)
    :rtype: np.array
    """

    n = len(h) - 1
    Z = np.zeros((n, n), dtype=float)

    # First Line in A-matrix
    Z[0][0] = 2 * (h[0] + h[1]) + h[0] + h[0]**2 / h[1]
    Z[0][1] = h[1] - h[0]**2 / h[1]

    # Setup diagonal matrix
    for i in range(1, n - 1):
        Z[i][i - 1] = h[i - 1]
        Z[i][i] = 2 * (h[i - 1] + h[i])
        Z[i][i + 1] = h[i]

    # Last Line in A-matrix
    Z[-1][-2] = h[-2] - h[-1]**2 / h[-2]
    Z[-1][-1] = 2 * (h[-2] + h[-1]) + h[-1] + h[-1]**2 / h[-2]

    return la.inv(Z)


def z_vector_alt(invZ, h, v):
    """
    z-vector with inverse Z-matrix input
    :param invZ: Z-matrix inverse, Z**(-1)
    :type invZ: np.array
    :param h: delta MD, h
    :type h: np.array
    :param v: v-vector
    :type v: np.array
    :return: z-vector, z
    :rtype: np.array
    """
    z_slv = np.dot(invZ, v)
    z = list()
    z.append(z_0(z_slv, h))
    for i in range(0, len(z_slv)):
        z.append(z_slv[i])
    z.append(z_n(z_slv, h))
    np.array(z)
    return z


def z_vector(h, v):
    """Diagonal Matrix Linear Algebra Solution"""
    n = len(v)
    Z = np.zeros((n, n), dtype=float)

    # First Line in A-matrix
    Z[0][0] = 2 * (h[0] + h[1]) + h[0] + h[0]**2 / h[1]
    Z[0][1] = h[1] - h[0]**2 / h[1]

    # Setup diagonal matrix
    for i in range(1, n - 1):
        Z[i][i - 1] = h[i - 1]
        Z[i][i] = 2 * (h[i - 1] + h[i])
        Z[i][i + 1] = h[i]

    # Last Line in A-matrix
    Z[-1][-2] = h[-2] - h[-1]**2 / h[-2]
    Z[-1][-1] = 2 * (h[-2] + h[-1]) + h[-1] + h[-1]**2 / h[-2]

    z_slv = np.linalg.solve(Z, v)

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
    for i in range(0, len(z) - 1):
        C[i] = z[i] / 2
    return C


def D_vector(z, h):
    D = np.zeros(len(z) - 1)
    for i in range(0, len(z) - 1):
        D[i] = (z[i + 1] - z[i]) / (6 * h[i])
    return D


def z_0(z, h):
    return z[0] + (z[0] - z[1]) * h[0] / h[1]


def z_n(z, h):
    return z[-1] + (z[-1] - z[-2]) * h[-1] / h[-2]


def error_model(lam, h, z, inc, azi, coord):
    drdD = np.zeros(len(lam) - 1)
    drdI = np.zeros(len(lam) - 1)
    drdA = np.zeros(len(lam) - 1)

    if coord == 0:
        coord = 1
    if coord == 1:
        coord = 0

    for i in range(len(lam) - 1):
        dldp = lambda_derivative(inc[i], azi[i])
        drdD[i] = lam[i] + 0.5 * (lam[i + 1] - lam[i]) \
                  - h[i] ** 2 / 2 * (0.5 * z[i + 1] + z[i]) \
                  + h[i] ** 2 / 2 * z[i] \
                  + h[i] ** 2 / 8 * (z[i + 1] - z[i])
        drdI[i] = 3 / 2 * h[i] * dldp[1][coord]
        drdA[i] = 2 * h[i] * dldp[2][coord] + h[i] / 2

    return drdD, drdI, drdA


def delta_position(A, B, C, D, h):
    return h * A + h**2 / 2 * B + h**3 / 3 * C + h**4 / 4 * D


def Y_second(lam, h, z):
    n = len(lam)
    Y_dbl = list()

    for i in range(0, n - 1):
        Y_dbl.append((lam[i + 1] - lam[i]) / h[i] - h[i] * z[i + 1] / 6 - h[i] * z[i] / 3)

    Y_dbl.append((lam[-1] - lam[-2]) / h[-1] + h[-1] * z[-2] / 6 + h[-1] * z[-1] / 3)
    return Y_dbl


def curvature(lam, h, z, y_2nd=None):
    if y_2nd is None:
        y_2nd = list()
        for coord in range(0, 3):
            y_2nd.append(Y_second(lam, h, z[coord]))
    k = list()
    for i in range(0, len(y_2nd[0])):
        k.append(la.norm(np.array([y_2nd[0][i], y_2nd[1][i], y_2nd[2][i]]), ord=2))
    return k


def curve_rate(y_2nd, k=None, lam=None, h=None, z=None):
    if k is None:
        k = curvature(lam, h, z)

    dls, build, turn = list([0]), list([0]), list([0])
    for i in range(0, len(y_2nd[0])):
        dls.append(k[i])
        build.append(y_2nd[2][i])
        turn.append(la.norm([y_2nd[0][i], y_2nd[1][i]], ord=2))
    return dls, build, turn


def rugosity(lam, y_2nd, z, h=None, k=None):
    if k is None:
        k = curvature(lam, h, z)
    wbr = list([0])
    for i in range(0, len(y_2nd[0])):
        det_matrix = list()
        for coord in range(0, 3):
            det_matrix.append([lam[coord][i], y_2nd[coord][i], z[coord][i]])
        np.array(det_matrix)
        wbr.append(np.degrees(la.det(det_matrix) / k[i]**2) * 100)
    return wbr
