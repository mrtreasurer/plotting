import os
import pathlib
import numpy as np

import parsers as psr

from matplotlib import pyplot as plt

root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

plt.figure(1)
plt.title("Benchmark position error")
plt.xlabel("Time [s]")
plt.ylabel("Position error [m]")
plt.minorticks_on()
plt.grid(True, axis="y", which="both")


for i in [1, 2]:
    benchmark_data = psr.read_file(root / f"benchmarks/benchmarkStateDifference_{i}.dat", "\t")

    time_stamp = benchmark_data[:, 0]
    benchmark_pos = benchmark_data[:, 1:4]

    benchmark_pos_diff = np.linalg.norm(benchmark_pos, axis=1)

    plt.semilogy(time_stamp[:-1], benchmark_pos_diff[:-1], label={f"Benchmark {i}"})

list_dir = os.listdir(root)
list_dir.remove("benchmarks")

for dir1 in list_dir:
    for dir2 in os.listdir(root / dir1):
        for dir3 in os.listdir(root / dir1 / dir2):
                path = root / dir1 / dir2 / dir3

                try:
                    success = psr.read_succesfull(path / "propagationSuccesfull.dat")

                except FileNotFoundError:
                    success = False

                print(success)

                if success:
                    state_data = psr.read_file(path / "stateDifferenceBenchmark.dat", "\t")
                    error = np.linalg.norm(state_data[:, 1:4], axis=1)

                    if dir2 == "int_0" and dir3 == "setting_0":
                        # propagators for one setting
                        plt.figure(2)
                        plt.semilogy(state_data[:, 0], error)

                    if dir2 == "int_0" and dir3 == "setting_1":
                        # propagators for one setting
                        plt.figure(3)
                        plt.semilogy(state_data[:, 0], error)

                    if dir1 == "prop_0" and dir3 == "setting_0":
                        
                        plt.figure(4)
                        plt.semilogy(state_data[:, 0], error)

plt.show()
