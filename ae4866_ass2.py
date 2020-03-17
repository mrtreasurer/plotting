import numpy as np
import os
import pathlib

from matplotlib import pyplot as plt

import parsers as psr
import ae4866.definitions as d

from constants import colours, linestyles, markers


root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscentAccelerationEnvironment")

fig, ax = plt.subplots()
fig.set_size_inches(10, 5)

legend_entries = ["GLGM (6,6)", "Earth perturbation"]

runs = []
for i in range(len(os.listdir(root))):
    data = psr.read_file(root / f"{i}/stateHistory.dat", "\t")
    runs.append(data)
    
t = runs[0][:, 0]
r0 = runs[0][:, 1:4]
v0 = runs[0][:, 4:7]

for i, run in enumerate(runs[1::]):
    r = run[:, 1:4]
    v = run[:, 4:7]

    err_r = np.linalg.norm(r0 - r, axis=1)/1000
    err_v = np.linalg.norm(v0 - v, axis=1)

    ax.plot(t, err_r, label=f"dr {legend_entries[i-1]} [km]", color=colours[i-1], linestyle=linestyles[0])
    ax.plot(t, err_v, label=f"dv {legend_entries[i-1]} [m/s]", color=colours[i-1], linestyle=linestyles[1])

ax.legend()
ax.set_title("Environment changes")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Difference")
ax.grid(True, axis="y")
plt.savefig("figures_ae4866/environment")

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscentParameterUncertainty")

fig, ax = plt.subplots()
fig.set_size_inches(6, 5)

runs = []
for i in range(len(os.listdir(root))):
    pert = d.read_number(root / f"{i}/parameterPerturbation.dat")
    pos = psr.read_file(root / f"{i}/stateHistory.dat", "\t")

    runs.append((pert, pos))

r0 = runs[0][1][-1, 1:4]

for i, run in enumerate(runs):
    pert = run[0]
    r = run[1][-1, 1:4]

    dr = np.linalg.norm(r0 - r)

    ax.plot(pert, dr, marker=".", color=colours[0])

ax.set_title(r"Position difference as function of perturbation to $\mu$")
ax.set_xlabel("Perturbation [km3/s2]")
ax.set_ylabel("Position difference [m]")
plt.savefig("figures_ae4866/parameters")

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscentAssignmentStateUncertainty")

fig, ax = plt.subplots()
fig.set_size_inches(6, 5)

fig2, ax2 = plt.subplots()
fig2.set_size_inches(6, 5)

fig3, ax3 = plt.subplots()
fig3.set_size_inches(6, 5)

fig4, ax4 = plt.subplots()
fig4.set_size_inches(6, 5)

runs = []
for i in range(len(os.listdir(root))):
    pert = psr.read_file(root / f"{i}/statePerturbation.dat", "\t")[:, 1]
    pos = psr.read_file(root / f"{i}/stateHistory.dat", "\t")

    runs.append((pert, pos))

r0 = runs[0][1][-1, 1:4]
f0 = runs[0][1][-1, -1]

for i, run in enumerate(runs):
    pert = run[0]
    r = run[1][-1, 1:4]
    f = run[1][-1, -1]

    dr = np.linalg.norm(r0 - r)
    df = f0 - f

    for j, p in enumerate(pert):
        if p != 0:
            if j < 3:
                a = ax
                b = ax3
            else:
                a = ax2
                b = ax4

            a.plot(p, dr, marker=".", color=colours[j])
            b.plot(p, df, marker=".", color=colours[j])

ax.set_title("Position difference as function of perturbation to initial position")
ax.set_xlabel("Perturbation [m]")
ax.set_ylabel("Position difference [m]")
fig.savefig("figures_ae4866/state1")

ax2.set_title("Position difference as function of perturbation to specific impulse")
ax2.set_xlabel("Perturbation [s]")
ax2.set_ylabel("Position difference [m]")
fig2.savefig("figures_ae4866/state2")

ax3.set_title("Fuel difference as function of perturbation to initial position")
ax3.set_xlabel("Perturbation [m]")
ax3.set_ylabel("Fuel difference [kg]")
fig3.savefig("figures_ae4866/state3")

ax4.set_title("Fuel difference as function of perturbation to specific impulse")
ax4.set_xlabel("Perturbation [s]")
ax4.set_ylabel("Fuel difference [kg]")
fig4.savefig("figures_ae4866/state4")

# plt.show()