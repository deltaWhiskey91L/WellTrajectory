import numpy as np


def survey(md, inc, azi):
    """
    Calculates the survey for the entire well using the Average Angle Method.

    :param md: measured depth, MD (ft)
    :type md: list
    :param inc: inclination, Inc (dega)
    :type inc: list
    :param azi: azimuth, Azi (dega)
    :type azi: list
    :return: east, north, tvd, dls at survey points along the well.
    """

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
    avg_inc = np.average(np.array(inc2))
    avg_azi = np.arctan2(np.sin(azi2[0]) + np.sin(azi2[1]), np.cos(azi2[0]) + np.cos(azi2[1]))
    if avg_azi < 0:
        avg_azi = 2 * np.pi + avg_azi

    dv = dm * np.cos(avg_inc)
    dn = dm * np.sin(avg_inc) * np.cos(avg_azi)
    de = dm * np.sin(avg_inc) * np.sin(avg_azi)

    return dv, dn, de
