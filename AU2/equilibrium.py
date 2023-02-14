import numpy as np
import matplotlib.pyplot as plt

# Constants
m = 1 # the mass of the oscillator
k = 1 # the spring constant
c = [0.2, 2, 5]  # the given damping coefficients

# Initial conditions
x0 = 1 # the initial displacement of the oscillator
v0 = 0 # the initial velocity of the oscillator

# Time
T = 10 # the total time of the simulation
dt = 0.001 # time step
t = np.arange(0, T, dt) # arange(start, stop, step) 

# Euler's method
def euler(x, v, t, c):
    # The function initializes two arrays, x_new and v_new, 
    # to store the values of the displacement and velocity of the oscillator at each time step.
    x_new = np.zeros(len(t))
    v_new = np.zeros(len(t))
    x_new[0] = x0
    v_new[0] = v0

    # Start at 1. For every i in the length of t, iteratively 
    # calculate the new values of x and v using Euler's method and 
    # store them in the x_new and v_new arrays
    for i in range(1, len(t)):
        x_new[i] = x_new[i-1] + v_new[i-1]*dt
        v_new[i] = v_new[i-1] - (k/m)*x_new[i-1]*dt - (c/m)*v_new[i-1]*dt
    return x_new, v_new

for value in c:
    x, v = euler(x0, v0, t, value)
    plt.plot(t, x, label='c={}'.format(value))

# Plot
plt.legend(fontsize=15)
plt.xlabel('Time (t)', fontsize=15) # set font size for x-axis label
plt.ylabel('Displacement (x)', fontsize=15) # set font size for y-axis label
plt.xticks(fontsize=14) # set font size for x-axis ticks
plt.yticks(fontsize=14) # set font size for y-axis ticks

plt.show()
