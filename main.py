from Utilities import mylogging, wellplot as Plot, writetofile as write, readfromfile as read
import montecarlo, trajectory
import matplotlib.pyplot as plt
import numpy as np
import os

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

    fig1 = plt.figure()
    Plot.plot_vertical_section(asc_list, target_azimuth=142, size=len(asc_list), fig=fig1, color='b', label='ASC')
    Plot.plot_vertical_section(mcm_list, size=len(mcm_list), fig=fig1, color='k', label='MCM')
    plt.gca().invert_yaxis()
    plt.legend()

    plt.figure()
    Plot.plot_horizontal_section(asc_list, size=len(asc_list), color='b', label='ASC')
    Plot.plot_horizontal_section(mcm_list, size=len(mcm_list), color='k', label='MCM')
    plt.legend()

    plt.figure()
    Plot.plot_dls(asc_list, size=len(asc_list), color='b', label='ASC')
    Plot.plot_dls(mcm_list, size=len(mcm_list), color='k', label='MCM')
    plt.gca().invert_yaxis()
    plt.legend()

    plt.show()


if __name__ == '__main__':
    __init__()
    azi = 285

    asc(name='hrcg', target=185)
    mcm(name='hrcg', target=185)
    asc(name='hrcg100', target=185)
    mcm(name='hrcg100', target=185)


    hrmcm = read.complete_survey(__root_path + '/Results/hrcg_mcm.csv', return_dataframe=True)
    hrasc = read.complete_survey(__root_path + '/Results/hrcg_asc.csv', return_dataframe=True)
    Plot.plot_horizontal_section([hrmcm, hrasc], label=['MCM', 'ASC'], legend=True,
                                 color=['k', 'b', 'r', 'm'])
    Plot.plot_vertical_section([hrmcm, hrasc], label=['MCM', 'ASC'], target_azimuth=azi, legend=True,
                               color=['k', 'b', 'r', 'm'])
    plt.show()

    print('Target Destroyed')
    mylogging.runlog.info("End: We'll meet again.")
