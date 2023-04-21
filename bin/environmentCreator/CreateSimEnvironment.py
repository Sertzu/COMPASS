from bin.environmentCreator.LatticeFactory import LatticeFactory
from bin.environmentCreator.InputReader import InputReader


class CreateSimEnvironment:
    def __init__(self, file_path: str, simboxLength: int, cutoffdistance: float):
        self.myLattice = LatticeFactory(InputReader(file_path), simboxLength)
        self.simboxLength = simboxLength
        self.atomPairing = []

        Jijs = self.myLattice.Jijs
        simBox = self.myLattice.simBox

        for z in range(self.simboxLength):
            for y in range(self.simboxLength):
                for x in range(self.simboxLength):
                    for element in Jijs:
                        if element[10] < cutoffdistance:
                            source = simbox[x][y][z][element[0]]
                            rel_cell_x, rel_cell_y, rel_cell_y = tuple(element[16:19])
                            target = simbox[(x + rel_cell_x) % self.simboxLength][(y + rel_cell_y) % self.simboxLength][(y + rel_cell_y) % self.simboxLength][element[2]]
                            source_id = source[3]
                            target_id = target[3]
                            Jvalue = element[12]
                            self.atomPairing.append([source_id + 1, element[0], target_id + 1, element[2], 0.0, 0.0, 0.0, 0.0, Jvalue])

        print("ello")