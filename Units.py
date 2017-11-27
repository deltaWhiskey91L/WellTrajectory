import datetime
import logging
from lxml import etree
import os
import sys

# LOGGING
root_path = os.path.dirname(os.path.realpath(__file__))
logging.basicConfig(filename=root_path + '/Logs/run.log', level=logging.DEBUG)
# Logging Levels:
# CRITICAL
# ERROR
# WARNING
# INFO
# DEBUG


class Energistics:
    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.file = self.path + '/Input Files/Units.xml'
        self.namespace = 'http://www.energistics.org/energyml/data/uomv1'
        try:
            self.document = etree.parse(self.file)
        except:
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.critical('{0} CRITICAL: Units.xml file is missing or has critical bug.'.format(t))
            sys.exit()
        self.root = self.document.getroot()

    def prefix(self, value, prefix_from=None, prefix_to=None):
        prefixSet = self.root.find('a:prefixSet', namespaces={'a': self.namespace})

        def multiplier(symbol):
            try:
                return float(prefixSet.xpath(".//*[a:symbol='%s']/./a:multiplier" % symbol,
                                             namespaces={'a': self.namespace})[0].text)
            except IndexError:
                t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                logging.error('{0} ERROR: Units.xml missing {1} prefix.'.format(t, symbol))
                return 1.

        if prefix_from is None:
            multiplier_from = 1.
        else:
            multiplier_from = multiplier(prefix_from)

        if prefix_to is None:
            multiplier_to = 1.
        else:
            multiplier_to = multiplier(prefix_to)

        return value * multiplier_from / multiplier_to

    def all_unit_symbols(self):
        unitSet = self.root.find('a:unitSet', namespaces={'a': self.namespace})
        symbols = unitSet.xpath(".//a:symbol", namespaces={'a': self.namespace})
        all_symbols = list()
        i = 0
        while True:
            try:
                all_symbols.append(symbols[i].text)
            except:
                break
            i += 1
        return all_symbols

    def convert(self, value, unit_from, unit_to):
        unitSet = self.root.find('a:unitSet', namespaces={'a': self.namespace})

        if Energistics.is_unit(self, unit_from) is False:
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.error('{0} ERROR: {1} is not a formally defined unit.'.format(t, unit_from))
            raise ValueError

        if Energistics.is_unit(self, unit_to) is False:
            t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
            logging.error('{0} ERROR: {1} is not a formally defined unit.'.format(t, unit_to))
            raise ValueError

        def unit_to_base(a, b, c, d, unit_value):
            try:
                return (a + b * unit_value) / (c + d * unit_value)
            except ZeroDivisionError:
                t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                logging.critical('{0} CRITICAL: Divide by zero error during unit conversion.'.format(t))
                return unit_value

        def base_to_unit(a, b, c, d, base_value):
            try:
                return (c * base_value - a) / (b - d * base_value)
            except ZeroDivisionError:
                t = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
                logging.critical('{0} CRITICAL: Divide by zero error during unit conversion.'.format(t))
                return base_value

        if Energistics.is_base(self, unit_from) is True:
            A1, B1, C1, D1 = 0, 1, 1, 0
        else:
            A1 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:A" % unit_from, namespaces={'a': self.namespace})[0].text)
            B1 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:B" % unit_from, namespaces={'a': self.namespace})[0].text)
            C1 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:C" % unit_from, namespaces={'a': self.namespace})[0].text)
            D1 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:D" % unit_from, namespaces={'a': self.namespace})[0].text)

        if Energistics.is_base(self, unit_to) is True:
            A2, B2, C2, D2 = 0, 1, 1, 0
        else:
            A2 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:A" % unit_to, namespaces={'a': self.namespace})[0].text)
            B2 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:B" % unit_to, namespaces={'a': self.namespace})[0].text)
            C2 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:C" % unit_to, namespaces={'a': self.namespace})[0].text)
            D2 = float(unitSet.xpath(".//*[a:symbol='%s']/./a:D" % unit_to, namespaces={'a': self.namespace})[0].text)
        return base_to_unit(A2, B2, C2, D2, unit_to_base(A1, B1, C1, D1, value))

    def is_unit(self, unit):
        unitSet = self.root.find('a:unitSet', namespaces={'a': self.namespace})
        unit = unitSet.xpath(".//*[a:symbol='%s']" % unit, namespaces={'a': self.namespace})
        if len(unit) is not 0:
            return True
        else:
            return False

    def is_base(self, unit):
        unitSet = self.root.find('a:unitSet', namespaces={'a': self.namespace})
        element = unitSet.xpath(".//*[a:symbol='%s']/./a:isBase" % unit, namespaces={'a': self.namespace})
        if len(element) is not 0:
            return True
        else:
            return False

    def is_same_base(self, unit_from, unit_to):
        unitSet = self.root.find('a:unitSet', namespaces={'a': self.namespace})
        if Energistics.is_base(self, unit_from) is True:
            base_from = unit_from
        else:
            base_from = unitSet.xpath(".//*[a:symbol='%s']/./a:baseUnit" % unit_from,
                                     namespaces={'a': self.namespace})[0].text
        if Energistics.is_base(unit_to) is True:
            base_to = unit_to
        else:
            base_to = unitSet.xpath(".//*[a:symbol='%s']/./a:baseUnit" % unit_to,
                                   namespaces={'a': self.namespace})[0].text
        return base_from == base_to


test = Energistics()
print(Energistics.prefix(test, 1., None, 'k'))
print('Total Number of Units: ' + str(len(Energistics.all_unit_symbols(test))))
unitFrom = 'm'
unitTo = 'ft'
testVal = 100
print(datetime.datetime.now())
print('There are {0} {1} per {2} {3}.'.format(Energistics.convert(test, testVal, unitFrom, unitTo), unitTo, testVal, unitFrom))
print(datetime.datetime.now())
