import numpy as np


def read_file(path, separator):
    with open(path, "r") as f:
        readout = f.readlines()

        if separator == " ":
            data = _parse_space_separated(readout)

        elif separator == "\t":
            data = _parse_tab_separated(readout)

        else:
            raise ValueError("No parsing function for delimiter")
    
    return data


def _parse_space_separated(readout):
    space = " "
    data = []

    for row in readout:
        row_list = row.split(space)

        while space in row:
            row_list.remove(space)
        
        f_row_list = []
        for s in row_list:
            f_row_list.append(float(s))

        data.append(f_row_list)

    return np.array(data)


def _parse_tab_separated(readout):
    return np.genfromtxt(readout, delimiter="\t")