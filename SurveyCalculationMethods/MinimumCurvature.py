import numpy as np


def survey(md, inc, azi):
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

    inc = [np.radians(ele) for ele in inc]
    azi = [np.radians(ele) for ele in azi]

    tvd, north, east, dls = list([0]), list([0]), list([0]), list([0])

    for i in range(1, len(md)):
        next_point = next_pt(md[i] - md[i - 1], [inc[i - 1], inc[i]], [azi[i - 1], azi[i]])
        tvd.append(tvd[i - 1] + next_point[0])
        north.append(north[i - 1] + next_point[1])
        east.append(east[i - 1] + next_point[2])
        dls.append(next_point[3])

    return tvd, north, east, dls


def next_pt(delta_md, inc, azi, tolerance=1e-10):
    """
    Calculates the next survey point using Minimum Curvature Method

    :param delta_md: delta measured depth, MD
    :type delta_md: float
    :param inc: inclination (rad)
    :type inc: list
    :param azi: azimuth (rad)
    :type azi: list
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
    build = buildturn_rate(inc[0], inc[1], delta_md)
    turn = buildturn_rate(azi[0], azi[1], delta_md)

    return tvd, north, east, dls, build, turn


def buildturn_rate(angle0, angle1, delta_md):
    delta_angle = angle1 - angle0
    if delta_md == 0:
        return 0

    return np.degrees(delta_angle) * 100 / delta_md
