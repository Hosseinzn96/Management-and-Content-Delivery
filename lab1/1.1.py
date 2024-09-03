#!/usr/bin/env python
# coding: utf-8

# In[4]:


# 2M/M/1 Limites/UnlimitedWaitingLine

#!/usr/bin/python3

import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt
import numpy as np

# ******************************************************************************
# Constants
# ******************************************************************************
LOAD = 0.85 # usage of server
SERVICE = 10.0  # avg service time
TYPE1 = 1
SIM_TIME = 500000

arrivals = 0 # keeps track of num of arrivals
users = 0
BusyServer = False  # True: server is currently busy; False: server is currently idle
in_service = 0 # keeps track of num of clients being served

MM1 = []

# temp_st later used to calculate the delay experienced by the client.
temp_st = [] # stores temporary service times during the simulation.

busy_time = 0 # total time that the server has been busy serving users.
delay = []

loss = 0

#Buffer_size = 10 # finite waiting line
Buffer_size = np.inf # infinite waiting line


# ******************************************************************************
# To take the measurements
# ******************************************************************************
class Measure:
    def __init__(self, Narr, Ndep, NAveraegUser, OldTimeEvent, AverageDelay):
        self.arr = Narr
        self.dep = Ndep
        self.ut = NAveraegUser # Store the average number of users in the system during the simulation.
        self.oldT = OldTimeEvent
        self.delay = AverageDelay
        self.utq = 0  # data.ut = number of average users in waiting line
        self.st = 0  # Service Time
        self.delays = [] # Store the delay times experienced by clients in the system
        self.delayed = [] # Track the arrival times of clients who experienced delay

        # delay_w will update by summing the delay times of clients in self.delays who also exist in self.delayed
        self.delay_w = 0 # total delay time of clients who experienced delay

        # st_w will update by summing the service times of clients in temp_st.
        self.st_w = 0 # total service time of clients who experienced delay
        self.count = 0 # tracks of the number of clients who experienced delay
        self.dep_w = 0 # tracks of the number of clients who experienced delay and have departed from the system.


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
class Server(object):

    # constructor
    def __init__(self):
        # whether the server is idle or not
        self.idle = True


# ******************************************************************************
# Arrivals
# *********************************************************************
def arrival(time, FES, queue):
    global users
    global in_service
    global loss

    # cumulate statistics
    data.arr += 1
    data.utq += ((users) - (in_service)) * (time - data.oldT)
    data.ut += (users) * (time - data.oldT)
    data.oldT = time


    inter_arrival = random.expovariate(lambd=1.0 / ARRIVAL)
    

    FES.put((time + inter_arrival, "Arrival"))
    if len(queue) < Buffer_size:
        users += 1
        client = Client(TYPE1, time)
        queue.append(client)
        data.delayed.append(client.arrival_time)

        if users == 1:
            data.delayed.remove(client.arrival_time)
            data.count += 1

            # sample the service time
            service_time = random.expovariate(1.0 / SERVICE)
            FES.put((time + service_time, "Departure"))

            in_service += 1

    else:
        loss += 1


# ******************************************************************************
# Departures
# *******************************************************************
def departure(time, FES, queue):
    global users
    global delay
    global in_service # keeps track of the number of clients currently being served by the server.
    global busy_time

    data.dep += 1
    data.ut += users * (time - data.oldT)
    data.utq += (users - in_service) * (time - data.oldT)
    data.oldT = time
    in_service -= 1
    users -= 1
    # for those who experienced delay [waiting line]ì
    if len(queue) != 0:
        # get the first element from the queue
        client = queue.pop(0)

        # do whatever we need to do when clients go away

        data.delay += (time - client.arrival_time)
        data.delays.append(time - client.arrival_time)
        # see whether there are more clients to in the line

        if client.arrival_time in data.delayed:
            data.st_w += temp_st[0]
            temp_st.pop(0)

        if users > 0:
            # sample the service time
            service_time = random.expovariate(1.0 / SERVICE)
            data.st += service_time
            temp_st.append(service_time)

            # schedule the next departure event
            FES.put((time + service_time, "Departure"))

            delay.append(time - client.arrival_time)
            busy_time += service_time

            in_service += 1


# ******************************************************************************
# The "main" of the simulation
# ******************************************************************************

import matplotlib.pyplot as plt

random.seed(50)

arrival_rates = np.arange(0.1, 1, 0.1)
average_delays = []
num_losses=[]
LOAD = 0.85
SERVICE = 10.0  # av service time
TYPE1 = 1
SIM_TIME = 500000 # simulation time

for arrival_rate in arrival_rates:
   

    ARRIVAL = SERVICE / (LOAD * arrival_rate)
    data = Measure(0, 0, 0, 0, 0)
    utq = 0  # data.ut = number of average users in waiting line
    st = 0  # Service Time
    delayed = []
    delay_w = 0
    st_w = 0
    count = 0
    dep_w = 0
    users=0
    time = 0
    

    arrivals = 0
    users = 0
    BusyServer = False  # True: server is currently busy; False: server is currently idle
    in_service = 0

    MM1 = []

    temp_st = []
    busy_time = 0
    delay = []
    loss = 0
    #Buffer_size = 10
    Buffer_size = np.inf
    FES = PriorityQueue()
    FES.put((0, "Arrival"))

    while time < SIM_TIME:
        if len(FES.queue):
            (time, event_type) = FES.get()
            if event_type == "Arrival":
                arrival(time, FES, MM1)
            elif event_type == "Departure":
                departure(time, FES, MM1)

    lambtda = round(1 / ARRIVAL, 3)
    mu = round(1 / SERVICE, 3)
    rho = round(lambtda / mu, 3)

   
    average_delay = round(data.delay / data.dep, 3)
    average_queue_delay = round(((data.delay - data.st) / data.dep), 3)

    average_delays.append(average_delay)
    num_losses.append(loss)
    

    print("Single Queue M/M/1 with Arrival Rate:", arrival_rate)
    print("\nNumber of arrivals:", data.arr)
    print("\nNumber of dropped packets:", loss)
    print("\nAverage number of packets:", round(data.ut / time, 3))
    print("\nLoss probability:", round((loss / data.arr) * 100, 3), "%")
    print("\nBusy time:", round(data.st / time * 100, 3), "%")
  

    
# Plot the average delays for different arrival rates
plt.plot(arrival_rates, average_delays, marker='o')
plt.xlabel("Arrival Rate")
plt.ylabel("Average Delay (ms)")
plt.title("Average Delay vs. Arrival Rate")
plt.show()


# In[ ]:




