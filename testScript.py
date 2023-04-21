from bin.environmentCreator.CreateSimEnvironment import CreateSimEnvironment

import os
# Usage example
file_path = os.path.join("inputs", "Jij_from_Hutsepot")
boxlength = 20
cutoff = 16.3
environment = CreateSimEnvironment(file_path, boxlength, cutoff)
environment.writeToFile("Jij_my_test.dat")
print("End")
