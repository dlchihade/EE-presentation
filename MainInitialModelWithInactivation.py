"""
Author    : Younes Valibeigi  
Date      : 2025-01-09  
Description: Updated Voltage-clamp simulation model for studying ion channel behavior,  
             utilizing steady-state activation curves and current calculations.  
Contact   : younes.valibeigi@mcgill.ca  
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Define the twoParamSig function
def twoParamSig(x, params):
    b = params[0]
    x0 = params[1]
    return 1 / (1 + np.exp(-b * (x - x0)))

# Load data
# Assuming you have 'CookAssignemnt1UnknownCurrent.mat' loaded as a dictionary (you can use scipy.io to load .mat files)
data = scipy.io.loadmat('CookAssignemnt1UnknownCurrent.mat')

# Extract variables (you may need to adjust based on actual .mat file structure)
t = data['t'].flatten()
vStep = data['vStep']
iUnknownCurrent = data['iUnknownCurrent']

# Model parameters
ba = .1  # stady state channels open per mV
v0a = -5  # mV
bi = .2
v0i = -10
gBar = .005  # mS
Er = 0   # mV
taua = 2  # msec
taui = 3

# Initialize the figure
plt.figure(figsize=(12, 10))

# Plot steady state curves
# Steady state activation curves
plt.subplot(6, 2, 1)
plt.grid(True)
v = np.arange(-80, 21, 20)  # from -80 to 20, with step of 20
plt.plot(v, twoParamSig(v, [ba, v0a]), linewidth=1.5, label="xa(t = inf)")
plt.plot(v, 1 - twoParamSig(v, [bi, v0i]), linewidth=1.5, label="xi(t = inf)")
plt.xlabel('mV')
plt.legend(loc='best')

# Model parameters display
plt.subplot(6, 2, 2)
plt.grid(False)
plt.text(0.1, 0.9, f'ba = {ba}', fontsize=12)
plt.text(0.1, 0.9, f'bi = {bi}', fontsize=12)
plt.text(0.1, 0.8, f'v0a = {v0a} mV', fontsize=12)
plt.text(0.1, 0.8, f'v0i = {v0i} mV', fontsize=12)
plt.text(0.1, 0.7, f'taua = {taua} msec', fontsize=12)
plt.text(0.1, 0.7, f'taui = {taui} msec', fontsize=12)
plt.text(0.1, 0.6, f'gBar = {gBar} mS', fontsize=12)
plt.text(0.1, 0.5, f'Er = {Er} mV', fontsize=12)
plt.axis('off')

# Run v-clamp simulation
dt = t[1] - t[0]
for vStepIndex in range(vStep.shape[1]):
    v = vStep[:, vStepIndex]
    xa = np.zeros_like(v, dtype=float)
    g = np.zeros_like(v, dtype=float)
    i = np.zeros_like(v, dtype=float)
    xi = np.zeros_like(v, dtype=float)

    for j in range(len(t)):
        xaInf = twoParamSig(v[j], [ba, v0a])
        xiInf = 1 - twoParamSig(v[j], [ba, v0a])

        if j > 0:
            # Advance channel activation values for each time point
            xa[j] = xa[j-1] + (xaInf - xa[j-1]) * (1 - np.exp(-dt/taua))
            xi[j] = xi[j-1] + (xiInf - xi[j-1]) * (1 - np.exp(-dt/taui))
        else:
            # First time point, assume channel activation is at steady state
            xa[j] = xaInf
            xi[j] = xiInf
        
        g[j] = gBar * xa[j] * xi[j]
        i[j] = g[j] * (v[j] - Er)
  
    # Plot the results
    plt.subplot(6, 1, 2)
    plt.plot(t, v, linewidth=1.5)
    plt.ylabel('V step (mV)')
    plt.grid(True)

    plt.subplot(6, 1, 3)
    plt.plot(t, xa, linewidth=1.5)
    plt.ylabel('xa')
    plt.grid(True)

    plt.subplot(6, 1, 4)
    plt.plot(t, xi, linewidth=1.5)
    plt.ylabel('xi')
    plt.grid(True)

    plt.subplot(6, 1, 5)
    plt.plot(t, g, linewidth=1.5)
    plt.ylabel('g (mS)')
    plt.grid(True)

    plt.subplot(6, 1, 6)
    plt.plot(t, iUnknownCurrent[:, vStepIndex], linewidth=2, label='Data')
    plt.plot(t, i, '--', linewidth=2, label='Model')
    plt.xlabel('msec')
    plt.ylabel('i (mA)')
    plt.legend(loc='best')
    plt.grid(True)

plt.tight_layout()
plt.show()
