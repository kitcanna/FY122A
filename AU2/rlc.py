import numpy as np
import matplotlib.pyplot as plt

#R = 5
R = 500
L = 8.2e-3
C = 100e-6

f = np.logspace(0, 6, num=1000) # generates an array of 1000 values between 10^0 and 10^6 (inclusive) on a logarithmic scale
omega = 2*np.pi*f # calculates the angular frequency in radians per second (rad/s)

Z_R = R # assigns the value of R to the variable Z_R, which represents the impedance of the resistor
Z_L = 1j*omega*L # calculates the impedance of the inductor using the formula Z_L = jωL, where j is the imaginary unit (sqrt(-1)) and ω is the angular frequency.
Z_C = 1/(1j*omega*C) # calculates the impedance of the capacitor using the formula Z_C = 1/(jωC)

Z = Z_R + Z_L + Z_C # calculates the total impedance of the circuit by summing the impedances of the resistor, inductor, and capacitor
H = Z_C / Z # calculates the transfer function of the circuit, which represents the ratio of the output voltage to the input voltage. The transfer function is equal to the impedance of the capacitor divided by the total impedance of the circuit

plt.semilogx(f, 20*np.log10(np.abs(H)))
plt.xlabel('Frekvens (Hz)')
plt.ylabel('Amplitudförstärkning (dB)')
plt.title('Frekvensrespons för RLC-lågpassfilter')
plt.grid()
plt.show()