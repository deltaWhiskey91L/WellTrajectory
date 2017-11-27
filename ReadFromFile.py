import configparser
import datetime
import logging
import os
import sys

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + 'Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

cfg = configparser.ConfigParser(allow_no_value=True)


class Config:
    """Config class object contains all of the configuration options for the Well Trajectory application."""
    def __init__(self, file=root_path + '/Input Files/config.ini'):
        try:
            cfg.read(file)
        except configparser.Error:
            self.method = 'MCM'
            self.units_out = 'PetroImperial'
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.info('CONFIG: {0} Missing Config.ini and subsequent configuration options. Using default options.'
                         .format(t))

        self.method = get_calculation_method(cfg)


def read_file(file):
    t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    logging.info('{0} INFO: Read survey from {1}.'.format(t, file))

    survey_file = list()
    f = open(file, 'r', encoding='utf-8-sig')
    for line in f:
        survey_file.append(line.strip().split(','))
    f.close()

    return survey_file


def get_option(config, section, option):
    if config.has_option(section, option):
        option_value = config.get(section, option)
    else:
        option_value = None
        timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        logging.debug('CONFIG: {0} {1} is missing {2} value.'.format(timestamp, section, option))
    return option_value


def get_calculation_method(config, section='ConfigOptions', option='calculation_method'):
    calc_method = get_option(config, section, option)

    if is_in_asc_list(calc_method, config=config, section=section) is True:
        return 'ASC'
    else:
        return 'MCM'


def is_in_asc_list(calc_method, config, section='PossibleOptionsList', option='advanced_spline_method'):
    try:
        config.get(section, option).split(',').index(calc_method)
    except configparser.Error:
        t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        logging.info('CONFIG: {0} Config.ini missing possible spellings for '
                     'Advanced Spline Curvature method.'.format(t))
        try:
            ['ASC', 'asc', 'Advanced Spline Curvature'].index(calc_method)
        except ValueError:
            return False
        else:
            return True
    except ValueError:
        try:
            ['ASC', 'asc', 'Advanced Spline Curvature'].index(calc_method)
        except ValueError:
            return False
        else:
            return True
    else:
        return True


def is_in_units_list(unit, config, section='PossibleOptionsList', option='unit_list'):
    try:
        config.get(section, option).split(',').index(unit)
    except configparser.Error:
        t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        logging.info('CONFIG: {0} Config.ini missing possible spellings for output units option.'.format(t))
        try:
            ['PetroImperial, Metric'].index(unit)
        except ValueError:
            return 'oilfield'
        else:
            return unit






