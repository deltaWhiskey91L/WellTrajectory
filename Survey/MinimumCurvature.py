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

    tvd, north, east, dls, build, turn = list([0]), list([0]), list([0]), list([0]), list([0]), list([0])
    rugosity = list(np.zeros(len(md)) * np.nan)

    for i in range(1, len(md)):
        next_point = next_pt(md[i] - md[i - 1], [inc[i - 1], inc[i]], [azi[i - 1], azi[i]])
        build.append(buildturn_rate(inc[i - 1], inc[i], md[i] - md[i - 1]))
        turn.append(buildturn_rate(azi[i - 1], azi[i], md[i] - md[i - 1]))
        tvd.append(tvd[i - 1] + next_point[0])
        north.append(north[i - 1] + next_point[1])
        east.append(east[i - 1] + next_point[2])
        dls.append(next_point[3])

    return east, north, tvd, dls, build, turn, rugosity


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

    return tvd, north, east, dls


def buildturn_rate(angle0, angle1, delta_md):
    delta_angle = angle1 - angle0
    if delta_md == 0:
        return 0

    return np.degrees(delta_angle) * 100 / delta_md
