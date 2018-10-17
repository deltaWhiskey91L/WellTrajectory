from Utilities import mylogging, unitconverter as units
import numpy as np
import os

root_path = os.path.dirname(os.path.dirname(__file__))


def write_well(tvd, north, east):
    mylogging.runlog.info('Write: Writing the synthetic wellbore to .csv.')
    file = root_path + '/Results/synthetic_true.csv'

    header = ['TVD,NS,EW\n']

    f = open(file, 'w')
    f.writelines(header)
    for i in range(0, len(tvd)):
        line = [str(tvd[i]) + ',' + str(north[i]) + ',' + str(east[i]) + '\n']
        f.writelines(line)
    f.close()


def write_survey(md, inc, azi):
    mylogging.runlog.info('Write: Writing the synthetic survey to .csv.')
    file = root_path + '/Data/synthetic.csv'

    header = ['MD,Inc,Azi\n0,0,0\n']

    f = open(file, 'w')
    f.writelines(header)
    for i in range(0, len(md)):
        line = [str(md[i]) + ',' + str(inc[i]) + ',' + str(azi[i]) + '\n']
        f.writelines(line)
    f.close()


def true_well(delta, alpha, xi, size=10000):
    t = np.linspace(0, 1, size)
    east = x_vector_1(delta, xi, t)
    north = x_vector_2(delta, xi, t)
    tvd = x_vector_3(alpha, t)
    return tvd, north, east


def survey(delta, alpha, xi, size=100):
    g = gamma(delta, alpha, xi)
    s = s_vector(g, size)
    y1 = y_vector_1(delta, xi, g, s)
    y2 = y_vector_2(delta, xi, g, s)
    y3 = y_vector_3(alpha, g, s)

    inc, azi = incazi(y1, y2, y3)
    print('survey()', azi)
    return s, inc, azi


def gamma(delta, alpha, xi):
    return np.sqrt(delta ** 2 * xi ** 2 + alpha ** 2)


def x_vector_1(delta, xi, t):
    return delta * np.sin(xi * t)


def x_vector_2(delta, xi, t):
    return delta * (1 - np.cos(xi * t))


def x_vector_3(alpha, t):
    return alpha * t


def y_vector_1(delta, xi, gamma, s):
    return delta * xi / gamma * np.cos(xi * s / gamma)


def y_vector_2(delta, xi, gamma, s):
    return -1 * delta * xi / gamma * np.sin(xi * s / gamma)


def y_vector_3(alpha, gamma, s):
    return np.ones(len(s)) * alpha / gamma


def s_vector(gamma, n):
    s = np.zeros(n + 1)
    for i in range(1, n + 1):
        s[i] = i * gamma / n
    return s


def incazi(y1, y2, y3):
    inc, azi = np.zeros(len(y1)), np.zeros(len(y1))
    for i in range(0, len(inc)):
        inc[i] = units.from_si(np.arccos(y3[i]), 'dega')
        if y2[i] == 0:
            if y1[i] > 0:
                azi[i] = np.pi / 2
            else:
                azi[i] = np.pi * 3 / 2
        else:
            if y1[i] < 0 and y2[i] < 0:
                azi[i] = 2 * np.pi - np.arctan(y1[i] / y2[i])
            elif y1[i] > 0 and y2[i] > 0:
                azi[i] = np.abs(np.pi / 2 - np.arctan(y1[i] / y2[i])) + np.pi / 2
            elif y1[i] < 0 < y2[i]:
                azi[i] = np.abs(np.arctan(y1[i] / y2[i])) + np.pi
            else:
                azi[i] = 2 * np.pi - np.arctan(y1[i] / y2[i])

        azi[i] = np.degrees(azi[i])
        if inc[i] < 0:
            inc[i] = np.abs(inc[i])
            azi[i] = azi[i] + 180
        azi[i] = azi[i] - (azi[i] // 360) * 360
        print(azi[i])
    return inc, azi
