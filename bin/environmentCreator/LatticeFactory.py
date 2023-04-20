from bin.environmentCreator.InputReader import InputReader
import numpy as np


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
                    self.atoms[atom[1]] = [atom[0], atom[2], atom[3], unique_id + counter]
                    counter += 1
            else:
                self.atoms[atom[1]] = [atom[0], atom[2], atom[3], unique_id + counter]
                counter += 1


class LatticeFactory:
    def __init__(self, inputs: InputReader, simBoxLength: int):
        mode = "simprepLegacy"

        self.latticeParameterA = inputs.structureRaw[0][0]
        self.latticeParameterB = inputs.structureRaw[0][1]
        self.latticeParameterC = inputs.structureRaw[0][2]
        self.simBoxLength = simBoxLength
        self.sites = inputs.structureRaw[2].values

        self.simBox = np.ndarray((simBoxLength, simBoxLength, simBoxLength), dtype=Cell)

        if mode == "simprepLegacy":
            for i in range(self.simBoxLength):
                for j in range(self.simBoxLength):
                    for k in range(self.simBoxLength):
                        self.simBox[i][j][k] = Cell(self.sites, 1, i, j, k, self.simBoxLength)

