from Utilities import mylogging
from SurveyCalculationMethods import trajectory
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


def all_surveys(name, target, location, N=1000):
    from SurveyCalculationMethods import Generic
    for i in range(N):
        print(name, str(i + 1), 'of', str(N))
        survey = Generic.Survey(name + '_' + str(i + 1), path=__root_path + '/Data/' + name + '/')
        trajectory.minimum_curvature(survey, target, location=location)
        trajectory.advanced_splines(survey, target, location=location)
        del survey


def plot_mc(name, index=-1, N=1000):
    from Utilities import readfromfile as read
    from Uncertainty import rotation
    import numpy as np

    base_file = __root_path + '/Results/' + name + 'gyro_MinimumCurvature.csv'
    base = read.complete_survey(base_file)

    md, inc, azi = base[0][index], base[1][index], base[2][index]
    base_tvd, base_north, base_east = base[3][index], base[4][index], base[5][index]
    mcm_up, mcm_right, mcm_front = list(), list(), list()
    asc_up, asc_right, asc_front = list(), list(), list()

    for i in range(N):
        mcm_file = __root_path + '/Results/' + name + '_' + str(i + 1) + '_mcm.csv'
        asc_file = __root_path + '/Results/' + name + '_' + str(i + 1) + '_asc.csv'
        mcm = read.complete_survey(mcm_file)
        asc = read.complete_survey(asc_file)

        tvd_mcm, north_mcm, east_mcm = mcm[3][index] - base_tvd, mcm[4][index] - base_north, mcm[5][index] - base_east
        delta_Pmcm = rotation.rotated_point(np.array([tvd_mcm, north_mcm, east_mcm]), np.radians(inc), np.radians(azi))

        tvd_asc, north_asc, east_asc = asc[3][index] - base_tvd, asc[4][index] - base_north, asc[5][index] - base_east
        delta_Pasc = rotation.rotated_point(np.array([tvd_asc, north_asc, east_asc]), np.radians(inc), np.radians(azi))

        mcm_up.append(delta_Pmcm[0])
        mcm_right.append(delta_Pmcm[1])
        mcm_front.append(delta_Pmcm[2])
        asc_up.append(delta_Pasc[0])
        asc_right.append(delta_Pasc[1])
        asc_front.append(delta_Pasc[2])

    import matplotlib.pyplot as plt

    fig = plt.figure()
    plt.scatter(mcm_right, mcm_front, label='MCM', color='k', s=2)
    plt.scatter(asc_right, asc_front, label='ASC', color='r', s=2, marker='x')
    plt.legend()
    plt.xlabel('Left/Right (ft)')
    plt.ylabel('Front/Back (ft)')
    fig.text(.5, .86, name, ha="center", va="center")
    plt.grid(linestyle='dashed')

    fig = plt.figure()
    plt.scatter(mcm_front, mcm_up, label='MCM', color='k', s=2)
    plt.scatter(asc_front, asc_up, label='ASC', color='r', s=2, marker='x')
    plt.legend()
    plt.xlabel('Front/Back (ft)')
    plt.ylabel('Up/Down (ft)')
    fig.text(.5, .86, name, ha="center", va="center")
    plt.grid(linestyle='dashed')
    plt.gca().invert_yaxis()

    fig = plt.figure()
    plt.scatter(mcm_right, mcm_up, label='MCM', color='k', s=2)
    plt.scatter(asc_right, asc_up, label='ASC', color='r', s=2, marker='x')
    plt.legend()
    plt.xlabel('Right/Left (ft)')
    plt.ylabel('Up/Down (ft)')
    fig.text(.5, .86, name, ha="center", va="center")
    plt.grid(linestyle='dashed')
    plt.gca().invert_yaxis()


if __name__ == '__main__':
    __init__()

    from SurveyCalculationMethods import Generic
    # Asurvey = Generic.Survey('A')
    Bsurvey = Generic.Survey('B')
    Csurvey = Generic.Survey('C')
    Dsurvey = Generic.Survey('D')
    Esurvey = Generic.Survey('E')
    target = 165

    import matplotlib.pyplot as plt
    from Uncertainty import montecarlo
    # montecarlo.surveys(Asurvey, __root_path + '/Data/A/A', size=1000)
    # montecarlo.surveys(Bsurvey, __root_path + '/Data/B/B', size=1000)
    # montecarlo.surveys(Csurvey, __root_path + '/Data/C/C', size=1000)
    # montecarlo.surveys(Dsurvey, __root_path + '/Data/D/D', size=1000)
    # montecarlo.surveys(Esurvey, __root_path + '/Data/E/E', size=1000)

    # all_surveys('A', target, (8.97793484, 28.62053526))
    # all_surveys('B', target, (-17.94649231, -57.30360237))
    # all_surveys('C', target, (-8.96780121, -28.65193616))
    # all_surveys('D', target, (0, 0))
    # all_surveys('E', target, (17.95670173, 57.272162))

    plot_mc('A')
    plot_mc('B')
    plot_mc('C')
    plot_mc('D')
    plot_mc('E')

    plt.show()

    # trajectory.minimum_curvature(Asurvey, target, location=(8.97793484, 28.62053526))
    # trajectory.advanced_splines(Asurvey, target, location=(8.97793484, 28.62053526))
    #
    # trajectory.minimum_curvature(Bsurvey, target, location=(-17.94649231, -57.30360237))
    # trajectory.advanced_splines(Bsurvey, target, location=(-17.94649231, -57.30360237))
    # trajectory.minimum_curvature(Csurvey, target, location=(-8.96780121, -28.65193616))
    # trajectory.advanced_splines(Csurvey, target, location=(-8.96780121, -28.65193616))
    # trajectory.minimum_curvature(Dsurvey, target)
    # trajectory.advanced_splines(Dsurvey, target)
    # trajectory.minimum_curvature(Esurvey, target, location=(17.95670173, 57.272162))
    # trajectory.advanced_splines(Esurvey, target, location=(17.95670173, 57.272162))



    # mcm(name='A', target=azi, offset_east=28.62053526, offset_north=8.97793484)
    # mcm(name='B', target=azi, offset_east=-57.30360237, offset_north=-17.94649231)
    # mcm(name='C', target=azi, offset_east=-28.65193616, offset_north=-8.96780121)
    # mcm(name='D', target=azi)
    # mcm(name='E', target=azi, offset_east=57.272162, offset_north=17.95670173)

    # print(__root_path)
    # tan = read.complete_survey(__root_path + '/Results/594survey_Tangential.csv')
    # baltan = read.complete_survey(__root_path + '/Results/594survey_BalancedTangential.csv')
    # avgang = read.complete_survey(__root_path + '/Results/594survey_AverageAngle.csv')
    # vecavg = read.complete_survey(__root_path + '/Results/594survey_VectorAverage.csv')
    # mcm = read.complete_survey(__root_path + '/Results/594survey_MinimumCurvature.csv')
    # radii = read.complete_survey(__root_path + '/Results/594survey_RadiusOfCurvature.csv')
    # asc = read.complete_survey(__root_path + '/Results/594survey_AdvancedSplineCurve.csv')

    # wellplot.plot_vertical_section(tan, target_azimuth=target, label='Tangential')
    # wellplot.plot_horizontal_section(tan, label='Tangential')
    # plt.show()

    print("We'll meet again.")
    mylogging.runlog.info("End: We'll meet again.")
