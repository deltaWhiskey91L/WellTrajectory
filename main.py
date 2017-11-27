import datetime
import logging
import os
import sys

import Survey
import WriteToFile
import WellPlot

root = os.path.dirname(Survey.__file__)
survey_file = root + '\Input Files\Surveys\survey.csv'

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

survey = Survey.DirectionalSurvey(survey_file)
survey.method = method
Survey.calculate_survey(survey, method)
WriteToFile.write_survey(survey, method)

if survey.method is 'ASC':
    WellPlot.plot_wbr([survey])
WellPlot.plot_dls([survey])
WellPlot.plot_horizontal_section([survey])
WellPlot.plot_vertical_section([survey])

# pt = len(survey.md) - 1
#
# #print('DLS: ' + str(survey.dls[pt]))
# print('TVD: ' + str(survey.tvd[pt]))
# print('North: ' + str(survey.north[pt]))
# print('East: ' + str(survey.east[pt]))
# # print('Departure: ' + str(survey.departure[pt]))
# print(('Target Azimuth: ' + str(survey.target_azi)))
# # print(('Target Vertical Section: ' + str(survey.vertical_section[pt])))
#

# print(('GL: ' + str(survey.field_alt[pt])))
# print(('FEL: ' + str(survey.field_east[pt])))
# print(('FSL: ' + str(survey.field_north[pt])))

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
logging.info('{0} END: Target Destroyed.'.format(t))
print('Target Destroyed')
