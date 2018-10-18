from Utilities import mylogging
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def object_csv(survey):
    """
    Writes complete survey to file
    :param survey: SurveyMethod object
    """

    mylogging.runlog.info('Write: Writing the survey to .csv.')
    file = root_path + '/Results/{0}_{1}.csv'.format(survey.name, survey.method)

    header = ['MD,Inc,Azi,TVD,North,East,Closure,Departure,Section,DLS,Build,Turn,Target\n',
              'ft,dega,dega,ft,ft,ft,dega,ft,ft,dega/100ft,dega/100ft,dega/100ft,dega\n']

    f = open(file, 'w')
    f.writelines(header)

    for i in range(len(survey.MD)):
        line = [str(survey.MD[i]) + ',' + str(survey.Inc[i]) + ',' + str(survey.Azi[i]) + ',' + str(survey.TVD[i]) + ','
                + str(survey.North[i]) + ',' + str(survey.East[i]) + ',' + str(survey.Closure[i]) + ','
                + str(survey.Departure[i]) + ',' + str(survey.Section[i]) + ',' + str(survey.DLS[i]) + ','
                + str(survey.Build[i]) + ',' + str(survey.Turn[i]) + ',' + str(survey.Target) +'\n']
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
