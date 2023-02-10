import numpy as np
import matplotlib.pyplot as plt

# The code implements the numerical solution of the damped harmonic oscillator equation using the Euler method. 
# The solution gives the position x and velocity v of the oscillator at each time step.


# Constants
# m = the mass of the oscillator
# c = the damping coefficient
# k = the spring constant
# b = the amplitude of the driving force
# omega = the frequency of the driving force

#m = 1
#k = 1
#b = 1
m = 0.05
k = 1
b = 0.02
omega_0 = np.sqrt(k/m)

# Euler
def euler(m, c, k, b, omega, x0, v0, T, dt):
    # arange(start, stop, step) 
    t = np.arange(0, T, dt) 

    # Return an array of zeros with the same shape and type as a given array.
    # x0 = the initial position of the oscillator
    x = np.zeros_like(t)
    x[0] = x0 

    # Return an array of zeros with the same shape and type as a given array.
    # v0 = the initial velocity of the oscillator
    v = np.zeros_like(t)
    v[0] = v0 

    # Start at 1. For every i in the length of t, iterate 
    for i in range(1, len(t)):

        # Updates the position of the oscillator at time step i 
        # by adding the velocity of the oscillator at the previous time step i-1 to the current position x[i-1].
        x[i] = x[i-1] + v[i-1]*dt
    
        # Updates the velocity of the oscillator at time step i 
        # using the velocity at the previous time step i-1 and the driving force, damping force, and spring force. 
        # The forces are determined using the equations for a damped harmonic oscillator. 
        # The np.cos function calculates the cosine value of the driving force.
        v[i] = v[i-1] + (b*np.cos(omega*t[i-1]) - c*v[i-1] - k*x[i-1])/m * dt
    
    # Returns the time array t and the position array x of the oscillator 
    # at each time step.
    return t, x

#c_values = [0.01, 0.1, 0.5, 1, 2, 5]
c_val = [0.01]
omega_val = [0.5 * omega_0, omega_0, 1.5 * omega_0]
# By choosing 0.9 and 1.1, we are defining a range of frequencies 
# that are slightly below and slightly above omega_0. 
# You could choose different values, for example, 0.5 and 1.5 if you wanted a wider range 
# or 0.95 and 1.05 for a narrower range. The important thing is to 
# have a range of frequencies defined so that you can simulate and analyze the system's behavior.

# Time
T = 10 # simulation time
dt = 0.001 # time step

# Loop to plot
for c in c_val:
    for omega in omega_val:
        t, x = euler(m, c, k, b, omega, 1, 0, T, dt)
        plt.plot(t, x, label=f'c = {c}, $\omega$ = {omega}')

# Constants
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Solution to the damped harmonic oscillator equation using Euler\'s method')
plt.legend()
plt.show()
