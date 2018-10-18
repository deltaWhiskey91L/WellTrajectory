from Utilities import mylogging, writetofile as write, readfromfile as read
import montecarlo
from SurveyCalculationMethods import trajectory
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
    print('Average Error =', np.round(
        trajectory.error(base_srv[0], srv[0], base_srv[1], srv[1], base_srv[2], srv[2], base_srv[3], srv[3]), 2), 'ft')


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
    import Synthetic

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

    from SurveyCalculationMethods import Generic
    survey = Generic.Survey('594survey')
    target = -158

    # trajectory.tangential('594survey', target_azimuth=-158)
    # trajectory.balanced_tangential('594survey', target_azimuth=-158)
    trajectory.average_angle(survey, target, rnd=True)
    # trajectory.vector_average('594survey', target_azimuth=-158)
    # trajectory.minimum_curvature('594survey', target_azimuth=-158)
    # trajectory.minimum_curvature2('594survey', target_azimuth=-158)
    # trajectory.radii_of_curvature('594survey', target_azimuth=-158)
    # trajectory.advanced_splines('594survey', target_azimuth=-158)
    import sys
    sys.exit()
    print(__root_path)
    tan = read.complete_survey(__root_path + '/Results/594survey_Tangential.csv')
    baltan = read.complete_survey(__root_path + '/Results/594survey_BalancedTangential.csv')
    avgang = read.complete_survey(__root_path + '/Results/594survey_AverageAngle.csv')
    vecavg = read.complete_survey(__root_path + '/Results/594survey_VectorAverage.csv')
    mcm = read.complete_survey(__root_path + '/Results/594survey_MinimumCurvature2.csv')
    radii = read.complete_survey(__root_path + '/Results/594survey_RadiiOfCurvature.csv')
    asc = read.complete_survey(__root_path + '/Results/594survey_AdvancedSplines.csv')

    wellplot.plot_vertical_section(tan, target_azimuth=target, label='Tangential')
    wellplot.plot_horizontal_section(tan, label='Tangential')
    plt.show()

    print("We'll meet again.")
    mylogging.runlog.info("End: We'll meet again.")
