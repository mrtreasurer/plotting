import os
import pathlib
import numpy as np

import parsers as psr

from matplotlib import pyplot as plt

colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = ["solid", "dashed", "dotted", "dashdot", (0, (1, 10)), (0, (3, 5, 1, 5, 1, 5))]
figures = []

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

benchmark_time = []
benchmark_error = []
for i in [1, 2]:
    benchmark_data = psr.read_file(root / f"benchmarks/benchmarkStateDifference_{i}.dat", "\t")
    benchmark_time.append(benchmark_data[:, 0])
    benchmark_error.append(np.linalg.norm(benchmark_data[:, 1:4], axis=1))

propagators = ["cowell", "encke", "gauss me", "usm quaternions", "usm mrp", "usm em"]
integrators = ["RKF45", "RKF56", "RKF78", "RK87 DP", "RK4"]
settings = [10**-10, 10**-9, 10**-8, 10**-7]
rk4_settings = [1, 2, 4, 8, 16, 32]

props = len(propagators)
ints = len(integrators)
sets = len(settings)

for i in range(props):
    fig, ax = plt.subplots(num=i)
    figures.append((fig, ax))

    fig.figsize = (10, 6)
    fig.dpi = 400

    ax.set_title(f"{propagators[i].capitalize()} Propagator")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Position Error [m]")
    ax.grid(True, axis="y", which="major")

    for j in range(2):
        ax.semilogy(benchmark_time[j][:-1], benchmark_error[j][:-1], "k--", label="benchmark", linewidth=1)

list_dir = os.listdir(root)
list_dir.remove("benchmarks")

for dir1 in list_dir:
    for dir2 in os.listdir(root / dir1):
        for dir3 in os.listdir(root / dir1 / dir2):
                path = root / dir1 / dir2 / dir3

                i = int(dir1[-1])
                j = int(dir2[-1])
                k = int(dir3[-1])

                try:
                    success = psr.read_succesfull(path / "propagationSuccesfull.dat")

                except FileNotFoundError:
                    success = False

                s = settings
                if j == 0:
                    s = rk4_settings

                if success:
                    if k < 4:
                        state_data = psr.read_file(path / "stateDifferenceBenchmark.dat", "\t")
                        error = np.linalg.norm(state_data[:-1, 1:4], axis=1)

                        fig, ax = figures[i]
                        ax.semilogy(state_data[:-1, 0], error, label=f"{integrators[j]}, {s[k]}", color=colours[j], linestyle=linestyles[k], linewidth=1)

for i, (fig, ax) in enumerate(figures):
    ax.legend(prop={"size": 8})
    fig.savefig(f"figures/prop{i}")

# plt.show()
