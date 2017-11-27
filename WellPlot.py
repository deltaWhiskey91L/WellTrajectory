import datetime
import logging
import os

import matplotlib.pyplot as plt

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG


def plot_horizontal_section(survey_list):
    plt.figure()
    legend = list()
    for i in range(0, len(survey_list)):
        plt.plot(survey_list[i].east, survey_list[i].north)
        legend.append(survey_list[i].well_name)

    plt.legend(legend)
    plt.grid(linestyle='dashed')
    plt.xlabel('Easting ' + '(ft)')
    plt.ylabel('Northing ' + '(ft)')
    plt.savefig(root_path + '/Results/' + 'HorizontalSection.png', bbox_inches='tight')


def plot_vertical_section(survey_list):
    plt.figure()
    legend = list()
    for i in range(0, len(survey_list)):
        plt.plot(survey_list[i].vertical_section, survey_list[i].md)
        legend.append(survey_list[i].well_name)

    plt.legend(legend)
    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Vertical Section ' + '(ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    plt.savefig(root_path + '/Results/' + 'VeritcalSection.png', bbox_inches='tight')


def plot_dls(survey_list):
    plt.figure()
    legend = list()
    for i in range(0, len(survey_list)):
        plt.plot(survey_list[i].dls, survey_list[i].md)
        legend.append(survey_list[i].well_name)

    plt.legend(legend)
    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Dogleg Severity ' + '(deg/100ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    plt.savefig(root_path + '/Results/' + 'DLS.png', bbox_inches='tight')


def plot_wbr(survey_list):
    plt.figure()
    legend = list()
    for i in range(0, len(survey_list)):
        plt.plot(survey_list[i].wbr, survey_list[i].md)
        legend.append(survey_list[i].well_name)

    plt.legend(legend)
    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Wellbore Rugosity ' + '(deg/ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.savefig(root_path + '/Results/' + 'WBR.png', bbox_inches='tight')


