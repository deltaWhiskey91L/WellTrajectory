from Utilities import mylogging
import os

try:
    import pandas as pd
except ModuleNotFoundError:
    mylogging.runlog.warn('Import: pandas module not found.')
    import csv
    __pandas = False
else:
    __pandas = True

root_path = os.path.dirname(os.path.realpath(__file__))


def complete_survey(file=root_path + '/Data/original_survey.csv', return_dataframe=False):
    mylogging.runlog.info('Read: Survey File')
    if __pandas is True:
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
    else:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            lines = list(reader)
        lines.pop(0)

        md, tvd, ns, ew, section = list(), list(), list(), list(), list()
        dls, build, turn, rugosity = list(), list(), list(), list()
        for line in lines:
            md.append(float(line[0])), tvd.append(float(line[3])), ns.append(float(line[4])), ew.append(float(line[5]))
            section.append(float(line[6])), dls.append(float(line[7])), build.append(float(line[8]))
            turn.append(float(line[9])), rugosity.append(float(line[10]))
        return md, tvd, ns, ew, section, dls, build, turn, rugosity


def survey(file=root_path + '/Data/original_survey.csv', return_dataframe=False):
    mylogging.runlog.info('Read: Survey File')
    if __pandas is True:
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
    else:
        with open(file, 'r') as f:
            reader = csv.reader(f)
            lines = list(reader)
        lines.pop(0)

        md, inc, azi = list(), list(), list()
        for line in lines:
            md.append(float(line[0])), inc.append(float(line[1])), azi.append(float(line[2]))
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

