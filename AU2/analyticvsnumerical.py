import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
tmax = 10
t = np.arange(0,tmax,dt)
dim = len(t)

# Parametrar för numerisk lösning
m = 1
k = 1
c = 0.2
ca = [0.2, 2, 5]  # the given damping coefficients
b = 0
w = 2.5
w0 = np.sqrt(k/m)
lam = c/(2*m)

# Parametrar för analytisk lösning
A = 1.01
beta = np.sqrt(w0**2-lam**2)
delt = np.radians(81.9106)

# Initialisera vektorer
x = np.zeros(dim)
v = np.zeros(dim)
a = np.zeros(dim)

# Begynnelsevillkor
x[0] = 1
v[0] = 0
a[0] = (-k*x[0] - c*v[0] + b*np.cos(w*t[0]))/m

# Analytic solution
xa = A*np.exp(-lam*t)*np.sin(beta*t+delt)

# Numerical solution
for i in range(dim-1):
    v[i+1] = v[i] + a[i]*dt
    x[i+1] = x[i] + v[i]*dt
    a[i+1] = (-k*x[i+1] -c*v[i+1] + b*np.cos(w*t[i+1]))/m

plt.plot(t, x, label='Numerical Solution')
plt.plot(t, xa, label='Analytical Solution')
plt.xlabel('Time (t)')
plt.ylabel('Displacement (x)')
plt.legend()
plt.title('Comparison of Analytical and Numerical Solutions')
plt.show()