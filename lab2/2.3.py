#!/usr/bin/env python
# coding: utf-8

# In[38]:


import numpy as np
import matplotlib.pyplot as plt

class Packet:
    def __init__(self, packet_type):
        self.packet_type = packet_type

class MicroDataCenter:
    def __init__(self, service_rate):
        self.service_rate = service_rate
        self.buffer = []
        self.departure_times = []

    def process_packet(self, packet, arrival_time):
        self.buffer.append(packet)
        service_time = 1.0 / self.service_rate
        if len(self.departure_times) == 0:
            departure_time = arrival_time + service_time
        else:
            last_departure_time = max(self.departure_times)
            departure_time = max(arrival_time, last_departure_time) + service_time
        self.departure_times.append(departure_time)
        return departure_time

class CloudDataCenter:
    def __init__(self, service_rate):
        self.service_rate = service_rate
        self.buffer = []
        self.departure_times = []

    def process_packet(self, packet, arrival_time):
        self.buffer.append(packet)
        service_time = 1.0 / self.service_rate
        if len(self.departure_times) == 0:
            departure_time = arrival_time + service_time
        else:
            last_departure_time = max(self.departure_times)
            departure_time = max(arrival_time, last_departure_time) + service_time
        self.departure_times.append(departure_time)
        return departure_time

def simulate_system(service_rate_micro, service_rate_cloud, f, num_packets, Tq):
    micro_data_center = MicroDataCenter(service_rate_micro)
    cloud_data_center = CloudDataCenter(service_rate_cloud)

    type_a_queuing_times = []
    for i in range(num_packets):
        packet_type = 'A' if np.random.uniform() > f else 'B'
        packet = Packet(packet_type)
        arrival_time = i

        if packet_type == 'A':
            type_a_queuing_times.append(micro_data_center.process_packet(packet, arrival_time) - arrival_time)

        else:
            cloud_data_center.process_packet(packet, arrival_time)

    if len(type_a_queuing_times) > 0:
        max_type_a_queuing_time = max(type_a_queuing_times)
    else:
        max_type_a_queuing_time = 0

    return max_type_a_queuing_time

def find_minimum_service_rate(buffer_size_cloud, f, num_packets):
    # Initial guess for the minimum and maximum service rates
    min_service_rate = 0.1
    max_service_rate = 10.0

    while max_service_rate - min_service_rate > 0.001:
        service_rate_micro = (min_service_rate + max_service_rate) / 2.0
        max_type_a_queuing_time = simulate_system(service_rate_micro, 1.0, f, num_packets, Tq)

        if max_type_a_queuing_time <= Tq:
            max_service_rate = service_rate_micro
        else:
            min_service_rate = service_rate_micro

    return min_service_rate

# Define parameters for simulation
buffer_size_cloud = 10
f = 0.5  # Fraction of type B packets
num_packets = 10000  # Number of packets for simulation

# Find the maximum queuing time for type A packets
Tq = simulate_system(0.9, 10, f, num_packets, Tq)
print(f"Threshold Tq: {Tq} ms")

# Find the minimum service rate for Micro Data Center to achieve the desired threshold Tq
min_service_rate_micro = find_minimum_service_rate(buffer_size_cloud, f, num_packets)
print(f"Minimum service rate for Micro Data Center: {min_service_rate_micro} packets/ms")

# Plotting the results
service_rates_micro = np.linspace(0.7, 10, 100)
average_queuing_times = [simulate_system(sr, 1.0, f, num_packets, Tq) for sr in service_rates_micro]

plt.plot(service_rates_micro, average_queuing_times, label='Average Queuing Time for Type A Packets')
plt.axhline(y=Tq, color='red', linestyle='--', label='Threshold Tq')
plt.xlabel('Micro Data Center Service Rate (packets/ms)')
plt.ylabel(f'Average Queuing Time for Type A Packets (ms) ')
plt.title(f'Average Queuing Time for Type A vs. Micro Data Center Service Rate')
plt.grid(True)
plt.legend()
plt.show()


# In[136]:


import numpy as np
import matplotlib.pyplot as plt

class Packet:
    def __init__(self, packet_type):
        self.packet_type = packet_type

