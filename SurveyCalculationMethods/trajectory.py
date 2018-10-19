from Utilities import mylogging, readfromfile as read, writetofile as write
from SurveyCalculationMethods import Generic
import math
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def average_angle(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Average Angle Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import AverageAngle

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Average Angle method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'AverageAngle'

    surv.tvd, surv.north, surv.east \
        = AverageAngle.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.dls = np.zeros(len(surv.md)) * np.nan
    surv.build = np.zeros(len(surv.md)) * np.nan
    surv.turn = np.zeros(len(surv.md)) * np.nan
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def tangential(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Tangential Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import Tangential

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Tangential method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'Tangential'

    surv.tvd, surv.north, surv.east \
        = Tangential.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.dls = np.zeros(len(surv.md)) * np.nan
    surv.build = np.zeros(len(surv.md)) * np.nan
    surv.turn = np.zeros(len(surv.md)) * np.nan
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def balanced_tangential(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Balanced Tangential Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import BalancedTangential

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Balanced Tangential method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'BalancedTangential'

    surv.tvd, surv.north, surv.east \
        = BalancedTangential.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.dls = np.zeros(len(surv.md)) * np.nan
    surv.build = np.zeros(len(surv.md)) * np.nan
    surv.turn = np.zeros(len(surv.md)) * np.nan
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def vector_average(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Vector Average Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import VectorAverage

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Vector Average method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'VectorAverage'

    surv.tvd, surv.north, surv.east \
        = VectorAverage.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.dls = np.zeros(len(surv.md)) * np.nan
    surv.build = np.zeros(len(surv.md)) * np.nan
    surv.turn = np.zeros(len(surv.md)) * np.nan
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def radii_of_curvature(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Radius of Curvature Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import RadiiOfCurvature

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Radius of Curvature method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'RadiusOfCurvature'

    surv.tvd, surv.north, surv.east, surv.dls, surv.build, surv.turn \
        = RadiiOfCurvature.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def minimum_curvature(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Minimum Curvature Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import MinimumCurvature

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Minimum Curvature method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'MinimumCurvature'

    surv.tvd, surv.north, surv.east, surv.dls,  surv.build,  surv.turn \
        = MinimumCurvature.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.rugosity = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


def advanced_splines(survey_object, target=None, rnd=False):
    """
    Survey calculations using the Advanced Spline Curve Method and writes results to .csv file.

    :param survey_object: survey class object
    :param target: target azimuth
    :type target: float
    :param rnd: round to nearest 100th
    :type rnd: bool
    """
    from SurveyCalculationMethods import AdvancedSplineCurve

    mylogging.runlog.info('Survey: Calculate survey for {0} using the Advanced Spline Curve method.'.format(survey_object.name))
    surv = Generic.SurveyMethod(survey_object, target)
    surv.name = survey_object.name
    surv.method = 'AdvancedSplineCurve'

    surv.tvd, surv.north, surv.east, surv.dls, surv.build, surv.turn, surv.rugosity \
        = AdvancedSplineCurve.survey(surv.md, np.radians(surv.inc), np.radians(surv.azi))

    if surv.target is None:
        surv.target = closure_azimuth(surv.north[-1], surv.east[-1])

    if survey_object.location is not None:
        surv.north = np.add(surv.north, survey_object.location[0])
        surv.east = np.add(surv.east, survey_object.location[1])

    surv.closure = closure_azimuth(surv.north, surv.east)
    surv.departure = closure_departure(surv.north, surv.east)
    surv.section = vertical_section(surv.north, surv.east, surv.target)
    surv.build = np.zeros(len(surv.md)) * np.nan
    surv.turn = np.zeros(len(surv.md)) * np.nan
    write.object_csv(surv, rnd=rnd)
    return surv


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
