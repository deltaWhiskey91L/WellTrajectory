from Utilities import mylogging
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def complete_survey(survey, rnd=False):
    """
    Writes complete survey to file
    :param survey: SurveyMethod object
    :param rnd: round to nearest 100th
    :type rnd: bool
    """

    mylogging.runlog.info('Write: Writing the survey to .csv.')
    file = root_path + '/Results/{0}_{1}.csv'.format(survey.name, survey.method)

    header = ['MD,Inc,Azi,TVD,North,East,Closure,Departure,Section,DLS,Build,Turn,Target\n',
              'ft,dega,dega,ft,ft,ft,dega,ft,ft,dega/100ft,dega/100ft,dega/100ft,dega\n']

    if rnd is True:
        md, inc, azi = np.round(survey.md, 2), np.round(survey.inc, 2), np.round(survey.azi, 2)
        tvd, ns, ew = np.round(survey.tvd, 2), np.round(survey.north, 2), np.round(survey.east, 2)
        closure, departure = np.round(survey.closure, 2), np.round(survey.departure, 2)
        section = np.round(survey.section, 2)
        dls, build, turn = np.round(survey.dls, 2), np.round(survey.build, 2), np.round(survey.turn, 2)
    else:
        md, inc, azi, tvd, ns, ew = survey.md, survey.inc, survey.azi, survey.tvd, survey.north, survey.east
        closure, departure, section = survey.closure, survey.departure, survey.section
        dls, build, turn = survey.dls, survey.build, survey.turn

    f = open(file, 'w')
    f.writelines(header)
    for i in range(len(survey.md)):
        line = [str(md[i]) + ',' + str(inc[i]) + ',' + str(azi[i]) + ',' + str(tvd[i]) + ','
                + str(ns[i]) + ',' + str(ew[i]) + ',' + str(closure[i]) + ','
                + str(departure[i]) + ',' + str(section[i]) + ',' + str(dls[i]) + ','
                + str(build[i]) + ',' + str(turn[i]) + ',' + str(survey.target) + '\n']
        f.writelines(line)
    f.close()


def survey_measurements(md, inc, azi, file):
    """
    Writes the survey measurements to csv
    :param md: measured depth
    :type md: list
    :param inc: inclination
    :type inc: list
    :param azi: azimuth
    :type azi: list
    :param file: file path
    :type file: str
    """
    mylogging.runlog.info('Write: Writing the survey to .csv.')

    header = ['MD,Inc,Azi\n', 'ft,dega,dega\n']

    f = open(file, 'w')
    f.writelines(header)
    for i in range(len(md)):
        f.writelines([str(md[i]) + ',' + str(inc[i]) + ',' + str(azi[i]) + '\n'])
    f.close()
