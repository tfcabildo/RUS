from scipy import signal
import matplotlib.pyplot as plt

points = 1000
a = 15.0
vcm = 2.048
vpp = 0.5 

# Creating the ricker wavelet
vec1 = signal.ricker(points, a)

# Make amplitude smaller
vec3 = vpp * vec1
# Create an inverse signal of vec3
vec4 = vec3 * -1

# Adjust DC level of differential signal to LTC2387's VCM
vec2 = vcm + vec3
vec5 = vcm + vec4

# Difference of the two signals
vec6 = vec2 - vec5

# Plot the ricker wavelet
plt.plot(vec2)
plt.plot(vec5)
plt.plot(vec6)
plt.show()