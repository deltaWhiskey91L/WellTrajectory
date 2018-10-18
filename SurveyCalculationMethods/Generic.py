from Utilities import mylogging, unitconverter as units
import csv
import math
import numpy as np
import os


class Survey:
    def __init__(self, file_name, path=None, location=(0, 0)):
        """
        :param file_name: survey file name
        :type file_name: str
        :param path: survey file root path
        :type path: str
        :param location: wellhead local [north, east] position
        :type location: list
        """
        if path is None:
            path = os.path.dirname(os.path.dirname(__file__)) + '/Data/'

        self.name = file_name
        self.file = path + self.name + '.csv'
        self.location = location

        from Utilities import readfromfile as read
        md, inc, azi = read.survey(self.file)

        self.MD = np.array(md)
        self.Inc = np.array(inc)
        self.Azi = np.array(azi)


class SurveyMethod:
    def __init__(self, survey, target=None):
        self.method = None
        self.name = survey.name
        if target < 0:
            target = target + 360
        self.Target = target
        self.MD = survey.MD
        self.Inc = survey.Inc
        self.Azi = survey.Azi
        self.TVD = None
        self.North = None
        self.East = None
        self.Closure = None
        self.Departure = None
        self.Section = None
        self.DLS = None
        self.Build = None
        self.Turn = None
        self.Rugosity = None


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
    Absolute horizontal departure from wellhead.
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
    Horizontal departure from the wellhead along the target azimuth.
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
