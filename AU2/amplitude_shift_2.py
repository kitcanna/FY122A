import numpy as np
import matplotlib.pyplot as plt

# Constants
b = 1 # the amplitude of the driving force
m = 1 # the mass of the oscillator
k = 1 # the spring constant
omega_0 = np.sqrt(k / m) # Calculates the natural frequency of the undamped oscillator

# the damping coefficients
c_val = [0.1, 0.2, 0.5, 1, 1.5]

# Function to calculate A(omega)
def A(omega, c):
  return b/np.sqrt(m**2 * (omega**2 - omega_0**2)**2 + c**2 * omega**2)

# Interval around omega_0
omega_min = omega_0 - 1
omega_max = omega_0 + 1

# Array of omega values
# Creates a list of 100 evenly spaced values between omega_min and omega_max
omega = np.linspace(omega_min, omega_max, 100)

# Loop through c_array to plot amplitude curves for each value of c
for c in c_val:

  # Defines the variable A_omega as the result of calling the function A with the argument omega.
  A_omega = A(omega, c)

  # Plot the amplitude curve
  plt.plot(omega, A_omega, label='c = ' + str(c))

plt.xlabel('Drive Frequency (omega)')
plt.ylabel('Amplitude (A(omega))')
plt.title('Amplitude curve as a function of drive frequency')
plt.legend()
plt.show()



