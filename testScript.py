from bin.environmentCreator.CreateSimEnvironment import CreateSimEnvironment

import os
# Usage example
file_path = os.path.join("inputs", "Jij_from_Hutsepot")
boxlength = 10
cutoff = 16.3
CreateSimEnvironment(file_path, boxlength, cutoff)
print("End")
