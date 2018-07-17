from Utilities import unitconverter as units
from Survey import Ellipsoid
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from numpy import linalg as la
import sys


print(np.sin(1.38212623))
print(np.cos(4.97418837))
print(np.sin(1.38212623)*np.cos(4.97418837))
sys.exit()

locations = [[33, 31.70747099, -102.158939],
             [34, 31.70749399, -102.1588459],
             [35, 31.70751594, -102.1587531],
             [36, 31.70753926, -102.1586602]]

locations_xy = [[0, 0],
                [33.98, 8.39],
                [67.84, 16.4],
                [101.74, 13.76]]

radius = 6373146  # meters

x = []
y = []
r = []
for i in range(1, 4):
    x.append(np.radians(locations[i][2] - locations[0][2]) * radius)
    y.append(np.radians(locations[i][1] - locations[0][1]) * radius)
    r.append(np.sqrt(locations_xy[i][0]**2 + locations_xy[i][1]**2))

x = np.array(x)
y = np.array(y)
print(units.from_si(x, 'ft'))
print(units.from_si(y, 'ft'))
print(np.degrees(np.arctan(y/x)))
print(np.round(units.from_si(r, 'ft'), 2))

print(90 - np.degrees(np.arctan(y[-1] / x[-1])))
sys.exit()
# ell = Ellipse((0, 0), 4, 2, 0)
# print(ell)
# a = plt.subplot(111, aspect='equal')
# ell.set_clip_box(a.bbox)
# ell.set_alpha(0.1)
# a.add_artist(ell)
#
# plt.xlim(-2, 2)
# plt.ylim(-1, 1)
# plt.show()

N = np.linspace(-5, 5, 1000)
E = np.linspace(-5, 5, 1000)
V = np.linspace(-5, 5, 1000)

inc = 90
azi = 90
std = np.array([[2], [1], [1]])
U = Ellipsoid.unit_matrix(inc, azi)
S = Ellipsoid.sigma_matrix(std)

X = np.array([0, 2, 0])
A = np.dot(np.dot(U, S**2), U.T)

print(std)
print(U)
print(np.dot(U, std))
# print(X.T)
# print('U =', np.round(U, 2))
# print(S * U.T)
print(np.dot(np.dot(X.T, A), X))

print(np.average(np.array([340.5, 343.7, 348.7, 353.1])))


from scipy.stats import norm
m1 = 0
std1 = 1
m2 = 2.5
std2 = 0.8
pts = Ellipsoid.intersect(m1, m2, std1, std2)
ovl = Ellipsoid.ovl(m1, m2, std1, std2)

x = np.linspace(-5, 15, 10000)
plot1 = plt.plot(x, norm.pdf(x, m1, std1), label='m1')
plot2 = plt.plot(x, norm.pdf(x, m2, std2), label='m2')
plot3 = plt.plot(pts, norm.pdf(pts, m1, std1), 'o')
plt.text((x[-1] - x[0]) * 0.4 + x[0], 0.4, r'OVL = ' + str(np.round(ovl * 100, 2)) + r' %')
plt.legend()
plt.show()
