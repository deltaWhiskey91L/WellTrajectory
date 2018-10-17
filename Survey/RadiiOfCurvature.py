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

    md = np.array(md)
    inc = np.radians(np.array(inc))
    azi = np.radians(np.array(azi))

    tvd, north, east, dls = list([0]), list([0]), list([0]), list([0])
    for i in range(1, len(md)):
        dv, dn, de, dls_current = next_pt([md[i - 1], md[i]], [inc[i - 1], inc[i]], [azi[i - 1], azi[i]])
        tvd.append(tvd[i - 1] + dv)
        north.append(north[i - 1] + dn)
        east.append(east[i - 1] + de)
        dls.append(dls_current)

    return tvd, north, east


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
    r_vert = dm / (inc2[1] - inc2[0])
    dv = r_vert * (np.sin(inc2[1]) - np.sin(inc2[0]))
    dh = r_vert * (np.cos(inc2[0]) - np.cos(inc2[1]))
    r_hor = dh / (azi2[1] - azi2[0])
    dn = r_hor * (np.sin(azi2[1]) - np.sin(azi2[0]))
    de = r_hor * (np.cos(azi2[0]) - np.cos(azi2[1]))
    dls = np.sqrt((1 / r_vert) ** 2 + (1 / r_hor) ** 2)

    return dv, dn, de, dls
