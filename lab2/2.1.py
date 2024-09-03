#!/usr/bin/env python
# coding: utf-8

# In[12]:


import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
num_packets = 10000  # Total number of packets
f = 0.5  # Fraction of type B packets
buffer_size_cloud = 100  # Buffer size in Cloud Data Center

# Variables to track packet drop
total_packets_forwarded = 0
packets_dropped = 0

# Warm-up transient variables
warmup_period = 1000  # Number of packets to discard as warm-up period
in_warmup_period = True

# Lists to store data for plotting
packet_drop_probability = []

# Simulation loop
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_cloud:
            # Packet dropped if Cloud buffer is full
            packets_dropped += 1

    # Check if warm-up period is over
    if in_warmup_period and i >= warmup_period:
        in_warmup_period = False

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability.append(packets_dropped / total_packets_forwarded)

# Plot packet drop probability over time
plt.plot(packet_drop_probability, label="Packet Drop Probability")
plt.axvline(x=warmup_period, linestyle="--", color="r", label="Transition to Steady State")
plt.xlabel("Time")
plt.ylabel("Packet Drop Probability")
plt.legend()
plt.title("Packet Drop Probability including warm-up transient")
plt.show()


# In[13]:


import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
num_packets = 10000  # Total number of packets
f = 0.5  # Fraction of type B packets
buffer_size_cloud = 100  # Buffer size in Cloud Data Center

# Variables to track packet drop
total_packets_forwarded = 0
packets_dropped = 0

# Warm-up transient variables
warmup_period = 1000  # Number of packets to discard as warm-up period
in_warmup_period = True

# Lists to store data for plotting
packet_drop_probability = []

# Simulation loop
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_cloud:
            # Packet dropped if Cloud buffer is full
            packets_dropped += 1

    # Check if warm-up period is over
    if in_warmup_period and i >= warmup_period:
        in_warmup_period = False

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability.append(packets_dropped / total_packets_forwarded)

# Remove warm-up transient data
packet_drop_probability_steady = packet_drop_probability[warmup_period:]

# Plot packet drop probability in the steady state
plt.plot(packet_drop_probability_steady, label="Packet Drop Probability")
plt.xlabel("Time (Steady State)")
plt.ylabel("Packet Drop Probability")
plt.title("Steady State Packet Drop Probability after removing warm-up transient")
plt.show()


# In[ ]:




