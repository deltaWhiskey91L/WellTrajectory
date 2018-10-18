import matplotlib.pyplot as plt
import os


def plot_horizontal_section(survey_list, size=None, label=None, color=None, montecarlo=False, legend=False,
                            limits=None, linestyle=None, save=False):
    root_path = os.path.dirname(os.path.dirname(__file__))
    if size is None:
        size = len(survey_list)

    if size == 1:
        plt.plot(survey_list.EW.values, survey_list.NS.values)
    else:
        if montecarlo is True:
            for i in range(0, size):
                plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color, alpha=0.02)
            plt.plot(survey_list[-1].EW.values, survey_list[-1].NS.values, c=color, label=label)
        else:
            for i in range(0, size):
                if legend is True:
                    if montecarlo is False:
                        if linestyle is None:
                            plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i], label=label[i])
                        else:
                            plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i], label=label[i],
                                     linestyle=linestyle[i])
                else:
                    if linestyle is None:
                        plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i])
                    else:
                        plt.plot(survey_list[i].EW.values, survey_list[i].NS.values, c=color[i], linestyle=linestyle[i])

    plt.grid(linestyle='dashed')
    plt.xlabel('Easting (ft)')
    plt.ylabel('Northing (ft)')
    if legend is True:
        if montecarlo is False:
            plt.legend()

    if limits is not None:
        plt.xlim([limits[0][0], limits[0][1]])
        plt.ylim([limits[1][0], limits[1][1]])

    if save is True:
        plt.savefig(root_path + '/Results/HorizontalSection.png', bbox_inches='tight')


def plot_vertical_section(survey_list, size=None, fig=None, target_azimuth=None, label=None, color=None,
                          limits=None, montecarlo=False, legend=False, linestyle=None, save=False):
    root_path = os.path.dirname(os.path.dirname(__file__))
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
                        if linestyle is None:
                            plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i], label=label[i])
                        else:
                            plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i],
                                     label=label[i], linestyle=linestyle[i])
                else:
                    if linestyle is None:
                        plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i])
                    else:
                        plt.plot(survey_list[i].Section.values, survey_list[i].TVD.values, c=color[i],
                                 linestyle=linestyle[i])

    if target_azimuth is not None:
        fig.text(.5, .86, r"Azimuth: ${0}^\circ$".format(target_azimuth), ha="center", va="center")
    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Vertical Section ' + '(ft)')
    plt.ylabel('True Vertical Depth, TVD ' + '(ft)')
    if legend is True:
        if montecarlo is False:
            plt.legend()

    if limits is not None:
        plt.xlim([limits[0][0], limits[0][1]])
        plt.ylim([limits[1][0], limits[1][1]])

    if save is True:
        plt.savefig(root_path + '/Results/VeritcalSection' + str(target_azimuth) + '.png', bbox_inches='tight')


def plot_dls(survey_list, label=None, color=None, save=False, legend=False, linestyle=None):
    root_path = os.path.dirname(os.path.dirname(__file__))
    if isinstance(survey_list, list) is True:
        size = len(survey_list)
    else:
        size = 1

    if size == 1:
        plt.plot(survey_list[7], survey_list[3])
    else:
        for i in range(0, size):
            plt.plot(survey_list[i].DLS.values, survey_list[i].MD.values, c=color[i], linestyle=linestyle[i], label=label[i])

    plt.gca().invert_yaxis()
    plt.grid(linestyle='dashed')
    plt.xlabel('Dogleg Severity (deg/100ft)')
    plt.ylabel('Measured Depth, MD (ft)')
    plt.xlim(0, 18)

    if legend is True:
        plt.legend()

    if save is True:
        plt.savefig(root_path + '/Results/DLS.png', bbox_inches='tight')


def plot_wbr(survey_list, size=1, save=False):
    root_path = os.path.dirname(os.path.dirname(__file__))
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

    if save is True:
        plt.savefig(root_path + '/Results/WBR.png', bbox_inches='tight')