class MicroDataCenter:
    def __init__(self, service_rate):
        self.service_rate = service_rate
        self.buffer = []
        self.departure_times = []

    def process_packet(self, packet, arrival_time):
        self.buffer.append(packet)
        service_time = 1.0 / self.service_rate
        if len(self.departure_times) == 0:
            departure_time = arrival_time + service_time
        else:
            last_departure_time = max(self.departure_times)
            departure_time = max(arrival_time, last_departure_time) + service_time
        self.departure_times.append(departure_time)
        return departure_time

def simulate_system(num_edge_nodes, f, num_packets, service_rate_micro):
    micro_data_centers = [MicroDataCenter(service_rate_micro) for _ in range(num_edge_nodes)]

    queuing_times = []
    for i in range(num_packets):
        packet_type = 'A' if np.random.uniform() > f else 'B'
        packet = Packet(packet_type)
        arrival_time = i

        selected_node = np.random.choice(micro_data_centers)
        queuing_times.append(selected_node.process_packet(packet, arrival_time) - arrival_time)

    if len(queuing_times) > 0:
        avg_queuing_time = np.mean(queuing_times)
    else:
        avg_queuing_time = 0

    return avg_queuing_time

# Define parameters for simulation
f = 0.5  # Fraction of type B packets
num_packets = 10000  # Number of packets for simulation
service_rate_micro = 0.6  # Fixed average service rate for each edge node (packets/ms)

# Plotting the results
num_edge_nodes = np.arange(2, 10)  # Vary the number of edge nodes from 1 to 100
average_queuing_times = [simulate_system(ne, f, num_packets, service_rate_micro) for ne in num_edge_nodes]

plt.plot(num_edge_nodes, average_queuing_times, marker='o', linestyle='-')
plt.xlabel('Number of Edge Nodes')
plt.ylabel('Average Queuing Time (ms)')
plt.title('Average Queuing Time vs. Number of Edge Nodes')
plt.grid(True)
plt.show()


# In[135]:


import numpy as np
import matplotlib.pyplot as plt

class Packet:
    def __init__(self, packet_type):
        self.packet_type = packet_type

class MicroDataCenter:
    def __init__(self, service_rate):
        self.service_rate = service_rate
        self.buffer = []
        self.departure_times = []

    def process_packet(self, packet, arrival_time):
        self.buffer.append(packet)
        service_time = 1.0 / self.service_rate
        if len(self.departure_times) == 0:
            departure_time = arrival_time + service_time
        else:
            last_departure_time = max(self.departure_times)
            departure_time = max(arrival_time, last_departure_time) + service_time
        self.departure_times.append(departure_time)
        return departure_time

def simulate_system(num_edge_nodes, f, num_packets, service_rate_micro):
    micro_data_centers = [MicroDataCenter(service_rate_micro) for _ in range(num_edge_nodes)]

    queuing_times = []
    for i in range(num_packets):
        packet_type = 'A' if np.random.uniform() > f else 'B'
        packet = Packet(packet_type)
        arrival_time = i

        selected_node = np.random.choice(micro_data_centers)
        queuing_times.append(selected_node.process_packet(packet, arrival_time) - arrival_time)

    if len(queuing_times) > 0:
        avg_queuing_time = np.mean(queuing_times)
    else:
        avg_queuing_time = 0

    return avg_queuing_time

# Define parameters for simulation
f = 0.5  # Fraction of type B packets
num_packets = 10000  # Number of packets for simulation
service_rate_micro = 0.6 # Fixed average service rate for each edge node (packets/ms)
Tq = 2.3333333333357587  # Threshold Tq (fixed)

# Plotting the results
num_edge_nodes = np.arange(2, 10)  # Vary the number of edge nodes from 1 to 100
average_queuing_times = [simulate_system(ne, f, num_packets, service_rate_micro) for ne in num_edge_nodes]

plt.plot(num_edge_nodes, average_queuing_times, marker='o', linestyle='-')
plt.axhline(y=Tq, color='red', linestyle='--', label='Threshold Tq')
plt.xlabel('Number of Edge Nodes')
plt.ylabel('Average Queuing Time (ms)')
plt.title('Average Queuing Time vs. Number of Edge Nodes')
plt.grid(True)
plt.legend()
plt.show()


# In[ ]:




