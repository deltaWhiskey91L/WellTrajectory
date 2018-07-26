from Utilities import mylogging, writetofile as write, readfromfile as read
import montecarlo
import trajectory
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
        wellplot.plot_dls(asc_list, color='b', label='ASC')
        wellplot.plot_dls(mcm_list, color='k', label='MCM')
        plt.gca().invert_yaxis()
        plt.legend()

        plt.show()


def montecarlo_generation(file='hrcg.csv'):
    pass


def synthetic_well():
    from Survey import Synthetic
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D

    alpha, delta, xi = 1000, 100, 100
    tvd, ns, ew = Synthetic.true_well(delta, alpha, xi, size=10000)
    md, inc, azi = Synthetic.survey(delta, alpha, xi, size=300)
    print(azi)

    Synthetic.write_well(tvd, ns, ew)
    Synthetic.write_survey(md, inc, azi)

    mcm('synthetic', target=355)
    asc('synthetic', target=355)

    mcmsyn = read.complete_survey(__root_path + '/Results/synthetic_mcm.csv', return_dataframe=True)
    ascsyn = read.complete_survey(__root_path + '/Results/synthetic_asc.csv', return_dataframe=True)
    syn = read.complete_survey(__root_path + '/Results/synthetic_true.csv', return_dataframe=True)

    plt.figure()
    plt.plot(syn.EW.values, syn.NS.values, label='Helical', color='k', alpha=0.5)
    plt.scatter(mcmsyn.EW.values, mcmsyn.NS.values, label='MCM', color='r', s=2)
    plt.scatter(ascsyn.EW.values, ascsyn.NS.values, label='ASC', color='b', s=2)
    plt.xlabel('East/West')
    plt.ylabel('North/South')
    plt.legend(loc=1)
    plt.gca().invert_yaxis()

    plt.figure()
    plt.plot(syn.EW.values, syn.TVD.values, label='Helical', color='k', alpha=0.5)
    plt.scatter(mcmsyn.EW.values, mcmsyn.TVD.values, label='MCM', color='r', s=2)
    plt.scatter(ascsyn.EW.values, ascsyn.TVD.values, label='ASC', color='b', s=2)
    plt.xlabel('East/West')
    plt.ylabel('True Vertical Depth')
    # plt.legend(loc=1)
    plt.gca().invert_yaxis()

    # mpl.rcParams['legend.fontsize'] = 10
    # fig = plt.figure()
    # ax = fig.gca(projection='3d')
    # ax.plot(ew, ns, tvd, label='Synthetic', color='k')
    # ax.plot(mcmsyn.EW.values, mcmsyn.NS.values, mcmsyn.TVD.values, label='MCM', color='b')
    # ax.plot(ascsyn.EW.values, ascsyn.NS.values, ascsyn.TVD.values, label='ASC', color='r')
    # plt.xlabel('East/West')
    # plt.ylabel('North/South')
    # plt.gca().invert_zaxis()
    # ax.legend()

    plt.show()


if __name__ == '__main__':
    __init__()

    import sys
    synthetic_well()
    sys.exit()

    from time import time
    # target = 75.3
    target = 345

    tic = time()
    asc(name='12', target=target)
    mcm(name='12', target=target)
    asc(name='18', target=target, adj=[33.98, 8.39])
    mcm(name='18', target=target, adj=[33.98, 8.39])
    asc(name='22', target=target, adj=[67.84, 16.4])
    mcm(name='22', target=target, adj=[67.84, 16.4])
    asc(name='29', target=target, adj=[101.74, 23.76])
    mcm(name='29', target=target, adj=[101.74, 23.76])

    # asc(name='test', target=90)
    # mcm(name='test', target=90)

    # asc(name='hrcg', target=185)
    # mcm(name='hrcg', target=185)
    toc = time()
    print('Elapsed time =', toc - tic, 's')

    __plotEnabled = True

    if __plotEnabled is True:
        # hrmcm = read.complete_survey(__root_path + '/Results/hrcg_mcm.csv', return_dataframe=True)
        # hrasc = read.complete_survey(__root_path + '/Results/hrcg_asc.csv', return_dataframe=True)
        # wellplot.plot_horizontal_section([hrmcm, hrasc], label=['MCM', 'ASC'], legend=True,
        #                                  color=['k', 'b'])
        # wellplot.plot_vertical_section([hrmcm, hrasc], label=['MCM', 'ASC'], target_azimuth=185, legend=True,
        #                                color=['k', 'b'])

        # mcm = read.complete_survey(__root_path + '/Results/test_mcm.csv', return_dataframe=True)
        # asc = read.complete_survey(__root_path + '/Results/test_asc.csv', return_dataframe=True)
        #
        # wellplot.plot_horizontal_section([mcm, asc], legend=True, label=['MCM', 'ASC'], color=['r', 'k'])
        # wellplot.plot_vertical_section([mcm, asc], legend=True, label=['MCM', 'ASC'], color=['r', 'k'])

        asc12 = read.complete_survey(__root_path + '/Results/12_asc.csv', return_dataframe=True)
        mcm12 = read.complete_survey(__root_path + '/Results/12_mcm.csv', return_dataframe=True)
        asc18 = read.complete_survey(__root_path + '/Results/18_asc.csv', return_dataframe=True)
        mcm18 = read.complete_survey(__root_path + '/Results/18_mcm.csv', return_dataframe=True)
        asc22 = read.complete_survey(__root_path + '/Results/22_asc.csv', return_dataframe=True)
        mcm22 = read.complete_survey(__root_path + '/Results/22_mcm.csv', return_dataframe=True)
        asc29 = read.complete_survey(__root_path + '/Results/29_asc.csv', return_dataframe=True)
        mcm29 = read.complete_survey(__root_path + '/Results/29_mcm.csv', return_dataframe=True)
        wellplot.plot_horizontal_section([mcm12, asc12, mcm18, asc18, mcm22, asc22, mcm29, asc29], legend=False,
                                         limits=[[-6000, 3000], [-500, 8500]],
                                     label=['Lynch A Hz 33 HM - MCM', 'Lynch A Hz 33 HM - ASC', 'Lynch A Hz 34 HM - MCM',
                                            'Lynch A Hz 34 HM - ASC', 'Lynch A Hz 35 HM - MCM', 'Lynch A Hz 35 HM - ASC',
                                            'Lynch A Hz 36 HM - MCM', 'Lynch A Hz 36 HM - ASC'],
                                     color=[(163 / 255, 147 / 255, 130 / 255), (97 / 255, 70 / 255, 43 / 255),
                                            (220 / 255, 74 / 255, 38 / 255), (127 / 255, 48 / 255, 53 / 255),
                                            (113 / 255, 197 / 255, 232 / 255), (0 / 255, 79 / 255, 113 / 255),
                                            (250 / 255, 224 / 255, 83 / 255), (201 / 255, 151 / 255, 0 / 255)],
                                     linestyle=['-', '--', '-', '--', '-', '--', '-', '--'])
        wellplot.plot_vertical_section([mcm12, asc12, mcm18, asc18, mcm22, asc22, mcm29, asc29], legend=True, target_azimuth=target,
                                     label=['Lynch A Hz 33 HM - MCM', 'Lynch A Hz 33 HM - ASC', 'Lynch A Hz 34 HM - MCM',
                                            'Lynch A Hz 34 HM - ASC', 'Lynch A Hz 35 HM - MCM', 'Lynch A Hz 35 HM - ASC',
                                            'Lynch A Hz 36 HM - MCM', 'Lynch A Hz 36 HM - ASC'],
                                     color=[(163 / 255, 147 / 255, 130 / 255), (97 / 255, 70 / 255, 43 / 255),
                                            (220 / 255, 74 / 255, 38 / 255), (127 / 255, 48 / 255, 53 / 255),
                                            (113 / 255, 197 / 255, 232 / 255), (0 / 255, 79 / 255, 113 / 255),
                                            (250 / 255, 224 / 255, 83 / 255), (201 / 255, 151 / 255, 0 / 255)],
                                     linestyle=['-', '--', '-', '--', '-', '--', '-', '--'])

        plt.figure()
        wellplot.plot_dls([mcm12, asc12], legend=False,
                                     label=['Lynch A Hz 33 HM - MCM', 'Lynch A Hz 33 HM - ASC'],
                                     color=[(163 / 255, 147 / 255, 130 / 255), (97 / 255, 70 / 255, 43 / 255)],
                                     linestyle=['-', '--'])

        plt.figure()
        wellplot.plot_dls([mcm18, asc18], legend=True,
                                     label=['Lynch A Hz 34 HM - MCM', 'Lynch A Hz 34 HM - ASC'],
                                     color=[(220 / 255, 74 / 255, 38 / 255), (127 / 255, 48 / 255, 53 / 255)],
                                     linestyle=['-', '--'])

        plt.figure()
        wellplot.plot_dls([mcm22, asc22], legend=False,
                                     label=['Lynch A Hz 35 HM - MCM', 'Lynch A Hz 35 HM - ASC'],
                                     color=[(113 / 255, 197 / 255, 232 / 255), (0 / 255, 79 / 255, 113 / 255)],
                                     linestyle=['-', '--'])

        plt.figure()
        wellplot.plot_dls([mcm29, asc29], legend=True,
                                     label=['Lynch A Hz 36 HM - MCM', 'Lynch A Hz 36 HM - ASC'],
                                     color=[(250 / 255, 224 / 255, 83 / 255), (201 / 255, 151 / 255, 0 / 255)],
                                     linestyle=['-', '--'])

        plt.show()

    print("We'll meet again.")
    mylogging.runlog.info("End: We'll meet again.")
