from bin.environmentCreator.LatticeFactory import LatticeFactory
from bin.environmentCreator.InputReader import InputReader

from math import floor, sqrt

def euclidean_distance(x, y, z):
    r = sqrt(x**2 + y**2 + z**2)
    return r

class CreateSimEnvironment:
    def __init__(self, file_path: str, simboxLength: int, cutoffdistance: float):
        self.myLattice = LatticeFactory(InputReader(file_path), simboxLength)
        self.simboxLength = simboxLength
        self.atomPairing = []

        Jijs = self.myLattice.Jijs
        simBox = self.myLattice.simBox

        latA = self.myLattice.latticeParameterA
        latB = self.myLattice.latticeParameterB
        latC = self.myLattice.latticeParameterC

        for z in range(self.simboxLength):
            for y in range(self.simboxLength):
                for x in range(self.simboxLength):
                    for element in Jijs:
                        if element[10] < cutoffdistance:
                            source = simBox[x][y][z].atoms[element[0]]
                            rel_cell_x, rel_cell_y, rel_cell_z = tuple(element[16:19])
                            corr_x, corr_y, corr_z = (floor(((x + rel_cell_x)/self.simboxLength)), floor(((y + rel_cell_y)/self.simboxLength)), (floor((z + rel_cell_z)/self.simboxLength)))
                            wrap_x, wrap_y, wrap_z = (corr_x*self.simboxLength*latA, corr_y*self.simboxLength*latB, corr_z*self.simboxLength*latC)
                            target = simBox[(x + rel_cell_x) % self.simboxLength][(y + rel_cell_y) % self.simboxLength][(z + rel_cell_z) % self.simboxLength].atoms[element[2]]
                            source_id = source[3]
                            target_id = target[3]
                            Jvalue = element[12]
                            x_val, y_val, z_val = (element[7] - wrap_x, element[8] - wrap_y, element[9] - wrap_z)
                            self.atomPairing.append([source_id + 1, element[0], target_id + 1, element[2], x_val, y_val, z_val, euclidean_distance(x_val, y_val, z_val), Jvalue])

        self.atomPairing.sort(key=lambda x: (x[0], x[2]))

    def writeToFile(self, file_name):
        print(f"Length: {len(self.atomPairing)}")
        with open(file_name, "w") as f:
            for row in self.atomPairing:
                formatted_row = ""
                for value in row:
                    if isinstance(value, int):
                        formatted_value = "{: >5}".format(value)  # Reserve 5 spaces for integers
                    elif isinstance(value, float):
                        formatted_value = "{: >12.6f}".format(
                            value)  # Reserve 10 spaces for floats, with 6 decimal places
                    formatted_row += formatted_value
                f.write(formatted_row + "\n")