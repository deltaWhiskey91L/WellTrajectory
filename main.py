from Utilities import mylogging, writetofile as write, readfromfile as read
import montecarlo
import trajectory
from time import time
import numpy as np
import os

try:
    from Utilities import wellplot
except:
    mylogging.runlog.warn('Import: Cannot import wellplot.py')
    __plotEnabled = False
else:
    __plotEnabled = True

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    mylogging.runlog.warn('Import: matplotlib module not found.')
    __plotEnabled = False

__root_path = os.path.dirname(os.path.abspath(__file__))


def __init__():
    mylogging.runlog.info("START: Now, lets get this thing on the hump. We got some flyin' to do.")
    print("Now, lets get this thing on the hump. We got some flyin' to do.")


def mcm(name='hrcg', target=None, adj=None):
    mylogging.runlog.info('MCM: Calculate survey for {0}'.format(name))
    file = __root_path + '/Data/' + name + '.csv'

    md, inc, azi = read.survey(file)
    survey = trajectory.calculate_survey(md, inc, azi, target, adj=adj, method='MCM')
    write.survey_csv(survey, name=name, method='mcm')


def asc(name='hrcg', target=None, adj=None):
    mylogging.runlog.info('MCM: Calculate survey for {0}'.format(name))
    file = __root_path + '/Data/' + name + '.csv'

    md, inc, azi = read.survey(file)
    survey = trajectory.calculate_survey(md, inc, azi, target, adj=adj, method='ASC')
    write.survey_csv(survey, name=name, method='asc')


def err(base='hrcg_mcm', name='hrcg100_asc'):
    mylogging.runlog.info('Error: Calculate survey error.')
    base_file = __root_path + '/Data/' + base + '.csv'
    file = __root_path + '/Data/' + name + '.csv'

    base_srv = read.complete_survey(file=base_file)
    srv = read.complete_survey(file=file)
    print('Average Error =', np.round(trajectory.error(base_srv[0], srv[0], base_srv[1], srv[1], base_srv[2], srv[2], base_srv[3], srv[3]), 2), 'ft')


def montecarlo_mcm(file='hrcg.csv'):
    mylogging.runlog.info('Monte Carlo: Start Monte Carlo.')
    file = __root_path + '/Data/' + file

    montecarlo.survey_generation()
    asc_list, asc_stats, mcm_list, mcm_stats = montecarlo.survey(100, 142, file)

    if __plotEnabled is True:
        fig1 = plt.figure()
        wellplot.plot_vertical_section(asc_list, target_azimuth=142, size=len(asc_list), fig=fig1, color='b', label='ASC')
        wellplot.plot_vertical_section(mcm_list, size=len(mcm_list), fig=fig1, color='k', label='MCM')
        plt.gca().invert_yaxis()
        plt.legend()

        plt.figure()
        wellplot.plot_horizontal_section(asc_list, size=len(asc_list), color='b', label='ASC')
        wellplot.plot_horizontal_section(mcm_list, size=len(mcm_list), color='k', label='MCM')
        plt.legend()

        plt.figure()
        wellplot.plot_dls(asc_list, size=len(asc_list), color='b', label='ASC')
        wellplot.plot_dls(mcm_list, size=len(mcm_list), color='k', label='MCM')
        plt.gca().invert_yaxis()
        plt.legend()

        plt.show()


