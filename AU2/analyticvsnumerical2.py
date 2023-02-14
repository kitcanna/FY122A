import numpy as np
import matplotlib.pyplot as plt

dt = 0.0001
tmax = 200
t = np.arange(0,tmax,dt)
dim = len(t)

# Parametrar för numerisk lösning
m = 1
k = 1
c = 0.05
b = 1
w = 2
w0 = np.sqrt(k/m)
lam = c/(2*m)

# Initialisera vektorer
x = np.zeros(dim)
v = np.zeros(dim)
a = np.zeros(dim)

# Begynnelsevillkor
x[0] = 1
v[0] = 0
a[0] = (-k*x[0] - c*v[0] + b*np.cos(w*t[0]))/m 

# Numerical solution
for i in range(dim-1):
    v[i+1] = v[i] + a[i]*dt
    x[i+1] = x[i] + v[i]*dt
    a[i+1] = (-k*x[i+1] -c*v[i+1] + b*np.cos(w*t[i+1]))/m 
    a =V(t) * (L - 1 / (ω * C) )

plt.plot(t, x, label='Numerical Solution')
plt.legend(fontsize=15)
plt.xlabel('Time (t)',fontsize=15)
plt.ylabel('Displacement (x)',fontsize=15)
plt.title('From transient to stationary',fontsize=15)
plt.xticks(fontsize=14) # set font size for x-axis ticks
plt.yticks(fontsize=14) # set font size for y-axis ticks
plt.show()
