from bin.environmentCreator.InputReader import InputReader
import numpy as np
from math import floor

class Cell:
    def __init__(self, atomsInCell, onlyMag, i, j, k, L):
        self.atoms = {}
        self.amount = 0
        for atom in atomsInCell:
            if onlyMag:
                if atom[3]:
                    self.amount += 1
            else:
                self.amount += 1

        self.i = i
        self.j = j
        self.k = k
        unique_id = self.amount * (L * L * i + L * j + k)
        counter = 0
        for atom in atomsInCell:
            if onlyMag:
                if atom[3]:
                    # atom[1] = type, atom[0] = handle, atom[2] = tau, unique identifier, current index
                    self.atoms[atom[1]] = [atom[0], atom[2], atom[3], unique_id + counter, counter]
                    counter += 1
            else:
                self.atoms[atom[1]] = [atom[0], atom[2], atom[3], unique_id + counter, num]
                counter += 1


class LatticeFactory:
    def __init__(self, inputs: InputReader, simBoxLength: int):
        mode = "simprepLegacy"

        self.Jijs = inputs.Jijs.values.tolist()
        self.latticeParameterA = inputs.structureRaw[0][0]
        self.latticeParameterB = inputs.structureRaw[0][1]
        self.latticeParameterC = inputs.structureRaw[0][2]
        self.unitVectorA = self.latticeParameterA * inputs.structureRaw[1].values[0]
        self.unitVectorB = self.latticeParameterB * inputs.structureRaw[1].values[1]
        self.unitVectorC = self.latticeParameterC * inputs.structureRaw[1].values[2]
        self.simBoxLength = simBoxLength
        self.sites = inputs.structureRaw[2].values

        self.simBox = np.ndarray((simBoxLength, simBoxLength, simBoxLength), dtype=Cell)

        if mode == "simprepLegacy":
            for i in range(self.simBoxLength):
                for j in range(self.simBoxLength):
                    for k in range(self.simBoxLength):
                        self.simBox[i][j][k] = Cell(self.sites, 1, i, j, k, self.simBoxLength)

            firstcell = self.simBox[0][0][0]
            for i, element in enumerate(self.Jijs):
                source = element[0]
                dx,dy,dz = tuple(element[7:10])

                tau_source = firstcell.atoms[source][1]
                xyz_source = self.unitVectorA * tau_source[0] + self.unitVectorB * tau_source[1] + self.unitVectorC * tau_source[2]
                xyz_target = np.array([xyz_source[0] + dx, xyz_source[1] + dy, xyz_source[2] + dz])

                # Create the matrix with A, B, and C as columns
                ABC_matrix = np.column_stack((self.unitVectorA, self.unitVectorB, self.unitVectorC))

                # Invert the matrix
                inv_ABC_matrix = np.linalg.inv(ABC_matrix)

                # Calculate the (j, k, l) vector
                jkl = np.matmul(inv_ABC_matrix, xyz_target)
                rel_cell_x, rel_cell_y, rel_cell_z = (floor(x_target/self.latticeParameterA), floor(y_target/self.latticeParameterB), floor(z_target/self.latticeParameterC))
                self.Jijs[i].append(0)
                self.Jijs[i].append(0)
                self.Jijs[i].append(0)
                self.Jijs[i].append(rel_cell_x)
                self.Jijs[i].append(rel_cell_y)
                self.Jijs[i].append(rel_cell_z)
