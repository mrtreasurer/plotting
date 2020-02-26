import pathlib

from matplotlib import pyplot as plt

import parsers as psr


root = pathlib.Path("X:/Git/tudatBundle/tudatApplications/po2020/SimulationOutput/LunarAscent").resolve()

data = psr.read_file(root / "prop_0/int_0/setting_0/dependentVariables.dat", "\t")

plt.plot(data[:, 0], data[:, 1])

plt.show()