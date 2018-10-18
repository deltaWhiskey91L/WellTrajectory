from Utilities import mylogging
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def object_csv(survey, rnd=False):
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
        md, inc, azi = np.round(survey.MD, 2), np.round(survey.Inc, 2), np.round(survey.Azi, 2)
        tvd, ns, ew = np.round(survey.TVD, 2), np.round(survey.North, 2), np.round(survey.East, 2)
        closure, departure = np.round(survey.Closure, 2), np.round(survey.Departure, 2)
        section = np.round(survey.Section, 2)
        dls, build, turn = np.round(survey.DLS, 2), np.round(survey.Build, 2), np.round(survey.Turn, 2)
    else:
        md, inc, azi, tvd, ns, ew = survey.MD, survey.Inc, survey.Azi, survey.TVD, survey.North, survey.East
        closure, departure, section = survey.Closure, survey.Departure, survey.Section
        dls, build, turn = survey.DLS, survey.Build, survey.Turn

    f = open(file, 'w')
    f.writelines(header)
    for i in range(len(survey.MD)):
        line = [str(md[i]) + ',' + str(inc[i]) + ',' + str(azi[i]) + ',' + str(tvd[i]) + ','
                + str(ns[i]) + ',' + str(ew[i]) + ',' + str(closure[i]) + ','
                + str(departure[i]) + ',' + str(section[i]) + ',' + str(dls[i]) + ','
                + str(build[i]) + ',' + str(turn[i]) + ',' + str(survey.Target) +'\n']
        f.writelines(line)
    f.close()


def survey_csv(survey, name=None, method='mcm', iteration=None):
    if iteration is not None:
        mylogging.runlog.info('Write: Writing the {0} survey to .csv.'.format(iteration))
        file = root_path + '/Results/{0}_{1}{2}.csv'.format(name, method, iteration)
    else:
        mylogging.runlog.info('Write: Writing the survey to .csv.')
        file = root_path + '/Results/{0}_{1}.csv'.format(name, method)

    header = ['MD,Inc,Azi,TVD,NS,EW,Closure,Departure,Section,DLS\n',
              'ft,dega,dega,ft,ft,ft,dega,ft,ft,dega/100ft\n']

    f = open(file, 'w')
    f.writelines(header)
    survey = np.round(survey, 2)

    for i in range(0, len(survey[0])):
        line = [str(survey[0][i]) + ',' + str(survey[1][i]) + ',' + str(survey[2][i]) + ',' + str(survey[3][i]) + ','
                + str(survey[4][i]) + ',' + str(survey[5][i]) + ',' + str(survey[6][i]) + ','
                + str(survey[7][i]) + ',' + str(survey[8][i]) + ',' + str(survey[9][i]) + '\n']
        f.writelines(line)
    f.close()
