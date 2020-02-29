import os
import pathlib
import numpy as np

import parsers as psr

from matplotlib import pyplot as plt

colours = plt.rcParams['axes.prop_cycle'].by_key()['color']
linestyles = ["solid", "dotted", "dashdot", (0, (1, 10))]
markers = ["o", "^", "s"]
figures = []

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

def get_benchmark_comp(path, success=False, which="pos"):

    if not success:
        success = get_successful(path.parent)

    if success:
        data = psr.read_file(path, "\t")
        time = data[:-1, 0]

        if which == "pos":
            error = np.linalg.norm(data[:-1, 1:4], axis=1)

        elif which == "vel":
            error = np.linalg.norm(data[:-1, 4:7], axis=1)

        else:
            raise ValueError(f"wrong value for which: {which}")

        return time, error

    else:
        return 0, 0


def get_max_error(path, **kwargs):
    time, error = get_benchmark_comp(path, **kwargs)

    if type(time) == np.ndarray:
        return time, max(error)
    
    else:
        return time, error


def get_successful(path):
    try:
        success = psr.read_succesfull(path / "propagationSuccesfull.dat")

    except FileNotFoundError:
        success = False

    return success


def get_evals(path):
    success = get_successful(path)
    
    if success:
        return psr.read_evaluations(root / get_relpath(p, 3, s) / "numberOfFunctionEvaluations.dat")

    else:
        return 0


def get_relpath(p, i, s):
    return f"prop_{p}/int_{i}/setting_{s}"


def plot_benchmark(ax, benchmarks, which="pos"):
    index = 1
    if which == "vel":
        index = 2

    if which not in ["pos", "vel"]:
        raise ValueError(f"wrong value for which: {which}")

    for j in range(len(benchmarks)):
        ax.semilogy(benchmarks[j][0], benchmarks[j][index], "k--", label=f"benchmark {j+1}", linewidth=1)


def apply_settings(fig, mode=1):
    if mode == 1:
        fig.set_figwidth(10)
        fig.set_figheight(5)

    elif mode == 2:
        pass

    else:
        raise ValueError(f"wrong value for mode: {mode}")
    fig.set_dpi(600)


def settings_string(i, s):
    if i == 4:
        setting = f"step {rk4_settings[s]}s"
    else:
        setting = f"tol {settings[s]}"

    return setting


benchmarks = []
for i in [1, 2]:
    time, error = get_benchmark_comp(root / f"benchmarks/benchmarkStateDifference_{i}.dat", success=True)
    _, verror = get_benchmark_comp(root / f"benchmarks/benchmarkStateDifference_{i}.dat", success=True, which="vel")
    benchmarks.append((time, error, verror))

propagators_long = ["Cowell", "Encke", "Gauss Keplerian", "Gauss Modified Equinoctial", "Unified State Model Quaternions", "Unified State Model Modified Rodrigues Parameters", "Unified State Model Exponential Model"]
propagators = ["cowell", "encke", "gauss kepl", "gauss me", "usm q", "usm mrp", "usm em"]
integrators_long = ["Runge-Kutta-Fehlberg 45", "Runge-Kutta-Fehlberg 56", "Runge-Kutta-Fehlberg 78", "Runge-Kutta 87 Dormand-Prince", "Runge-Kutta 4", "Bulirsch-Stoer", "Adams-Bashforth-Moulton"]
integrators = ["RKF45", "RKF56", "RKF78", "RK87 DP", "RK4", "BS", "ABM"]
# settings = [10**-10, 10**-9, 10**-8, 10**-7]
# settings = [10**-8, 10**-7, 10**-6, 10**-5]
settings = [10**-8, 10**-6, 10**-4, 10**-2]
rk4_settings = [1, 2, 4, 8, 16, 32]

props = len(propagators)
ints = len(integrators)
sets = len(settings)

# propacc0
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks)

for i in range(ints):
    for s in range(2):
        time, error = get_benchmark_comp(root / get_relpath(0, i, s) / "stateDifferenceBenchmark.dat")

        setting = settings_string(i, s)

        ax.semilogy(time, error, label=f"{integrators[i]}, {setting}", color=colours[i], linestyle=linestyles[s], linewidth=1)

ax.set_title(propagators_long[0])
ax.set_xlabel("Time [s]")
ax.set_ylabel("Position Error [m]")
ax.set_xlim(xmax=800)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/propacc0")

# proptime0
fig, ax = plt.subplots()
apply_settings(fig, mode=2)
for i in range(ints):
    for s in range(2):
        _, error = get_max_error(root / get_relpath(0, i, s) / "stateDifferenceBenchmark.dat")
        evals = psr.read_evaluations(root / get_relpath(0, i, s) / "numberOfFunctionEvaluations.dat")

        setting = settings_string(i, s)

        ax.semilogy(evals, error, label=f"{integrators[i]}, {setting}", color=colours[i], marker=markers[s], linestyle=None)

ax.set_title(propagators_long[0])
ax.set_xlabel("Function Evaluations [-]")
ax.set_ylabel("Maximum Position Error [m]")
ax.grid(True, axis="y", which="major")
plt.legend(loc="upper right", prop={"size": 8})
plt.savefig("figures/proptime0")

# intacc3
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks)

