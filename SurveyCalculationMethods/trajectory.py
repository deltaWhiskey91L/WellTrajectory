from Utilities import mylogging, readfromfile as read, writetofile as write
from SurveyCalculationMethods import Generic
import math
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def average_angle(survey_object, target=None):
    """
    Survey calculations using the Average Angle Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    """
    from SurveyCalculationMethods import AverageAngle

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(survey_object.name))
    Calculation = Generic.SurveyMethod(survey_object, target)
    Calculation.name = survey_object.name
    Calculation.method = 'AverageAngletest'

    Calculation.TVD, Calculation.North, Calculation.East \
        = AverageAngle.survey(Calculation.MD, np.radians(Calculation.Inc), np.radians(Calculation.Azi))

    if Calculation.Target is None:
        Calculation.Target = closure_azimuth(Calculation.North[-1], Calculation.East[-1])

    if survey_object.location is not None:
        Calculation.North = np.add(Calculation.North, survey_object.location[0])
        Calculation.East = np.add(Calculation.East, survey_object.location[1])

    Calculation.Closure = closure_azimuth(Calculation.North, Calculation.East)
    Calculation.Departure = closure_departure(Calculation.North, Calculation.East)
    Calculation.Section = vertical_section(Calculation.North, Calculation.East, Calculation.Target)
    Calculation.DLS = np.zeros(len(Calculation.MD)) * np.nan
    Calculation.Build = np.zeros(len(Calculation.MD)) * np.nan
    Calculation.Turn = np.zeros(len(Calculation.MD)) * np.nan
    write.object_csv(Calculation)


def tangential(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Tangential Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import Tangential

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east = Tangential.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    dls = list()
    [dls.append(np.nan) for element in tvd]
    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]
    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name, method='Tangential')


def balanced_tangential(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Balanced Tangential Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import BalancedTangential

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east = BalancedTangential.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    dls = list()
    [dls.append(np.nan) for element in tvd]
    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]
    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name, method='BalancedTangential')


def vector_average(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Vector Average Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import VectorAverage

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east = VectorAverage.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    dls = list()
    [dls.append(np.nan) for element in tvd]
    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]
    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name, method='VectorAverage')


def radii_of_curvature(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Radii of Curvature Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import RadiiOfCurvature

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east, dls = RadiiOfCurvature.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]

    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name, method='RadiiOfCurvature')


def minimum_curvature(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Minimum Curvature Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import MinimumCurvature

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east, dls = MinimumCurvature.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]

    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name,
                     method='MinimumCurvature')


def minimum_curvature2(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Minimum Curvature Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import MinimumCurvature2

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east, dls = MinimumCurvature2.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]

    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name,
                     method='MinimumCurvature2')


def advanced_splines(name, target_azimuth=None, wellhead_location=None, file_path=None):
    """
    Survey calculations using the Minimum Curvature Method and writes results to .csv file.

    :param name: survey file name
    :type name: str
    :param file_path: survey file root path
    :type file_path: str
    :param target_azimuth: target azimuth (dega), if None, then last survey location
    :type target_azimuth: float
    :param wellhead_location: wellhead local [north, east] position
    :type wellhead_location: list
    """
    from SurveyCalculationMethods import AdvancedSplineCurve

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(name))
    if file_path is None:
        file_path = root_path + '/Data/'
    file = file_path + name + '.csv'

    md, inc, azi = read.survey(file)
    tvd, north, east, dls = AdvancedSplineCurve.survey(md, inc, azi)

    if target_azimuth is None:
        target_azimuth = closure_azimuth(north[-1], east[-1])

    if wellhead_location is not None:
        north = [north[i] + wellhead_location[0] for i in range(len(north))]
        east = [east[i] + wellhead_location[1] for i in range(len(east))]

    closure = [closure_azimuth(north[i], east[i]) for i in range(len(north))]
    departure = [closure_departure(north[i], east[i]) for i in range(len(north))]
    section = [vertical_section(north[i], east[i], target_azimuth) for i in range(len(north))]

    write.survey_csv([md, inc, azi, tvd, north, east, closure, departure, section, dls], name=name,
                     method='AdvancedSplines')


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
    closure = closure_azimuth(north, east)
    section = np.zeros(len(north))
    for i in range(len(north)):
        section[i] = departure[i] * np.cos(np.radians(target_azimuth - closure[i]))
    return section


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
    departure = np.zeros(len(north))
    for i in range(len(north)):
        departure[i] = np.sqrt(north[i] ** 2 + east[i] ** 2)
    return departure


def closure_azimuth(north, east):
    """
    Closure azimuth. north and east must be the same unit

    :param north: northing cartesian location, n (L)
    :type north: np.array
    :param east: easting cartesian location, e (L)
    :type east: np.array
    :return: closure azimuth (dega)
    :rtype: np.array
    """

    closure = np.zeros(len(north))
    for i in range(len(north)):
        closure[i] = np.degrees(np.arctan2(north[i], east[i]))
        if (closure[i] <= 180) and (closure[i] > 90):
            closure[i] = 450 - closure[i]
        elif (closure[i] <= 90) and (closure[i] >= 0):
            closure[i] = 90 - closure[i]
        else:
            closure[i] = 90 + math.fabs(closure[i])
    return closure


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
