import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Define fuzzy input/output ranges
temperature = np.arange(15, 46, 1)
humidity = np.arange(10, 91, 1)
lighting = np.arange(0, 101, 1)
comfort = np.arange(0, 11, 1)

# Define membership functions
temp_cold = fuzz.trimf(temperature, [15, 15, 25])
temp_moderate = fuzz.trimf(temperature, [20, 30, 35])
temp_hot = fuzz.trimf(temperature, [30, 45, 45])

hum_dry = fuzz.trimf(humidity, [10, 10, 40])
hum_normal = fuzz.trimf(humidity, [30, 50, 70])
hum_humid = fuzz.trimf(humidity, [60, 90, 90])

light_dim = fuzz.trimf(lighting, [0, 0, 40])
light_normal = fuzz.trimf(lighting, [30, 50, 70])
light_bright = fuzz.trimf(lighting, [60, 100, 100])

comfort_low = fuzz.trimf(comfort, [0, 0, 4])
comfort_medium = fuzz.trimf(comfort, [3, 5, 7])
comfort_high = fuzz.trimf(comfort, [6, 10, 10])

# Plotting
plt.figure(figsize=(12, 10))

# Temperature
plt.subplot(2, 2, 1)
plt.plot(temperature, temp_cold, 'b', label='Cold')
plt.plot(temperature, temp_moderate, 'g', label='Moderate')
plt.plot(temperature, temp_hot, 'r', label='Hot')
plt.title('Temperature')
plt.xlabel('°C')
plt.ylabel('Membership')
plt.legend()

# Humidity
plt.subplot(2, 2, 2)
plt.plot(humidity, hum_dry, 'b', label='Dry')
plt.plot(humidity, hum_normal, 'g', label='Normal')
plt.plot(humidity, hum_humid, 'r', label='Humid')
plt.title('Humidity')
plt.xlabel('%')
plt.ylabel('Membership')
plt.legend()

# Lighting
plt.subplot(2, 2, 3)
plt.plot(lighting, light_dim, 'b', label='Dim')
plt.plot(lighting, light_normal, 'g', label='Normal')
plt.plot(lighting, light_bright, 'r', label='Bright')
plt.title('Lighting')
plt.xlabel('%')
plt.ylabel('Membership')
plt.legend()

# Comfort
plt.subplot(2, 2, 4)
plt.plot(comfort, comfort_low, 'b', label='Low')
plt.plot(comfort, comfort_medium, 'g', label='Medium')
plt.plot(comfort, comfort_high, 'r', label='High')
plt.title('Comfort Level')
plt.xlabel('Comfort Index')
plt.ylabel('Membership')
plt.legend()

plt.tight_layout()
plt.show()
