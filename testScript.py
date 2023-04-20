from bin.environmentCreator.InputReader import InputReader
from bin.environmentCreator.LatticeFactory import LatticeFactory

import os
# Usage example
file_path = os.path.join("inputs", "Jij_from_Hutsepot")

myReader = InputReader(file_path)
myLattice = LatticeFactory(myReader, 2)

for i in range(myLattice.simBoxLength):
    for j in range(myLattice.simBoxLength):
        for k in range(myLattice.simBoxLength):
            print(myLattice.simBox[i][j][k].atoms[1])
print("End")
