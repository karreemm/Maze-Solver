from scipy.io import loadmat

# Load the .mat file
mat_data = loadmat('maze.mat')

print(mat_data.keys())  # Shows variable names

# Access specific data
data = mat_data['map']
print(data)
