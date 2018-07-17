import logging
import matplotlib.pyplot as plt
import os

root_path = os.path.dirname(os.path.realpath(__file__))
runlog = logging.getLogger('runlog')
alglog = logging.getLogger('alglog')


def plot_horizontal_section(survey_list, size=None, label=None, color=None, montecarlo=False, legend=False):
    if size is None:
        size = len(survey_list)

    if size == 1:
        pass
        # plt.plot(survey_list.EW.values, survey_list.NS.values)
    else:
        if montecarlo is True:
            for i in range(0, size):
                plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color, alpha=0.02)
            plt.plot(survey_list[-1].EW.values, survey_list[-1].NS.values, c=color, label=label)
        else:
            for i in range(0, size):
                if legend is True:
                    if montecarlo is False:
                        plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i], label=label[i])
                else:
                    plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i])

    plt.grid(linestyle='dashed')
    plt.xlabel('Easting (ft)')
    plt.ylabel('Northing (ft)')
    if legend is True:
        if montecarlo is False:
            plt.legend()
    # plt.savefig(root_path + '/Results/' + 'HorizontalSection.png', bbox_inches='tight')


def plot_vertical_section(survey_list, size=None, fig=None, target_azimuth=None, label=None, color=None, montecarlo=False, legend=False):
    if fig is None:
        fig = plt.figure()
    if size is None:
        size = len(survey_list)

    if size == 1:
        pass
        # plt.plot(survey_list.Section.values, survey_list.TVD.values)
    else:
        if montecarlo is True:
            for i in range(0, size):
                plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color, alpha=0.02)
            plt.plot(survey_list[-1].Section.values, survey_list[-1].TVD.values, c=color, label=label)
        else:
            for i in range(0, size):
                if legend is True:
                    if montecarlo is False:
                        plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i], label=label[i])
                else:
                    plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i])

    if target_azimuth is not None:
        fig.text(.47, .85, r"Azimuth: ${0}^\circ$".format(target_azimuth), ha="center", va="center")
    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Vertical Section ' + '(ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    if legend is True:
        if montecarlo is False:
            plt.legend()
    # plt.savefig(root_path + '/Results/' + 'VeritcalSection.png', bbox_inches='tight')


def plot_dls(survey_list, size=1, label=None, color=None):
    if size == 1:
        plt.plot(survey_list[7], survey_list[3])
    else:
        for i in range(0, size):
            plt.plot(survey_list[i][7], survey_list[i][3], color, alpha=0.02)
        plt.plot(survey_list[-1][7], survey_list[-1][3], color, label=label)

    # plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Dogleg Severity ' + '(deg/100ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    plt.xlim(0, 5)
    # plt.savefig(root_path + '/Results/' + 'DLS.png', bbox_inches='tight')


def plot_wbr(survey_list, size=1):
    if size == 1:
        plt.plot(survey_list[10], survey_list[3])
    else:
        for i in range(0, size):
            plt.plot(survey_list[i][10], survey_list[i][3], 'b', alpha=0.1)
        plt.plot(survey_list[-1][10], survey_list[-1][3], 'r')

    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Wellbore Rugosity ' + '(deg/100ft)')
    plt.ylabel('Measured Depth, MD ' + '(ft)')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    plt.savefig(root_path + '/Results/' + 'WBR.png', bbox_inches='tight')


