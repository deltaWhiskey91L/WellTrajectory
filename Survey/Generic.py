import math
import numpy as np


def closure_azimuth(north, east):
    """
    Calculates closure azimuth.
    north and east must be the same unit

    :param north: northing cartesian location, n (L)
    :type north: float
    :param east: easting cartesian location, e (L)
    :type east: float
    :return: closure azimuth (dega)
    :rtype: float
    """

    closure = np.degrees(math.atan2(north, east))
    if (closure <= 180) and (closure > 90):
        return 450 - closure
    if (closure <= 90) and (closure >= 0):
        return 90 - closure
    return 90 + math.fabs(closure)


def closure_departure(north, east):
    """
    Calculates the absolute horizontal departure from wellhead.
    north and east must be the same unit

    :param north: northing cartesian location, n (L)
    :type north: float
    :param east: easting cartesian location, e (L)
    :type east: float
    :return: closure departure (L)
    :type: float
    """

    return np.sqrt(north ** 2 + east ** 2)


def vertical_section(north, east, target_azimuth):
    """
    Calculates the horizontal departure from the wellhead along the target azimuth.
    north and east must be the same unit

    :param north: northing cartesian location, n (L)
    :type north: float
    :param east: easting cartesian location, e (L)
    :type east: float
    :param target_azimuth: target azimuth (dega)
    :type target_azimuth: float
    :return section: Vertical Section
    :return section: float
    """

    departure = closure_departure(north, east)
    return departure * np.cos(np.radians(target_azimuth - closure_azimuth(north, east)))
