import numpy as np


def survey(md, inc, azi):
    """
    Calculates the survey for the entire well using the Vector Average Method.

    :param md: measured depth, MD (ft)
    :type md: list
    :param inc: inclination, Inc (dega)
    :type inc: list
    :param azi: azimuth, Azi (dega)
    :type azi: list
    :return: east, north, tvd, dls at survey points along the well.
    """

    inc = [np.radians(ele) for ele in inc]
    azi = [np.radians(ele) for ele in azi]

    tvd, north, east, dls = list([0]), list([0]), list([0]), list([0])
    for i in range(1, len(md)):
        dv, dn, de, dls_current = next_pt([md[i - 1], md[i]], [inc[i - 1], inc[i]], [azi[i - 1], azi[i]])
        tvd.append(tvd[i - 1] + dv)
        north.append(north[i - 1] + dn)
        east.append(east[i - 1] + de)
        dls.append(dls_current)

    return tvd, north, east, dls


def next_pt(md2, inc2, azi2):
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
        dls = 0
    else:
        wA = unit_vector(inc2[0], azi2[0])
        wB = unit_vector(inc2[1], azi2[1])
        alpha = np.arccos(np.dot(wA, wB)) / 2
        r = dm / (2 * alpha)
        dc = 2 * r * np.sin(alpha)
        dP = dc * (wA + wB) / np.linalg.norm(wA + wB)
        dls = np.degrees(100 / r)

    return dP[0], dP[1], dP[2], dls


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
