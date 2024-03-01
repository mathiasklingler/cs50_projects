import numpy as np

# Assuming result_list is your tuple variable
result_list = (np.array([[1, 2, 3], [4, 5, 6]]), 10)

# Specify the file path
file_path = 'result_list5.txt'

# Save the NumPy array to a file
np.save(file_path, result_list[0])

# Save the integer to a separate file
with open('integer.txt', 'w') as file:
    file.write(str(result_list[1]))