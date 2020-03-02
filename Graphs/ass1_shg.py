import numpy as np

from gravity_spherical_harmonic import gravity_spherical_harmonic
from load_gravity_model import load_gravity_model


r, mu, c, s, n, m = load_gravity_model("X:/Git/pykep/pykep/util/gravity_models/Moon/grgm_1200a_t.txt")

lat = np.radians(0.6875)
lon = np.radians(23.4333)

# x = (r + 100) * np.array([[np.cos(lat)*np.sin(lon), np.cos(lat)*np.cos(lon), np.sin(lat)]])

# acc0 = gravity_spherical_harmonic(x, r, mu, c, s, 0, 0)
# acc1 = gravity_spherical_harmonic(x, r, mu, c, s, 500, 500)

# n_acc0 = np.linalg.norm(acc0)
# n_acc1 = np.linalg.norm(acc1)

# print(n_acc0, n_acc1, (n_acc0-n_acc1)/n_acc0)

isp = 311
g0 = 9.80665
m0 = 2759.424635848819
m1 = 2250

dv = isp*g0*np.log(m0/m1)
print(dv)

xf = np.array([1008965.648223693, 1534057.146672293, 68582.04673224296])
vf = np.array([868.8323325342774, -169.7202740381948, 20.52541892045531])
vfn = np.linalg.norm(vf)
print(vfn)

vr = np.dot(xf, vf)/np.linalg.norm(xf)**2 * xf
vrn = np.linalg.norm(vr)
print(vrn)

print(np.sqrt(vfn**2 - vrn**2))
