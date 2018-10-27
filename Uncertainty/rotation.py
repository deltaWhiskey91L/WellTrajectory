from SurveyCalculationMethods import  Generic
import numpy as np


def rotated_point(point, inc, azi):
    """
    Rotates coordinates of point parallel to vector with inc and azi

    :param point: point, P (v, n, e)
    :type point: np.array
    :param inc: inclination of vector (rad)
    :type inc: float
    :param azi: azimuth of vector (rad)
    :type azi: float
    :return: new coordinates of point P (Up/Down, Left/Right, Forward/Backward)
    """

    theta = np.radians(Generic.closure_azimuth(point[1], point[2]))
    phi = np.arctan2(np.linalg.norm(np.array([point[1], point[2]])), point[0])

    A = azi - theta
    B = inc - phi

    R = rotation_matrix(A, B)
    P = np.matmul(point, R)
    P = np.array([-1, -1, 1]) * P
    return P


def rotation_matrix(delta_theta, delta_phi):
    """
    Rotation matrix for Delta P [v, n, e]

    :param delta_theta: change in azimuth (rad)
    :type delta_theta: float
    :param delta_phi: change in inclination (rad)
    :type delta_phi: float
    :return: rotation matrix
    :rtype: np.array
    """

    Rv = np.array([[1, 0, 0],
                   [0, np.cos(delta_theta), -np.sin(delta_theta)],
                   [0, np.sin(delta_theta), np.cos(delta_theta)]])
    Rn = np.array([[np.cos(delta_phi), 0, -np.sin(delta_phi)],
                   [0, 1, 0],
                   [np.sin(delta_phi), 0, np.cos(delta_phi)]])

    return np.matmul(Rv, Rn)


def unit_vector_point(point):
    """
    Unit vector for a given inclination and azimuth

    :param point: point, P [v, n, w]
    :type point: list
    :return: unit vector, w_hat
    :rtype: np.array
    """

    theta = np.radians(Generic.closure_azimuth(point[1], point[2]))
    phi = np.arctan2(np.linalg.norm(np.array([point[1], point[2]])), point[0])

    return np.array([np.cos(phi), np.sin(phi) * np.cos(theta), np.sin(phi) * np.sin(theta)])


def unit_vector_angle(inc, azi):
    """
    Unit vector for a given inclination and azimuth

    :param inc: inclination, inc (rad)
    :type inc: float
    :param azi: azimuth, azi (rad)
    :type inc: float
    :return: unit vector, w_hat
    :rtype: np.array
    """

    return np.array([np.cos(inc), np.sin(inc) * np.cos(azi), np.sin(inc) * np.sin(azi)])
