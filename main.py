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


if __name__ == '__main__':
    __init__()

    from SurveyCalculationMethods import Generic
    survey = Generic.Survey('594survey')
    target = -158

    trajectory.tangential(survey, target, rnd=True)
    trajectory.balanced_tangential(survey, target, rnd=True)
    trajectory.average_angle(survey, target, rnd=True)
    trajectory.vector_average(survey, target, rnd=True)
    trajectory.minimum_curvature(survey, target, rnd=True)
    trajectory.radii_of_curvature(survey, target, rnd=True)
    trajectory.advanced_splines(survey, target, rnd=True)

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