for p in range(props):
    for s in range(1, 3):
        time, error = get_benchmark_comp(root / get_relpath(p, 4, s) / "stateDifferenceBenchmark.dat")
        
        if type(time) == np.ndarray:
            print(propagators[p])
            ax.semilogy(time, error, label=f"{propagators[p]}, {rk4_settings[s]}s", color=colours[p], linestyle=linestyles[s-1], linewidth=1)

ax.set_title(integrators_long[4])
ax.set_xlabel("Time [s]")
ax.set_ylabel("Position Error [m]")
ax.set_xlim(xmax=800)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/intacc3")

# inttime3
fig, ax = plt.subplots()
apply_settings(fig, mode=2)
for p in [0, 1]:
    for s in range(1, 3):
        _, error = get_max_error(root / get_relpath(p, 4, s) / "stateDifferenceBenchmark.dat")
        evals = get_evals(root / get_relpath(p, 4, s))

        if evals != 0:
            ax.semilogy(evals, error, label=f"{propagators[p]}, {rk4_settings[s]}s", color=colours[p], marker=markers[s-1], linestyle=None)

ax.set_title(integrators_long[4])
ax.set_xlabel("Function Evaluations [-]")
ax.set_ylabel("Maximum Position Error [m]")
ax.grid(True, axis="y", which="major")
plt.legend(loc="upper right", prop={"size": 8})
plt.savefig("figures/inttime3")

# q4
prop_ids = [0, 1]
int_ids = [0, 3, 4]
# root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

# q4acc
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks)

for x, p in enumerate(prop_ids):
    for y, i in enumerate(int_ids):
        for s in range(3):
            time, error = get_benchmark_comp(root / get_relpath(p, i, s) / "stateDifferenceBenchmark.dat")

            setting = settings_string(i, s)
            
            if type(time) == np.ndarray:
                ax.semilogy(time, error, label=f"{propagators[p]}, {integrators[i]}, {setting}", color=colours[len(int_ids)*x+y], linestyle=linestyles[s], linewidth=1)

ax.set_title("Combination of various integrators and propagators")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Position Error [m]")
ax.set_xlim(xmax=900)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/q4acc")

# q4time
fig, ax = plt.subplots()
apply_settings(fig, mode=2)
for x, p in enumerate(prop_ids):
    for y, i in enumerate(int_ids):
        for s in range(3):
            _, error = get_max_error(root / get_relpath(p, i, s) / "stateDifferenceBenchmark.dat")
            evals = get_evals(root / get_relpath(p, i, s))

            setting = settings_string(i, s)

            if evals != 0:
                ax.semilogy(evals, error, label=f"{propagators[p]}, {integrators[i]}, {setting}", color=colours[len(int_ids)*x+y], marker=markers[s], linestyle=None)

ax.set_title("Combination of various integrators and propagators")
ax.set_xlabel("Function Evaluations [-]")
ax.set_ylabel("Maximum Position Error [m]")
ax.grid(True, axis="y", which="major")
plt.legend(loc="upper right", prop={"size": 8})
plt.savefig("figures/q4time")

# propaccv0
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks, which="vel")

for i in range(ints):
    for s in range(2):
        time, error = get_benchmark_comp(root / get_relpath(0, i, s) / "stateDifferenceBenchmark.dat", which="vel")

        setting = settings_string(i, s)

        ax.semilogy(time, error, label=f"{integrators[i]}, {setting}", color=colours[i], linestyle=linestyles[s], linewidth=1)

ax.set_title(propagators_long[0])
ax.set_xlabel("Time [s]")
ax.set_ylabel("Velocity Error [m]")
ax.set_xlim(xmax=800)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/propaccv0")

# intaccv3
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks, which="vel")

for p in range(props):
    for s in range(1, 3):
        time, error = get_benchmark_comp(root / get_relpath(p, 4, s) / "stateDifferenceBenchmark.dat", which="vel")
        
        if type(time) == np.ndarray:
            ax.semilogy(time, error, label=f"{propagators[p]}, {rk4_settings[s]}s", color=colours[p], linestyle=linestyles[s-1], linewidth=1)

ax.set_title(integrators_long[4])
ax.set_xlabel("Time [s]")
ax.set_ylabel("Velocity Error [m]")
ax.set_xlim(xmax=800)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/intaccv3")

# q4accv
fig, ax = plt.subplots()
apply_settings(fig)
plot_benchmark(ax, benchmarks, which="vel")

for x, p in enumerate(prop_ids):
    for y, i in enumerate(int_ids):
        for s in range(3):
            time, error = get_benchmark_comp(root / get_relpath(p, i, s) / "stateDifferenceBenchmark.dat", which="vel")

            setting = settings_string(i, s)
            
            if type(time) == np.ndarray:
                ax.semilogy(time, error, label=f"{propagators[p]}, {integrators[i]}, {setting}", color=colours[len(int_ids)*x+y], linestyle=linestyles[s], linewidth=1)

ax.set_title("Combination of various integrators and propagators")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Velocity Error [m]")
ax.set_xlim(xmax=900)
ax.grid(True, axis="y", which="major")
plt.legend(loc="lower right", prop={"size": 8})
plt.savefig("figures/q4accv")