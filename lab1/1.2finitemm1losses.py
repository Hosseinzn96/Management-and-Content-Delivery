#!/usr/bin/env python
# coding: utf-8

# In[4]:


import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt
import numpy as np

# ******************************************************************************
# Constants
# ******************************************************************************

# Buffer_size = np.inf
# ******************************************************************************
# To take the measurements
# ******************************************************************************
class Measure:
    def __init__(self, Narr, Ndep, NAveraegUser, OldTimeEvent, AverageDelay):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        self.utq = 0
        self.st = 0
        self.delays = []
        self.delayed = []
        self.delay_w = 0
        self.st_w = 0
        self.count = 0
        self.dep_w = 0

# ******************************************************************************
# Client
# ******************************************************************************
class Client:
    def __init__(self, type, arrival_time):
        self.type = type
        self.arrival_time = arrival_time

# ******************************************************************************
# Server
# ******************************************************************************
class Server():
    # constructor
    def __init__(self):
        self.idle = True

    def busy(self):
        self.idle = False

    def ready(self):
        self.idle = True

    def status(self):
        return self.idle

# ******************************************************************************
# Arrivals
# *********************************************************************
def arrival(time, FES, queue, buffer_size):
    global users, in_service, loss

    # cumulate statistics
    data.arr += 1
    data.utq += (users - in_service) * (time - data.oldT)
    data.ut += users * (time - data.oldT)
    data.oldT = time

    # sample the time until the next event
    inter_arrival = random.expovariate(lambd=1.0 / ARRIVAL)

    # schedule the next arrival
    FES.put((time + inter_arrival, "Arrival"))

    # create a record for the client
    if len(queue) < buffer_size:
        users += 1
        client = Client(TYPE1, time)
        queue.append(client)
        data.delayed.append(client.arrival_time)

        # if the server is idle start the service
        if users == 1:
            data.count += 1
            data.delayed.remove(client.arrival_time)
            service_time = random.expovariate(1.0 / SERVICE)
            FES.put((time + service_time, "Departed"))
            S.busy()
            data.st += service_time
            in_service += 1
    else:
        loss += 1

# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, FES, queue):
    global users, temp_st, in_service

    # cumulate statistics
    data.dep += 1  
    data.ut += users * (time - data.oldT)
    data.utq += (users - in_service) * (time - data.oldT)
    data.oldT = time
    
    in_service -= 1
    users -= 1
    
    if len(queue) != 0:
        client = queue.pop(0)
        
        data.delay += (time - client.arrival_time)
        data.delays.append(time - client.arrival_time)
        
        if client.arrival_time in data.delayed:
            data.st_w += temp_st[0]
            temp_st.pop(0)
    
        if users > 0:
            S.busy()
            service_time = random.expovariate(1.0 / SERVICE)
            data.st += service_time
            temp_st.append(service_time)
            FES.put((time + service_time, "Departed"))

# ******************************************************************************
# The "main" of the simulation
# ******************************************************************************

random.seed(50)

arrival_rates = np.arange(0.1, 2, 0.2)

LOAD = 0.85
SERVICE = 10.0  # av service time
TYPE1 = 1
SIM_TIME = 500000

buffer_sizes = [1, 5, 10]

average_delays = []
num_losses = []

for buffer_size in buffer_sizes:
    # Reset the results for each buffer size
    average_delays_buffer = []
    num_losses_buffer = []

    for arrival_rate in arrival_rates:
        S = Server()
        ARRIVAL = SERVICE / (LOAD * arrival_rate)
    
        data = Measure(0, 0, 0, 0, 0)
        utq = 0
        st = 0
        delayed = []
        delay_w = 0
        st_w = 0
        count = 0
        dep_w = 0
        users = 0
        time = 0
        in_service = 0
        MM2 = []
        temp_st = []
        loss = 0
        FES = PriorityQueue()
        FES.put((0, "Arrival"))
        
        # simulate until the simulated time reaches a constant
        while time < SIM_TIME:
            (time, event_type) = FES.get()

            if event_type == "Arrival":
                arrival(time, FES, MM2, buffer_size=buffer_size)

            elif event_type == "Departed":
                S.ready()
                departure(time, FES, MM2)   
                
        lambtda = round(1/ARRIVAL, 3)
        mu = round(1/SERVICE, 3)
        rho = round(lambtda/mu, 3)
        
        average_delay = round(data.delay / data.dep, 3)

        average_delays_buffer.append(average_delay)
        num_losses_buffer.append(loss)
    
    average_delays.append(average_delays_buffer)
    num_losses.append(num_losses_buffer)

# ******************************************************************************
# Plot
# ******************************************************************************
fig, axes = plt.subplots(nrows=1, ncols=len(buffer_sizes), figsize=(15, 5))

for i, buffer_size in enumerate(buffer_sizes):
    axes[i].plot(arrival_rates, num_losses[i], marker='o')
    axes[i].set_xlabel("Arrival Rate")
    axes[i].set_ylabel("Number of losses")
    axes[i].set_title("Buffer Size: {}".format(buffer_size))

plt.tight_layout()
plt.show()


# In[ ]:




