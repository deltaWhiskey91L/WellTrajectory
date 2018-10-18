import numpy as np


def survey(md, inc, azi):
    """
    Calculates the survey for the entire well using the Tangential Method.

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

    tvd, north, east = list([0]), list([0]), list([0])
    for i in range(1, len(md)):
        dv, dn, de = next_pt([md[i - 1], md[i]], [inc[i - 1], inc[i]], [azi[i - 1], azi[i]])
        tvd.append(tvd[i - 1] + dv)
        north.append(north[i - 1] + dn)
        east.append(east[i - 1] + de)

    return tvd, north, east


def next_pt(md2, inc2, azi2):
    """
    Calculates the change in position between the two points.

    :param md2: measured depth of the two points, md (ft)
    :type md2: list
    :param inc2: inclination of the two points, md (rad)
    :type inc2: list
    :param azi2: azimuth of the two points, azi (rad)
    :type azi2: list
    :return: change in position [dv, dn, de]
    :rtype: list
    """

    dm = md2[1] - md2[0]
    dv = dm * np.cos(inc2[0])
    dn = dm * np.sin(inc2[0]) * np.cos(azi2[0])
    de = dm * np.sin(inc2[0]) * np.sin(azi2[0])

    return dv, dn, de