if __name__ == '__main__':
    __init__()

    tic = time()
    # asc(name='12', target=345)
    # mcm(name='12', target=345)
    # asc(name='18', target=345, adj=[33.98, 8.39])
    # mcm(name='18', target=345, adj=[33.98, 8.39])
    # asc(name='22', target=345, adj=[67.84, 16.4])
    # mcm(name='22', target=345, adj=[67.84, 16.4])
    # asc(name='29', target=345, adj=[101.74, 23.76])
    # mcm(name='29', target=345, adj=[101.74, 23.76])

    # asc(name='hrcg', target=185)
    mcm(name='hrcg', target=185)
    toc = time()
    print('Elapsed time =', toc - tic, 's')

    if __plotEnabled is True:
        hrmcm = read.complete_survey(__root_path + '/Results/hrcg_mcm.csv', return_dataframe=True)
        hrasc = read.complete_survey(__root_path + '/Results/hrcg_asc.csv', return_dataframe=True)
        wellplot.plot_horizontal_section([hrmcm, hrasc], label=['MCM', 'ASC'], legend=True,
                                         color=['k', 'b'])
        wellplot.plot_vertical_section([hrmcm, hrasc], label=['MCM', 'ASC'], target_azimuth=185, legend=True,
                                       color=['k', 'b'])

        # asc12 = read.complete_survey(__root_path + '/Results/12_asc.csv', return_dataframe=True)
        # mcm12 = read.complete_survey(__root_path + '/Results/12_mcm.csv', return_dataframe=True)
        # asc18 = read.complete_survey(__root_path + '/Results/18_asc.csv', return_dataframe=True)
        # mcm18 = read.complete_survey(__root_path + '/Results/18_mcm.csv', return_dataframe=True)
        # asc22 = read.complete_survey(__root_path + '/Results/22_asc.csv', return_dataframe=True)
        # mcm22 = read.complete_survey(__root_path + '/Results/22_mcm.csv', return_dataframe=True)
        # asc29 = read.complete_survey(__root_path + '/Results/29_asc.csv', return_dataframe=True)
        # mcm29 = read.complete_survey(__root_path + '/Results/29_mcm.csv', return_dataframe=True)
        # wellplot.plot_horizontal_section([mcm12, asc12, mcm18, asc18, mcm22, asc22, mcm29, asc29], legend=True,
        #                              label=['Lynch A Hz 33 HM - MCM', 'Lynch A Hz 33 HM - ASC', 'Lynch A Hz 34 HM - MCM',
        #                                     'Lynch A Hz 34 HM - ASC', 'Lynch A Hz 35 HM - MCM', 'Lynch A Hz 35 HM - ASC',
        #                                     'Lynch A Hz 36 HM - MCM', 'Lynch A Hz 36 HM - ASC'],
        #                              color=[(163 / 255, 147 / 255, 130 / 255), (97 / 255, 70 / 255, 43 / 255),
        #                                     (220 / 255, 74 / 255, 38 / 255), (127 / 255, 48 / 255, 53 / 255),
        #                                     (113 / 255, 197 / 255, 232 / 255), (0 / 255, 79 / 255, 113 / 255),
        #                                     (250 / 255, 224 / 255, 83 / 255), (201 / 255, 151 / 255, 0 / 255)])
        # wellplot.plot_vertical_section([mcm12, asc12, mcm18, asc18, mcm22, asc22, mcm29, asc29], legend=True, target_azimuth=76,
        #                              label=['Lynch A Hz 33 HM - MCM', 'Lynch A Hz 33 HM - ASC', 'Lynch A Hz 34 HM - MCM',
        #                                     'Lynch A Hz 34 HM - ASC', 'Lynch A Hz 35 HM - MCM', 'Lynch A Hz 35 HM - ASC',
        #                                     'Lynch A Hz 36 HM - MCM', 'Lynch A Hz 36 HM - ASC'],
        #                              color=[(163 / 255, 147 / 255, 130 / 255), (97 / 255, 70 / 255, 43 / 255),
        #                                     (220 / 255, 74 / 255, 38 / 255), (127 / 255, 48 / 255, 53 / 255),
        #                                     (113 / 255, 197 / 255, 232 / 255), (0 / 255, 79 / 255, 113 / 255),
        #                                     (250 / 255, 224 / 255, 83 / 255), (201 / 255, 151 / 255, 0 / 255)])

        plt.show()

    print("We'll meet again.")
    mylogging.runlog.info("End: We'll meet again.")
