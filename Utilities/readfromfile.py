from Utilities import mylogging
import pandas as pd
import os

root_path = os.path.dirname(os.path.realpath(__file__))


def complete_survey(file=root_path + '/Data/original_survey.csv', return_dataframe=False):
    mylogging.runlog.info('Read: Survey File')
    try:
        df = pd.read_csv(file, delimiter=',', header=0, dtype=float)
    except FileNotFoundError:
        mylogging.runlog.error('Read: {0} file not found.'.format(file))
        raise FileNotFoundError
    except Exception:
        mylogging.runlog.error('Read: Error reading {0} file.'.format(file))
        raise ValueError
    if return_dataframe is True:
        return df

    md = df.MD.values
    tvd = df.TVD.values
    ns = df.NS.values
    ew = df.EW.values
    section = df.Section.values
    dls = df.DLS.values
    build = df.Build.values
    turn = df.Turn.values
    rugosity = df.Rugosity.values
    return md, tvd, ns, ew, section, dls, build, turn, rugosity


def survey(file=root_path + '/Data/original_survey.csv', return_dataframe=False):
    mylogging.runlog.info('Read: Survey File')
    try:
        df = pd.read_csv(file, delimiter=',', header=0)
    except FileNotFoundError:
        mylogging.runlog.error('Read: {0} file not found.'.format(file))
        raise FileNotFoundError
    except Exception:
        mylogging.runlog.error('Read: Error reading {0} file.'.format(file))
        raise ValueError
    if return_dataframe is True:
        return df

    md = df.MD.values
    inc = df.Inc.values
    azi = df.Azi.values
    return md, inc, azi


def error_model(file=root_path + '/Data/ErrorModel.txt'):
    mylogging.runlog.info('Read: Error Model File')
    try:
        df = pd.read_csv(file, delimiter=',', header=0, names=['Name', 'Unit', 'Magnitude', 'Distribution'])
    except FileNotFoundError:
        mylogging.runlog.error('Read: {0} file not found.'.format(file))
        raise FileNotFoundError
    except Exception:
        mylogging.runlog.error('Read: Error reading {0} file.'.format(file))
        raise ValueError

    return df

