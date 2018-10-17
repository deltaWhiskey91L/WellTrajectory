import numpy as np
from scipy.stats import norm

def sigma_matrix(radius_vector):
    """
    3x3 diagonal radius matrix
    :param radius_vector: radius vector of the ellipsoid, standard deviation along wellbore, horizontal, and vertical
    :type radius_vector: np.array
    :return: sigma matrix
    :rtype: np.array
    """
    Sigma = np.eye(3)
    for i in range(0, 3):
        Sigma[i][i] = 1 / radius_vector[i]
    return Sigma


def unit_matrix(inclination, azimuth):
    """
    3x3 orthogonal unit matrix, U

    :param inclination: inclination, inc (dega)
    :type inclination: float
    :param azimuth: azimuth, azi (dega)
    :type azimuth: float
    :return: unit matrix, U
    :rtype: np.array
    """
    inclination = np.radians(inclination)
    azimuth = np.radians(azimuth)

    matrix = list()
    matrix.append([np.cos(azimuth) * np.sin(inclination), np.sin(azimuth) * np.sin(inclination), np.cos(inclination)])
    matrix.append([np.cos(azimuth - np.pi/2), np.sin(azimuth - np.pi/2), 0])
    matrix.append([np.cos(azimuth + np.pi) * np.sin(inclination - np.pi/2),
                   np.sin(azimuth + np.pi) * np.sin(inclination - np.pi/2), -np.cos(inclination-np.pi/2)])

    return np.array(matrix)


def intersect(m1, m2, std1, std2):
    """
    Points of intersection of two overlapping normal distributions

    :param m1: mean of distribution 1
    :type m1: float
    :param m2: mean of distribution 2
    :type m2: float
    :param std1: standard deviation of distribution 1
    :type std1: float
    :param std2: standard deviation of distribution 2
    :type std2: float
    :return: intersection points
    :rtype: list
    """

    a = 1. / (2. * std1 ** 2) - 1. / (2. * std2 ** 2)
    b = m2 / (std2 ** 2) - m1 / (std1 ** 2)
    c = m1 ** 2 / (2. * std1 ** 2) - m2 ** 2 / (2. * std2 ** 2) - np.log(std2 / std1)
    return np.roots([a, b, c])


def ovl(m1, m2, std1, std2):
    """
    Points of intersection of two overlapping normal distributions

    :param m1: mean of distribution 1
    :type m1: float
    :param m2: mean of distribution 2
    :type m2: float
    :param std1: standard deviation of distribution 1
    :type std1: float
    :param std2: standard deviation of distribution 2
    :type std2: float
    :return: intersection points
    :rtype: list
    """

    pts = intersect(m1, m2, std1, std2)

    if len(pts) == 0:
        return 0

    if len(pts) == 1:
        r = pts[0]
        if m1 > m2:
            return norm.cdf(r, m1, std1) + (1. - norm.cdf(r, m2, std2))
        else:
            return norm.cdf(r, m2, std2) + (1. - norm.cdf(r, m1, std1))

    r = np.sort(pts)
    y = norm.pdf(pts, m1, std1)
    if m1 > m2:
        return norm.cdf(r[0], m1, std1) + (norm.cdf(r[1], m2, std2) - norm.cdf(r[0], m2, std2)) \
               + (1. - norm.cdf(pts[1], m1, std1))
    else:
        print(norm.cdf(r[0], m2, std2))
        print(1 - norm.cdf(r[1], m2, std2))
        print((norm.cdf(r[1], m1, std1) - norm.cdf(r[0], m1, std1)))
        return norm.cdf(r[0], m2, std2) + (norm.cdf(r[1], m1, std1) - norm.cdf(r[0], m1, std1)) \
               + (1. - norm.cdf(r[1], m2, std2))
