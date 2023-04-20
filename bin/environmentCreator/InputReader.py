import pandas as pd
import os

def read_raw_Jrs(file_path):
    data = []

    with open(file_path, 'r') as file:
        for line in file:
            # Ignore lines starting with "#"
            if line.strip().startswith("#"):
                continue

            # Split line into elements using whitespace as delimiter
            elements = line.split()

            # Convert elements to appropriate data types (integer, string, or float)
            row = []
            for element in elements:
                try:
                    value = int(element)
                except ValueError:
                    try:
                        value = float(element)
                    except ValueError:
                        value = element
                row.append(value)

            data.append(row)

    # Convert the list of rows to a pandas DataFrame
    df = pd.DataFrame(data)

    return df


def read_structure_file(file_path):
    alat_blat_clat = None
    rb = []
    atomic_positions = []
    breakcondition = 0

    with open(file_path, 'r') as file:
        section = None
        for line in file:
            if "3D unit cell" in line:
                alat_blat_clat = tuple(line.split()[3:6])
                temp = []
                for elem in alat_blat_clat:
                    temp.append(elem.split("=")[1])
                alat_blat_clat = tuple(map(float, temp))
                section = 'unit_cell'
                continue
            elif "atomic positions" in line:
                section = 'atomic_positions'
                continue
            elif line.startswith('-') or not line.strip():
                if section == 'atomic_positions':
                    if breakcondition:
                        break
                    else:
                        breakcondition = 1
                        continue
                else:
                    continue

            if section == 'unit_cell':
                if 'scale' in line:
                    temp = []
                    for elem in line.split()[0:3]:
                        temp.append(elem.split("=")[-1])
                    rb.append(list(map(float, temp)))
            elif section == 'atomic_positions':
                elements = line.split()
                name = elements[1]
                dtype = int(elements[2].split("=")[-1])
                tau = tuple(map(float, elements[5:8]))
                mag = True if int(elements[10].split("=")[-1]) > 0 else False
                atomic_positions.append([name, dtype, tau, mag])

    rb_matrix = pd.DataFrame(rb)
    atomic_positions_df = pd.DataFrame(atomic_positions, columns=['name', 'type', 'tau', 'mag'])

    return alat_blat_clat, rb_matrix, atomic_positions_df


class InputReader:
    def __init__(self, path: str):
        self.Jijs = read_raw_Jrs(os.path.join(path, "tmp_jrs.dat"))
        self.structureRaw = read_structure_file(os.path.join(path, "file.str"))


