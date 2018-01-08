import datetime
import logging
import os
import sys

import ReadFromFile
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

config = ReadFromFile.Config()

survey = Survey.DirectionalSurvey(survey_file)
Survey.calculate_survey(survey, config)
WriteToFile.write_survey(survey, config)

if config.method is 'ASC':
    WellPlot.plot_wbr([survey])
WellPlot.plot_dls([survey])
WellPlot.plot_horizontal_section([survey])
WellPlot.plot_vertical_section([survey])

t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
logging.info('{0} END: Target Destroyed.'.format(t))
print('Target Destroyed')
