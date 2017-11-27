import datetime
import logging
import os

import UnitConverter as Units
import math as m

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG


def next_pt(md, inc, azi, units='oilfield'):
    inc_rad = list()
    azi_rad = list()

    if units is 'SI' or 'Metric':
        inc_rad = inc
        azi_rad = azi
    else:
        for i in range(0, 2):
            inc_rad.append(Units.to_si(inc[i], 'dega'))
            azi_rad.append(Units.to_si(azi[i], 'dega'))

    # psi = 2 * m.acos(m.sqrt(1 + m.cos(inc_rad[0]) * m.cos(inc_rad[1]) + m.sin(inc_rad[0]) * m.sin(inc_rad[1])
    #                         * m.cos(m.fabs(azi_rad[1] - azi_rad[0]) / 2)))
    #
    # tvd = md * m.tan(psi / 2) / psi * (m.cos(inc_rad[0]) + m.cos(inc_rad[1]))
    # north = md * m.tan(psi / 2) / psi * (m.cos(inc_rad[0]) + m.cos(inc_rad[1]))
    # east = md * m.tan(psi / 2) / psi * (m.cos(inc_rad[0]) + m.cos(inc_rad[1]))
    # if Units is 'oilfield':
    #     dls = Units.convert(psi, 'rad', 'deg') * 100.0 / md
    # else:
    #     dls = psi * 30.0 / md

    beta = m.acos(m.cos(inc_rad[1] - inc_rad[0]) - (m.sin(inc_rad[0]) * m.sin(inc_rad[1])
                                                    * (1 - m.cos(azi_rad[1] - azi_rad[0]))))

    if beta == 0.0:
        north, east, tvd, dls = 0, 0, md, 0
    else:
        ratio = 2.0 / beta * m.tan(beta / 2.0)
        north = md * ratio / 2.0 * (m.sin(inc_rad[0]) * m.cos(azi_rad[0]) + m.sin(inc_rad[1]) * m.cos(azi_rad[1]))
        east = md * ratio / 2.0 * (m.sin(inc_rad[0]) * m.sin(azi_rad[0]) + m.sin(inc_rad[1]) * m.sin(azi_rad[1]))
        tvd = md * ratio / 2.0 * (m.cos(inc_rad[0]) + m.cos(inc_rad[1]))
        if units is 'oilfield':
            dls = Units.from_si(beta, 'dega') * 100.0 / md
        else:
            dls = beta * 30.0 / md

    return tvd, north, east, dls


def buildturn_rate(angle0, angle1, delta_md, units='oilfield'):
    delta_angle = angle1 - angle0
    if units is 'oilfield':
        rate = delta_angle * 100 / delta_md
    else:
        rate = delta_angle * 30 / delta_md

    return rate


def add(item0, item1):
    return item0 + item1