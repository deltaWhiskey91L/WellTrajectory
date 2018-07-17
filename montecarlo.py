import logging
import numpy as np
import numpy.random as nprand
import trajectory as Survey
from Utilities import unitconverter as units, readfromfile as read
import os

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def survey(size, target_azimuth, survey_file=root_path + '/Data/original_survey.csv',
           error_model_file=root_path + '/Data/ErrorModel.txt'):

    survey_measurements = read.survey(survey_file)
    asc_survey = Survey.calculate_survey(survey_measurements[0], survey_measurements[1],
                                         survey_measurements[2], target_azimuth, method='ASC')
    mcm_survey = Survey.calculate_survey(survey_measurements[0], survey_measurements[1],
                                         survey_measurements[2], target_azimuth, method='MCM')

    # md, inc, azi, tvd, north, east, v_section, dls, build, turn, rugosity, target_azi
    num = len(asc_survey[0])
    asc_list, mcm_list = list(), list()
    asc_stats = [[list(asc_survey[3]), list(asc_survey[3]), np.zeros(num), np.zeros(num)],  # TVD
                [list(asc_survey[4]), list(asc_survey[4]), np.zeros(num), np.zeros(num)],   # NORTHING
                [list(asc_survey[5]), list(asc_survey[5]), np.zeros(num), np.zeros(num)]]   # EASTING [Min, Max, Std, M]
    mcm_stats = [[list(asc_survey[3]), list(asc_survey[3]), np.zeros(num), np.zeros(num)],  # TVD
                [list(asc_survey[4]), list(asc_survey[4]), np.zeros(num), np.zeros(num)],   # NORTHING
                [list(asc_survey[5]), list(asc_survey[5]), np.zeros(num), np.zeros(num)]]   # EASTING [Min, Max, Std, M]

    for itr in range(0, size):
        print(str(itr + 1) + ' of ' + str(size))
        artificial_survey = survey_generation(survey_file, error_model_file)
        art_asc = Survey.calculate_survey(artificial_survey[0], artificial_survey[1], artificial_survey[2],
                                          target_azimuth, method='ASC')
        art_mcm = Survey.calculate_survey(artificial_survey[0], artificial_survey[1], artificial_survey[2],
                                          target_azimuth, method='MCM')
        asc_list.append(art_asc)
        mcm_list.append(art_mcm)

        for i in range(0, len(art_asc[0])):
            for axis in range(0, 3):
                asc_stats[axis][0][i] = min_recursive(art_asc[axis + 3][i], asc_stats[axis][0][i])
                asc_stats[axis][1][i] = max_recursive(art_asc[axis + 3][i], asc_stats[axis][1][i])
                asc_stats[axis][2][i], asc_stats[axis][3][i] = std_recursive(art_asc[axis + 3][i],
                                                                             asc_survey[axis + 3][i],
                                                                             itr + 1, asc_survey[axis + 3][i],
                                                                             asc_stats[axis][3][i])

                mcm_stats[axis][0][i] = min_recursive(art_mcm[axis + 3][i], mcm_stats[axis][0][i])
                mcm_stats[axis][1][i] = max_recursive(art_mcm[axis + 3][i], mcm_stats[axis][1][i])
                mcm_stats[axis][2][i], mcm_stats[axis][3][i] = std_recursive(art_mcm[axis + 3][i],
                                                                             mcm_survey[axis + 3][i],
                                                                             itr + 1, mcm_survey[axis + 3][i],
                                                                             mcm_stats[axis][3][i])

    asc_list.append(asc_survey)
    mcm_list.append(mcm_survey)

    return asc_list, asc_stats, mcm_list, mcm_stats


def survey_generation(survey_file=root_path + '/Data/original_survey.csv',
                      error_model_file=root_path + '/Data/ErrorModel.txt'):
    """
    Generates an artificial surveys using NORMAL DISTRIBUTION

    :param survey_file:
    :param error_model_file:
    """

    survey = read.survey(survey_file, return_dataframe=True)
    error_model = read.error_model(error_model_file)

    error_md = units.from_si(units.to_si(error_model.loc[error_model.Name == 'md'].Magnitude.values[0],
                                         error_model.loc[error_model.Name == 'md'].Unit.values[0]), 'ft')
    error_inc = units.from_si(units.to_si(error_model.loc[error_model.Name == 'inc'].Magnitude.values[0],
                                          error_model.loc[error_model.Name == 'inc'].Unit.values[0]), 'dega')
    error_azi = units.from_si(units.to_si(error_model.loc[error_model.Name == 'azi'].Magnitude.values[0],
                                          error_model.loc[error_model.Name == 'azi'].Unit.values[0]), 'dega')

    md, inc, azi = list(), list(), list()
    md.append(nprand.normal(survey.iloc[0][0], error_md))
    inc.append(nprand.normal(survey.iloc[0][1], error_inc))
    azi.append(nprand.normal(survey.iloc[0][2], error_azi))
    for j in range(1, len(survey)):
        md.append(md[j-1] + (survey.iloc[j][0] - survey.iloc[j-1][0]) + nprand.normal(0, error_md))
        inc.append(nprand.normal(survey.iloc[j][1], error_inc))
        azi.append(nprand.normal(survey.iloc[j][2], error_azi))

    survey_normal = [md, inc, azi]
    return survey_normal


def mean_recursive(value, num_samples, mean_previous):
    mean = mean_previous + (value - mean_previous)/num_samples
    return mean


def std_recursive(value, mean, num_samples, mean_previous, M_previous):
    M = M_previous + (value - mean_previous) * (value - mean)
    std = np.sqrt(M / num_samples)
    return std, M


def min_recursive(value, previous):
    if value < previous:
        return value
    return previous


def max_recursive(value, previous):
    if value > previous:
        return value
    return previous


