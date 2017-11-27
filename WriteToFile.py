import datetime
from datetime import date
import logging
import os
import Survey as s

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + 'Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())


def write_survey(survey, method):
    calendar = [[1, 'JAN'], [2, 'FEB'], [3, 'MAR'], [4, 'APR'], [5, 'MAY'], [6, 'JUN'], [7, 'JUL'], [8, 'AUG'],
                [9, 'SEP'], [10, 'OCT'], [11, 'NOV'], [12, 'DEC']]

    today = date.today()
    year = today.year
    month = calendar[s.index_2d(calendar, today.month)][1]
    day = today.day

    t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    logging.info('{0} INFO: Writing the calculated survey to .txt file.'.format(t))

    file = root_path + 'Results/' + str(survey.operator_name) + str(survey.well_name) + '_DIR_' + method + '_' + \
           str(year) + month + str(day) + '_' + str(survey.optional) + '.txt'

    units = 'ft, deg, deg, ft, ft, ft, ft, ft, ft, deg, deg, deg, \n'
    if survey.units is 'Metric':
        units = 'm, deg, deg, m, m, m, m, m, m, deg, deg, deg, \n'

    survey_header = ['Measured Depth (MD), Inclination, Azimuth, True Vertical Depth (TVD), TVD 2-sigma, +N/-S, '
                     '+N/-S 2-sigma, +E/-W, +E/-W 2-sigma, Vertical Section, Dogleg Severity, Build Rate, Turn Rate, '
                     'Rugosity \n', units]

    f = open(file, 'w')
    f.writelines(survey_header)

    for i in range(0, len(survey.md)):
        line = [str(survey.md[i]) + ', ' + str(survey.inc[i]) + ', ' + ', ' + str(survey.azi[i]) + ', ' +
                str(survey.tvd[i]) + ', , ' + str(survey.north[i]) + ', , ' + str(survey.east[i]) + ', , ' + '\n']
                # str(survey.vertical_section[i]) + ', ' + str(survey.dls[i]) + ', ' + str(survey.build[i]) + ', ' +
                # str(survey.turn[i]) + ', ' + str(survey.wgr[i])\n']
        f.writelines(line)
    f.close()
