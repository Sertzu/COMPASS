from bin.environmentCreator.CreateSimEnvironment import CreateSimEnvironment

import os
# Usage example
file_path = os.path.join("inputs", "Jij_from_Hutsepot")
boxlength = 4
cutoff = 15.0
environment = CreateSimEnvironment(file_path, boxlength, cutoff)
environment.writeToFile("Jij_4_15_new2.dat")
print("End")
