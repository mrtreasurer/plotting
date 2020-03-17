import os
import pathlib
import numpy as np

from matplotlib import pyplot as plt

import parsers as psr
import ae4866.definitions as d

colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = ["solid", "dotted", "dashdot"]
markers = ["o", "^", "s"]
figures = []

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

benchmark_time = []
benchmark_error = []
for i in [1, 2]:
    benchmark_data = psr.read_file(root / f"benchmarks/benchmarkStateDifference_{i}.dat", "\t")
    benchmark_time.append(benchmark_data[:, 0])
    benchmark_error.append(np.linalg.norm(benchmark_data[:, 1:4], axis=1))

propagators = ["cowell", "encke", "gauss kepl", "gauss me", "usm q", "usm mrp", "usm em"]
integrators = ["RKF45", "RKF56", "RKF78", "RK87 DP", "RK4", "BS", "ABM"]
# settings = [10**-10, 10**-9, 10**-8, 10**-7]
settings = [10**-8, 10**-7, 10**-6, 10**-5]
rk4_settings = [1, 2, 4, 8, 16, 32]

props = len(propagators)
ints = len(integrators)
sets = len(settings)

for i in range(2*(props + ints)):
    fig, ax = plt.subplots(num=i)
    figures.append((fig, ax))

    fig.figsize = (10, 6)
    fig.dpi = 400

    if i%(props + ints) < props:
        ax.set_title(f"{propagators[i%(props + ints)].capitalize()} Propagator")
    else:
        ax.set_title(f"{integrators[(i - props)%(props + ints)]} Integrator")

    if i < props + ints:
        ax.set_xlabel("Time [s]")
        ax.set_ylabel("Position Error [m]")
        ax.grid(True, axis="y", which="major")

    else:
        ax.set_xlabel("Number of function evaluations [-]")
        ax.set_ylabel("Maximum Error [m]")
        ax.grid(True, axis="both", which="major")

    if i < props + ints:
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
                    success = d.read_succesfull(path / "propagationSuccesfull.dat")

                except FileNotFoundError:
                    success = False

                if j == 4:
                    s = f" step {rk4_settings[k]}s"

                else:
                    s = f"tol {settings[k]}"

                if success:
                    if k%2 == 0:
                        state_data = psr.read_file(path / "stateDifferenceBenchmark.dat", "\t")
                        error = np.linalg.norm(state_data[:-1, 1:4], axis=1)

                        _, ax = figures[i]
                        ax.semilogy(state_data[:-1, 0], error, label=f"{integrators[j]}, {s}", color=colours[j], linestyle=linestyles[k//2], linewidth=1)

                        _, ax = figures[props + j]
                        ax.semilogy(state_data[:-1, 0], error, label=f"{propagators[i].capitalize()}, {s}", color=colours[i], linestyle=linestyles[k//2], linewidth=1)

                        evals = d.read_evaluations(path / "numberOfFunctionEvaluations.dat")
                        max_error = max(error)

                        _, ax = figures[props + ints + i]
                        ax.semilogy(evals, max_error, label=f"{integrators[j]}, {s}", color=colours[j], marker=markers[k//2], linestyle=None)

                        # if not ((i not in [0, 1]) and (j == 3) ):
                        _, ax = figures[2*props + ints + j]
                        ax.semilogy(evals, max_error, label=f"{propagators[i].capitalize()}, {s}", color=colours[i], marker=markers[k//2], linestyle=None)

for i, (fig, ax) in enumerate(figures):
    loc = "lower right"
    if i >= props + ints:
        loc = "upper right"
    
    ax.legend(loc=loc, prop={"size": 8})

    if i%(props + ints) < props:
        name = "prop_"
    else:
        name = "int_"

    if i < props + ints:
        name += "acc_"
    else:
        name += "time_"

    j = i
    if i >= props + ints:
        j = j%(props + ints)

    if i >= props:
        j = j%props

    fig.savefig(f"figures_5/{name}{j}")
    plt.close(fig)

# plt.show()
