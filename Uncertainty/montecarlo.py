from Utilities import mylogging, writetofile as write
import numpy as np
import os

root_path = os.path.dirname(os.path.realpath(__file__))


class error_model:
    def __init__(self):
        self.md = 0.5 / 2
        self.md_persist = 0
        self.md_unit = 'ft'
        self.inc = 0.15 / 2
        self.inc_persist = 0
        self.inc_unit = 'dega'
        self.azi = 0.25 / 2
        self.azi_persist = 0
        self.azi_unit = 'dega'


def surveys(survey_object, path, error_object=None, size=1000):
    """
    Generates randomized survey files using a normal distribution from the original.
    :param survey_object: Original survey
    :param error_object: Error model object
    :param size: Monte Carlo size
    :type size: int
    :param path: Output file path
    :type path: str
    """
    mylogging.alglog.info('MonteCarlo: Generate survey model inputs')

    if error_object is None:
        error_object = error_model()

    md, inc, azi = list(), list(), list()
    for i in range(size):
        print(path, str(i + 1), 'of', str(size))
        md_error = 0
        for j in range(len(survey_object.md)):
            md_error += np.random.normal(0, error_object.md)
            md.append(survey_object.md[j] + md_error)
            phi = np.random.normal(survey_object.inc[j], error_object.inc)
            theta = np.random.normal(survey_object.azi[j], error_object.azi)

            if phi < 0:
                inc.append(np.abs(phi))
                azi.append(np.degrees(np.radians(theta) + np.pi))
            else:
                inc.append(phi), azi.append(theta)

        file = path + '_' + str(i + 1) + '.csv'
        write.survey_measurements(md, inc, azi, file)
        md.clear()
        inc.clear()
        azi.clear()


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


