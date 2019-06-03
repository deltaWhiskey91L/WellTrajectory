import numpy as np


def survey(md, inc, azi, error=(0, 0, 0)):
    """
    Calculates the survey for the entire well using the Vector Average Method.

    :param md: measured depth, MD (ft)
    :type md: list
    :param inc: inclination, Inc (rad)
    :type inc: list
    :param azi: azimuth, Azi (rad)
    :type azi: list
    :return: east, north, tvd, dls at survey points along the well.
    """

    tvd, north, east, dls, turn, build = list([0]), list([0]), list([0]), list([0]), list([0]), list([0])
    errV, errN, errE = [0], [0], [0]
    for i in range(1, len(md)):
        if i == len(md) - 1:
            dmd = [md[i - 1], md[i], md[i]]
            dinc = [inc[i - 1], inc[i], inc[i]]
            dazi = [azi[i - 1], azi[i], azi[i]]
        else:
            dmd = [md[i - 1], md[i], md[i + 1]]
            dinc = [inc[i - 1], inc[i], inc[i + 1]]
            dazi = [azi[i - 1], azi[i], azi[i + 1]]
        dv, dn, de, dls_current, turn_current, build_current, eV, eN, eE \
            = next_pt(dmd, dinc, dazi, error=error)
        tvd.append(tvd[i - 1] + dv)
        north.append(north[i - 1] + dn)
        east.append(east[i - 1] + de)
        dls.append(dls_current)
        turn.append(turn_current)
        build.append(build_current)
        errV.append(errV[i - 1] + np.abs(eV))
        errN.append(errN[i - 1] + np.abs(eN))
        errE.append(errE[i - 1] + np.abs(eE))

    return tvd, north, east, dls, turn, build, errV, errN, errE


def next_pt(md2, inc2, azi2, error=(0, 0, 0)):
    """
    Calculates the change in position between the two points.

    :param md2: measured depth of the two points, md (ft)
    :type md2: list
    :param inc2: inclination of the two points, inc (rad)
    :type inc2: list
    :param azi2: azimuth of the two points, azi (rad)
    :type azi2: list
    :return: change in position [dv, dn, de, dls]
    :rtype: list
    """

    dm = md2[1] - md2[0]
    dP = np.zeros(3)
    if inc2[0] == inc2[1] and azi2[0] == azi2[1]:
        dP[0] = dm * np.cos(inc2[0])
        dP[1] = dm * np.sin(inc2[0]) * np.cos(azi2[0])
        dP[2] = dm * np.sin(inc2[0]) * np.sin(azi2[0])
        dls, build, turn = 0, 0, 0
    else:
        wA = unit_vector(inc2[0], azi2[0])
        wB = unit_vector(inc2[1], azi2[1])
        alpha = np.arccos(np.dot(wA, wB)) / 2
        r = dm / (2 * alpha)
        dc = 2 * r * np.sin(alpha)
        dP = dc * (wA + wB) / np.linalg.norm(wA + wB)
        dls = np.degrees(100 / r)
        build = buildturn_rate(inc2[0], inc2[1], dm)
        turn = buildturn_rate(azi2[0], azi2[1], dm)

    drdD, drdI, drdA = error_model(md2, inc2, azi2)
    errV, errN, errE = error_calc(drdD, drdI, drdA, error)

    return dP[0], dP[1], dP[2], dls, build, turn, -errV, -errN, -errE


def unit_vector(inc, azi):
    """
    Unit vector for a given inclination and azimuth

    :param inc: inclination, inc (rad)
    :type inc: float
    :param azi: azimuth, azi (rad)
    :type inc: float
    :return: unit vector, w_hat
    :rtype: np.array
    """

    return np.array([np.cos(inc), np.sin(inc) * np.cos(azi), np.sin(inc) * np.sin(azi)])


def buildturn_rate(angle0, angle1, delta_md):
    delta_angle = angle1 - angle0
    if delta_md == 0:
        return 0

    return np.degrees(delta_angle) * 100 / delta_md


def error_calc(drdD, drdI, drdA, error_measure):
    errN = error_measure[0] * drdD[0] + error_measure[1] * drdI[0] + error_measure[2] * drdA[0]
    errE = error_measure[0] * drdD[1] + error_measure[1] * drdI[1] + error_measure[2] * drdA[1]
    errV = error_measure[0] * drdD[2] + error_measure[1] * drdI[2] + error_measure[2] * drdA[2]
    return errV, errN, errE


def error_model(md, inc, azi):
    drdD = np.zeros(3)
    drdI = np.zeros(3)
    drdA = np.zeros(3)

    drdD[0] = 0.5 * (np.sin(inc[0]) * np.cos(azi[0]) + np.sin(inc[1]) * np.cos(azi[1])) \
              - 0.5 * (np.sin(inc[1]) * np.cos(azi[1]) + np.sin(inc[2]) * np.cos(azi[2]))
    drdD[1] = 0.5 * (np.sin(inc[0]) * np.sin(azi[0]) + np.sin(inc[1]) * np.sin(azi[1])) \
              - 0.5 * (np.sin(inc[1]) * np.sin(azi[1]) + np.sin(inc[2]) * np.sin(azi[2]))
    drdD[2] = 0.5 * (np.cos(inc[0]) + np.cos(inc[1])) \
              - 0.5 * (np.cos(inc[1]) + np.cos(inc[2]))

    drdI[0] = 0.5 * (md[1] - md[0]) * (np.cos(inc[1]) * np.cos(azi[1])) \
              + 0.5 * (md[2] - md[1]) * (np.cos(inc[1]) * np.cos(azi[1]))
    drdI[1] = 0.5 * (md[1] - md[0]) * (np.cos(inc[1]) * np.sin(azi[1])) \
              + 0.5 * (md[2] - md[1]) * (np.cos(inc[1]) * np.sin(azi[1]))
    drdI[2] = - 0.5 * (md[1] - md[0]) * (np.sin(inc[1])) \
              - 0.5 * (md[2] - md[1]) * (np.sin(inc[1]))

    drdA[0] = - 0.5 * (md[1] - md[0]) * (np.sin(inc[1]) * np.sin(azi[1])) \
              - 0.5 * (md[2] - md[1]) * (np.sin(inc[1]) * np.sin(azi[1]))
    drdA[1] = 0.5 * (md[1] - md[0]) * (np.sin(inc[1]) * np.cos(azi[1])) \
              + 0.5 * (md[2] - md[1]) * (np.sin(inc[1]) * np.cos(azi[1]))
    return drdD, drdI, drdA
