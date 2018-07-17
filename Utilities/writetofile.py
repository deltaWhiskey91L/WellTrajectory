from Utilities import mylogging
import numpy as np
import os


root_path = os.path.dirname(os.path.dirname(__file__))


def survey_short_csv(survey, iteration=None, dataframe=False):
    if iteration is not None:
        mylogging.runlog.info('Write: Writing the {0} survey to .csv.'.format(iteration))
        file = root_path + '/Results/survey{0}.csv'.format(iteration)
    else:
        mylogging.runlog.info('Write: Writing the survey to .csv.')
        file = root_path + '/Results/survey.csv'

    header = ['MD,Inc,Azi \n']

    f = open(file, 'w')
    f.writelines(header)

    for i in range(0, len(survey)):
        if dataframe is True:
            line = [str(survey.iloc[i][0]) + ',' + str(survey.iloc[i][1]) + ',' + str(survey.iloc[i][2]) + '\n']
        else:
            line = [str(survey[i][0]) + ',' + str(survey[i][1]) + ',' + str(survey[i][2]) + '\n']
        f.writelines(line)
    f.close()


def survey_csv(survey, name=None, method='mcm', iteration=None):
    if iteration is not None:
        mylogging.runlog.info('Write: Writing the {0} survey to .csv.'.format(iteration))
        file = root_path + '/Results/{0}_{1}{2}.csv'.format(name, method, iteration)
    else:
        mylogging.runlog.info('Write: Writing the survey to .csv.')
        file = root_path + '/Results/{0}_{1}.csv'.format(name, method)

    header = ['MD,Inc,Azi,TVD,NS,EW,Section,DLS,Build,Turn,Rugosity,Target \n']

    f = open(file, 'w')
    f.writelines(header)

    for i in range(0, len(survey[0])):
        line = [str(survey[0][i]) + ',' + str(np.degrees(survey[1][i])) + ',' + str(np.degrees(survey[2][i])) + ',' + str(survey[3][i]) + ','
                + str(survey[4][i]) + ',' + str(survey[5][i]) + ',' + str(survey[6][i]) + ',' + str(np.degrees(survey[7][i])) + ','
                + str(np.degrees(survey[8][i])) + ',' + str(np.degrees(survey[9][i])) + ',' + str(np.degrees(survey[10][i])) + ',' + str(survey[11]) + '\n']
        f.writelines(line)
    f.close()
