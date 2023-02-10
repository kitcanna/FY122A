import numpy as np
import matplotlib.pyplot as plt

# Constants
c = 1 # the damping coefficient
b = 1 # the amplitude of the driving force
m = 1 # the mass of the oscillator
k = 1 # the spring constant
omega_0 = np.sqrt(k / m) # Calculates the natural frequency of the undamped oscillator

# Calculate A(omega)
def A(omega):
 return b/np.sqrt(m**2 * (omega**2 - omega_0**2)**2 + c**2 * omega**2)

# Interval around omega_0
omega_min = omega_0 - 1
omega_max = omega_0 + 1

# Array of omega values
# Creates a list of 100 evenly spaced values between omega_min and omega_max
omega = np.linspace(omega_min, omega_max, 100)

# Defines the variable A_omega as the result of calling the function A with the argument omega.
A_omega = A(omega)

# Plot the amplitude curve
plt.plot(omega, A_omega)
plt.xlabel('Drive Frequency (omega)')
plt.ylabel('Amplitude (A(omega))')
plt.title('Amplitude curve as a function of drive frequency')
plt.show()
