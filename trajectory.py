import logging
import math
import numpy as np
import os

from Survey import AdvancedSplineCurve as ASC, MinimumCurvature as MCM
from Utilities import unitconverter as units, mylogging

root_path = os.path.dirname(os.path.realpath(__file__))


def calculate_survey(md, inc, azi, target_azi=None, adj=None, method='ASC'):
    """
    Calculates the survey from the survey measurements.

    :param md: Measured Depth
    :type md: list([float])
    :param inc: Inclination (dega)
    :type inc: list([float])
    :param azi: azimuth (dega)
    :type azi: list([float])
    :param adj: wellhead position adjustment
    :type adj: list
    :param target_azi: Target Azimuth (dega)
    :type target_azi: float
    :param method: Calculation method. 'ASC' (Advanced Spline Curve)
    :type method: str
    :return: md, inc, azi, tvd, northing, easting, vertical section, dls, build, turn, rugosity, target azi
    :return: [list([float]), list([float]), list([float]), list([float]), list([float]), list([float]), list([float]),
              list([float]), list([float]), list([float]), list([float]), float]
    """

    md = np.array(md)
    inc = np.radians(np.array(inc))
    azi = np.radians(np.array(azi))

    if method is 'ASC':
        mylogging.alglog.info('Survey: Calculating the survey using Advanced Spline Curve.')
        east, north, tvd, dls, build, turn, rugosity = ASC.survey(md, inc, azi)
    else:
        mylogging.alglog.info('Survey: Calculating the survey using Minimum Curvature Method.')
        east, north, tvd, dls, build, turn, rugosity = MCM.survey(md, inc, azi)

    if target_azi is None:
        target_azi = closure_azimuth(north[-1], east[-1])

    v_section = vertical_section(north, east, target_azi)

    if adj is None:
        return md, inc, azi, tvd, north, east, v_section, dls, build, turn, rugosity, target_azi
    else:
        v_adj = vertical_section(adj[1], adj[0], target_azi)
        return md, inc, azi, tvd, np.add(north, adj[1][0]), np.add(east, adj[0][0]), np.add(v_section, v_adj[0]), dls, build, turn, rugosity, target_azi


def vertical_section(northing, easting, target_azimuth):
    """
    Calculates the horizontal departure from the wellhead along the target azimuth.
    :param northing: Northing
    :type northing: list([float])
    :param easting: Easting
    :type easting: list([float])
    :param target_azimuth: Target Azimuth (dega)
    :type target_azimuth: float
    :return section: Vertical Section
    :return section: list([float])
    """
    departure_dist = departure(northing, easting)
    section = list()
    for i in range(0, len(northing)):
        section.append(departure_dist[i] * np.cos(np.radians(target_azimuth - closure_azimuth(northing[i], easting[i]))))

    return section


def departure(northing, easting):
    """
    Calculates the absolute horizontal departure from wellhead.

    :param northing:
    :param easting:
    :return: total_departure
    :type: list([float])
    """

    total_departure = list()
    for i in range(0, len(northing)):
        total_departure.append(np.sqrt(northing[i] ** 2 + easting[i] ** 2))

    return total_departure


def closure_azimuth(northing, easting):
    """
    Calculates the closure azimuth.

    :param northing: Northing
    :type northing: float
    :param easting: Easting
    :type easting: float
    :return closure: Closure Azimuth (dega)
    :return closure: float
    """

    closure = np.degrees(math.atan2(northing, easting))
    if (closure <= 180) and (closure > 90):
        return 450 - closure
    if (closure <= 90) and (closure >= 0):
        return 90 - closure
    return 90 + math.fabs(closure)


def error(md0, md1, tvd0, tvd1, north0, north1, east0, east1):
    """
    Calculates the error between HRCG and 100ft surveys

    :return: Cumulative relative error
    """

    err = 0
    for i in range(0, len(md1)):
        for j in range(0, len(md0)):
            if md0[j] == md1[i]:
                err += np.sqrt((tvd0[j] - tvd1[i])**2 + (north0[j] - north1[i])**2 + (east0[j] - east1[i])**2)

    return err / len(md1)
