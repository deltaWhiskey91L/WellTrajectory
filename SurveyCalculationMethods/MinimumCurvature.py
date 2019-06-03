import numpy as np


def survey(md, inc, azi, error=(0, 0, 0)):
    """
    Calculates the survey for the entire well.

    :param md: Array of measured depth measurements
    :type md: np.array
    :param inc: Array of inclination measurements
    :type inc: np.array
    :param azi: Array of azimuth measurements
    :type azi: np.array
    :return: east, north, tvd, dls at survey points along the well.
    """

    tvd, north, east, dls, turn, build = list([0]), list([0]), list([0]), list([0]), list([0]), list([0])
    errV, errN, errE = [0], [0], [0]
    for i in range(1, len(md)):
        dm = md[i] - md[i - 1]
        dv, dn, de, dls_current, turn_current, build_current, eV, eN, eE \
            = next_pt(dm, [inc[i - 1], inc[i]], [azi[i - 1], azi[i]], measurement_error=error)
        tvd.append(tvd[i - 1] + dv)
        north.append(north[i - 1] + dn)
        east.append(east[i - 1] + de)
        dls.append(dls_current)
        turn.append(turn_current)
        build.append(build_current)
        errV.append(errV[i - 1] + eV)
        errN.append(errN[i - 1] + eN)
        errE.append(errE[i - 1] + eE)

    print('MCM errN', errN[-1])
    print('MCM errE', errE[-1])
    print('MCM errV', errV[-1])
    return tvd, north, east, dls, turn, build, errV, errN, errE


def next_pt(delta_md, inc, azi, measurement_error=(0, 0, 0), tolerance=1e-10):
    """
    Calculates the next survey point using Minimum Curvature Method

    :param delta_md: delta measured depth, MD
    :type delta_md: float
    :param inc: inclination (rad)
    :type inc: list
    :param azi: azimuth (rad)
    :type azi: list
    :param measurement_error: 2-sigma measurement error (MD, Inc, Azi) (ft, rad, rad)
    :type measurement_error: tuple
    :param tolerance: iteration tolerance
    :type tolerance: float
    :return:
    """

    beta = np.arccos(np.cos(inc[1] - inc[0]) - np.sin(inc[0]) * np.sin(inc[1]) * (1 - np.cos(azi[1] - azi[0])))
    if beta == 0:
        beta = tolerance

    ratio = 2.0 / beta * np.tan(beta / 2.0)
    north = delta_md * ratio / 2.0 * (np.sin(inc[0]) * np.cos(azi[0]) + np.sin(inc[1]) * np.cos(azi[1]))
    east = delta_md * ratio / 2.0 * (np.sin(inc[0]) * np.sin(azi[0]) + np.sin(inc[1]) * np.sin(azi[1]))
    tvd = delta_md * ratio / 2.0 * (np.cos(inc[0]) + np.cos(inc[1]))
    dls = np.degrees(beta) * 100.0 / delta_md
    build = np.degrees(buildturn_rate(inc[0], inc[1], delta_md)) * 100
    turn = np.degrees(buildturn_rate(azi[0], azi[1], delta_md)) * 100
    drdD, drdI, drdA = error_model(delta_md, inc, azi)
    errV, errN, errE = error(drdD, drdI, drdA, measurement_error)

    return tvd, north, east, dls, build, turn, errV, errN, errE


def buildturn_rate(angle0, angle1, delta_md):
    delta_angle = angle1 - angle0
    if delta_md == 0:
        return 0

    return delta_angle


def error(drdD, drdI, drdA, error_measure):
    errN = error_measure[0] * drdD[0] + error_measure[1] * drdI[0] + error_measure[2] * drdA[0]
    errE = error_measure[0] * drdD[1] + error_measure[1] * drdI[1] + error_measure[2] * drdA[1]
    errV = error_measure[0] * drdD[2] + error_measure[1] * drdI[2] + error_measure[2] * drdA[2]
    return errV, errN, errE


def error_model(delta_md, inc, azi):
    drdD = np.zeros(3)
    drdI = np.zeros(3)
    drdA = np.zeros(3)

    drdD[0] = 0.5 * (np.sin(inc[0]) * np.cos(azi[0]) + np.sin(inc[1]) * np.cos(azi[1]))
    drdD[1] = 0.5 * (np.sin(inc[0]) * np.sin(azi[0]) + np.sin(inc[1]) * np.sin(azi[1]))
    drdD[2] = 0.5 * (np.cos(inc[0]) + np.cos(inc[1]))

    drdI[0] = 0.5 * delta_md * (np.cos(inc[1]) * np.cos(azi[1]))
    drdI[1] = 0.5 * delta_md * (np.cos(inc[1]) * np.sin(azi[1]))
    drdI[2] = -0.5 * delta_md * (np.sin(inc[1]))

    drdA[0] = -0.5 * delta_md * (np.sin(inc[1]) * np.sin(azi[1]))
    drdA[1] = 0.5 * delta_md * (np.sin(inc[1]) * np.cos(azi[1]))
    return drdD, drdI, drdA
