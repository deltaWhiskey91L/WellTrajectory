import datetime
import logging
import math as m
import numpy as np
import os

import AdvancedSplineCurve as asc
import MinimumCurvature as mcm
import ReadFromFile as read
import UnitConverter as Units

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
logging.info('{0} START: Starting survey analysis.'.format(t))


class DirectionalSurvey:
    """Survey object contains all of the data from the survey file."""
    def __init__(self, file=root_path + '/Input Files/Surveys/survey.csv'):
        survey_file = list()

        try:
            survey_file = read.read_file(file)
        except:
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.critical('{0} CONFIG: Error loading the survey file ({1}).'.format(t, file))

        self.operator_name = get_item(survey_file, 'Operator Name:', 'str')
        self.operator_number = get_item(survey_file, 'Operator Number:', 'int')
        self.well_name = get_item(survey_file, 'Well Name:', 'str')
        self.well_number = get_item(survey_file, 'Well Number:', 'int')
        self.api_number = get_item(survey_file, 'API Number:', 'str')
        self.location = get_dbl_item(survey_file, 'Location:', 'str')
        self.site_northing = get_item(survey_file, 'Site Northing:')
        self.site_easting = get_item(survey_file, 'Site Easting:')
        self.tie_point = get_item(survey_file, 'Tie Point:')
        self.well_northing = get_item(survey_file, 'Wellhead Northing:')
        self.well_easting = get_item(survey_file, 'Wellhead Easting:')
        self.rkb = get_item(survey_file, 'RKB:')
        self.altitude = get_item(survey_file, 'Ground Level:')
        self.target_azi = get_item(survey_file, 'Target Azimuth:')
        self.citing_type = get_item(survey_file, 'Citing Type:', 'str')
        self.deviation_indicator = get_item(survey_file, 'Deviation Indicator:', 'str')
        self.north_reference = get_item(survey_file, 'North Reference:', 'str')
        self.grid_type = get_item(survey_file, 'Grid Type:', 'str')
        self.units = get_item(survey_file, 'Units:', 'str')
        self.azi_accuracy = get_item(survey_file, 'Azimuth Accuracy:', if_none=1.0)     # Accuracy at 1 std
        self.azi_resolution = get_item(survey_file, 'Azimuth Resolution:', if_none=0.18)
        self.inc_accuracy = get_item(survey_file, 'Inclination Accuracy:', if_none=0.1)     # Accuracy at 1 std
        self.inc_resolution = get_item(survey_file, 'Inclination Resolution:', if_none=0.025)
        self.optional = get_item(survey_file, 'Optional:', 'str')

        try:
            self.points = survey_pts(survey_file)
        except:
            self.points = [None, None, None]
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.critical('{0} SURVEY: Survey missing survey points.'.format(t))

        self.md = [self.points[i][0] for i in range(0, len(self.points))]
        self.inc = [self.points[i][1] for i in range(0, len(self.points))]
        self.azi = [self.points[i][2] for i in range(0, len(self.points))]
        self.tvd = list()
        self.north = list()
        self.east = list()
        self.departure = list()
        self.departure_azi = list()
        self.vertical_section = list()
        self.dls = list()
        self.build = list()
        self.turn = list()
        self.wbr = list()
        self.north_err = list()
        self.east_err = list()
        self.tvd_err = list()
        self.field_north = list([self.well_northing])
        self.field_east = list([self.well_easting])
        self.field_alt = list([self.altitude])


def calculate_survey(survey, config):
    t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    logging.info('{0} INFO: Calculating the detailed survey.'.format(t))

    if config.method is 'ASC':
        survey.east, survey.north, survey.tvd, survey.dls, survey.turn, survey.build, survey.wbr = \
            asc.survey(survey.md, survey.inc, survey.azi)
    else:
        survey.tvd.append(0)
        survey.north.append(0)
        survey.east.append(0)
        survey.dls.append(0)
        survey.build.append(0)
        survey.turn.append(0)
        for i in range(1, len(survey.md)):
            delta_md = survey.md[i] - survey.md[i - 1]
            delta_tvd, delta_north, delta_east, dls \
                = mcm.next_pt(delta_md, [survey.inc[i - 1], survey.inc[i]], [survey.azi[i - 1], survey.azi[i]])

            survey.tvd.append(add(survey.tvd[i - 1], delta_tvd))
            survey.north.append(add(survey.north[i - 1], delta_north))
            survey.east.append(add(survey.east[i - 1], delta_east))
            survey.dls.append(dls)
            survey.build.append(mcm.buildturn_rate(survey.inc[i - 1], survey.inc[i], delta_md))
            survey.turn.append(mcm.buildturn_rate(survey.azi[i - 1], survey.azi[i], delta_md))

    if survey.target_azi is None:
        survey.target_azi = calculate_azimuth(survey.north[len(survey.north) - 1], survey.east[len(survey.east) - 1],
                                              survey.well_northing, survey.well_easting)

    for i in range(0, len(survey.md)):
        survey.departure.append(departure(survey.north[i], survey.east[i]))
        survey.departure_azi.append(calculate_azimuth(survey.north[i], survey.east[i], survey.well_northing,
                                                      survey.well_easting))
        survey.vertical_section.append(
            survey.departure[i] * np.cos(Units.to_si(survey.target_azi - survey.departure_azi[i], 'dega')))

    # for i in range(1, len(survey.md)):
    #     survey.field_north.append(add(survey.field_north[0], survey.north[i]))
    #     survey.field_east.append(add(survey.field_east[0], survey.east[i]))
    #     survey.field_alt.append(add(survey.field_alt[0], - survey.tvd[i]))


def index_2d(my_list, item):
    for i, line in enumerate(my_list):
        if item in line:
            return i
    raise IndexError


def get_dbl_item(survey_file, item_name, if_none=(None, None)):
    try:
        item = survey_file[index_2d(survey_file, item_name)][1:]
    except ValueError:
        item = if_none
        return item
    except IndexError:
        item = if_none
        return item
    else:
        if item is '':
            item = if_none
            return item
    return item


def get_item(survey_file, item_name, var_type='float', if_none=None):
    try:
        item = survey_file[index_2d(survey_file, item_name)][1]
    except ValueError:
        item = if_none
        return item
    except IndexError:
        item = if_none
        return item
    else:
        if item is '':
            item = if_none
            return item

    if var_type is 'float':
        item = float(item)
    elif var_type is 'int':
        item = int(item)

    return item


def survey_pts(survey_file):
    survey = list()
    for i in range(index_2d(survey_file, 'MD') + 1, len(survey_file)):
        line = list()
        for j in range(0, 3):
            try:
                line.append(float(survey_file[i][j]))
            except ValueError:
                line.append(survey_file[i][j])
        survey.append(line)
    return survey


def departure(north, east):
    total_departure = np.sqrt(north ** 2 + east ** 2)

    return total_departure


def calculate_azimuth(target_north, target_east, sighting_north=0, sighting_east=0):
    north = target_north - sighting_north
    east = target_east - sighting_east
    arc = Units.from_si(m.atan2(north, east), 'dega')
    if 90 < arc <= 180:
        azimuth = 450 - arc
    elif 0 <= arc <= 90:
        azimuth = 90 - arc
    else:
        azimuth = 90 + m.fabs(arc)

    return azimuth


def add(item0, item1):
    return item0 + item1
