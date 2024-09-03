#!/usr/bin/env python
# coding: utf-8

# In[8]:


import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
num_packets = 10000  # Total number of packets
f = 0.5  # Fraction of type B packets

# Lists to store data for plotting
packet_drop_probability_buffer_50 = []
packet_drop_probability_buffer_500 = []

# Simulation loop for buffer size 50
buffer_size_micro_50 = 50
total_packets_forwarded = 0
packets_dropped = 0
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_micro_50:
            # Packet dropped if Micro Data Center buffer is full
            packets_dropped += 1

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability_buffer_50.append(packets_dropped / total_packets_forwarded)

# Simulation loop for buffer size 500
buffer_size_micro_500 = 500
total_packets_forwarded = 0
packets_dropped = 0
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_micro_500:
            # Packet dropped if Micro Data Center buffer is full
            packets_dropped += 1

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability_buffer_500.append(packets_dropped / total_packets_forwarded)

# Plot packet drop probability for both buffer sizes
plt.plot(packet_drop_probability_buffer_50, label="Buffer Size 50")
plt.plot(packet_drop_probability_buffer_500, label="Buffer Size 500")
plt.xlabel("Time")
plt.ylabel("Packet Drop Probability")
plt.legend()
plt.title("Effect of Buffer Size in Micro Data Center on Packet Drop Probability")
plt.show()


# In[13]:


import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
num_packets = 10000  # Total number of packets
f = 0.5  # Fraction of type B packets

# Lists to store data for plotting
packet_drop_probability_buffer_50 = []
packet_drop_probability_buffer_500 = []

# Simulation loop for buffer size 50 in the Cloud Data Center
buffer_size_cloud_50 = 50
total_packets_forwarded = 0
packets_dropped = 0
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_cloud_50:
            # Packet dropped if Cloud Data Center buffer is full
            packets_dropped += 1

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability_buffer_50.append(packets_dropped / total_packets_forwarded)

# Simulation loop for buffer size 500 in the Cloud Data Center
buffer_size_cloud_500 = 250
total_packets_forwarded = 0
packets_dropped = 0
for i in range(num_packets):
    # Process packet
    if np.random.rand() < f:
        # Type B packet, need to forward to Cloud
        total_packets_forwarded += 1
        if total_packets_forwarded > buffer_size_cloud_500:
            # Packet dropped if Cloud Data Center buffer is full
            packets_dropped += 1

    # Calculate packet drop probability at each step (avoiding division by zero)
    if total_packets_forwarded > 0:
        packet_drop_probability_buffer_500.append(packets_dropped / total_packets_forwarded)

# Plot packet drop probability for both buffer sizes in the Cloud Data Center
plt.plot(packet_drop_probability_buffer_50, label="Buffer Size 50")
plt.plot(packet_drop_probability_buffer_500, label="Buffer Size 500")
plt.xlabel("Time")
plt.ylabel("Packet Drop Probability")
plt.legend()
plt.title("Effect of Buffer Size in Cloud Data Center on Packet Drop Probability")
plt.show()


# In[65]:


import numpy as np
import matplotlib.pyplot as plt

class Packet:
    def __init__(self, packet_type):
        self.packet_type = packet_type

class EdgeNode:
    def __init__(self, buffer_size):
        self.buffer = []
        self.buffer_size = buffer_size

    def process_packet(self, packet):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(packet)
            return True  # Packet processed successfully
        else:
            return False  # Buffer full, unable to process packet

class MicroDataCenter:
    def __init__(self, edge_nodes):
        self.edge_nodes = edge_nodes

    def process_packet(self, packet):
        for node in self.edge_nodes:
            if node.process_packet(packet):
                return True  # Packet processed successfully
        return False  # All edge nodes busy or buffers full, packet forwarded to Cloud

class CloudDataCenter:
    def __init__(self, cloud_buffer_size):
        self.buffer = []
        self.cloud_buffer_size = cloud_buffer_size

    def process_packet(self, packet):
        if len(self.buffer) < self.cloud_buffer_size:
            self.buffer.append(packet)
            return True  # Packet processed successfully
        else:
            return False  # Buffer full, unable to process packet

def simulate_system(buffer_size_micro, buffer_size_cloud, f, num_packets):
    edge_node = EdgeNode(buffer_size_micro)
    micro_data_center = MicroDataCenter([edge_node])
    cloud_data_center = CloudDataCenter(buffer_size_cloud)

    queuing_delays = []
    for i in range(num_packets):
        packet_type = 'A' if np.random.uniform() > f else 'B'
        packet = Packet(packet_type)
        arrival_time = i

        if packet_type == 'A':
            processing_time = np.random.uniform(0.1, 0.5)  # Random processing time for each packet type A
            success = micro_data_center.process_packet(packet)
            if success:
                departure_time = i + processing_time
                queuing_delays.append(departure_time - arrival_time)
        else:
            processing_time = np.random.uniform(2,4.5)  # Random processing time for each packet type B
            success = micro_data_center.process_packet(packet) or cloud_data_center.process_packet(packet)
            if success:
                departure_time = i + processing_time
                queuing_delays.append(departure_time - arrival_time)

    average_queuing_delay = np.mean(queuing_delays)
    return average_queuing_delay

# (c) Impact of different values of f (fraction of type B packets)
buffer_size_micro = 10
buffer_size_cloud = 10
f_values = [ 0.2, 0.4, 0.6, 0.8]  # Example values of f
num_packets = 1000  # Example number of packets

average_delays = []
for f in f_values:
    average_queuing_delay = simulate_system(buffer_size_micro, buffer_size_cloud, f, num_packets)
    average_delays.append(average_queuing_delay)
    print(f"Average queuing delay with f={f}: {average_queuing_delay}")

# Plotting the results
plt.plot(f_values, average_delays, marker='o', linestyle='-')
plt.xlabel('Fraction of Type B Packets (f)')
plt.ylabel('Average Delay (ms)')
plt.title('Average Delay vs. Fraction of Type B Packets')
plt.show()


# In[ ]:




