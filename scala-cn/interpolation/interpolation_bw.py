import numpy as np
from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

x = []
y = []
z = []

for i in range(21):
    for j in range(21):
        filename = f'../tmp/profiling_ce20_de_20/profiles_local/cen_{i}_cde_0_sen_0_sde_{j}_send_bw_pod.log'
        fp = open(filename, 'r')
        lines = fp.readlines()
        fp.close()
        enter_data = False
        out_data = ''
        for line in lines:
            if line.startswith(' #bytes'):
                enter_data = True
                continue
            if not enter_data:
                continue
            if line.startswith('---'):
                continue
            data_split = line.split()
            out_data = float(data_split[3]) * 8 / 1024
            # out_data = float(data_split[4])
            # break
        x.append(i)
        y.append(j)
        z.append(out_data)

x = np.array(x)
y = np.array(y)
z = np.array(z) * 8 / 1024



# Define the model function for a plane
def model(variables, x, y):
    # a, b, c, d, e = variables
    # return a * x ** 2 + b * y ** 2 + c * x + d * y + e
    # a, b, c, d, e, f, g = variables
    # return a * x ** 3 + b * y ** 3 + c * x ** 2 + d * y ** 2 + e * x + f * y + g
    # a, b, c, d, e, f, g, h, i = variables
    # return a * x ** 4 + b * y ** 4 + c * x ** 3 + d * y ** 3 + e * x ** 2 + f * y ** 2 + g * x + h * y + i
    a, b, c, d, e = variables
    return a * np.e ** (-((x - b)**2 + (y - c)**2) / (2 * d**2)) + e

# Define the function to minimize
def objective_function(variables, x, y, z):
    return np.sqrt((model(variables, x, y) - z)**2)

# Initial guess for the parameters [a, b, c]
initial_guess = [100, -10, -10, 1000, 20]

# Perform the fitting
result = least_squares(objective_function, initial_guess, args=(x, y, z))
fitted_params = result.x
print(fitted_params)

# Plot the original data and the fitted plane
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d', computed_zorder=False)

# Generate meshgrid for the plane surface
xx, yy = np.meshgrid(np.linspace(0, 101), np.linspace(0, 101))
zz = model(fitted_params, xx, yy)

# Plot the fitted plane
ax.plot_surface(xx, yy, zz, alpha=1, label='Fit function', cmap='summer', vmin=20, vmax=100)
ax.scatter(x, y, z, label='Samples', color=(128/255, 0/255, 128/255), s=25)

ax.set_xlabel('Host Flow Groups')
ax.set_ylabel('Remote Flow Groups')
ax.set_zlabel('Bandwidth (Gbps)')
ax.legend()

plt.show()