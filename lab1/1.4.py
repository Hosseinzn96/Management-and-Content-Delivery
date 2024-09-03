#!/usr/bin/env python
# coding: utf-8

# In[13]:



import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt


# ******************************************************************************
# Constants
# ******************************************************************************
class simulator:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.service = 1/service  # SERVICE is the average service time; service rate = 1/SERVICE
        self.arrival = 1/arrival  # ARRIVAL is the average inter-arrival time; arrival rate = 1/ARRIVAL
        self.load= self.service / self.arrival  # This relationship holds for M/M/1
        self.max_buffer_size = max_buffer_size
        self.type1 = 1
        self.sim_time = sim_time
        self.arrivals=0
        self.users=0
        self.data = None
        self.BusyServer=False # True: server is currently busy; False: server is currently idle
        self.MM1= None
        self.FES = None
        self.result = None
        self.mu = 10  # Mean for normal distribution
        self.sigma = 3  # Standard deviation for normal distribution
        random.seed(42)

    # ******************************************************************************
    # To take the measurements
    # ******************************************************************************
    class Measure:
        def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay,Drop):
            self.arr = Narr
            self.dep = Ndep
            self.ut = NAveraegUser
            self.oldT = OldTimeEvent
            self.delay = AverageDelay
            self.drop = Drop

    # ******************************************************************************
    # Client
    # ******************************************************************************
    class Client:
        def __init__(self,type,arrival_time):
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

    # arrivals *********************************************************************
    def Arrival(self,time, queue):

        #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )

        # cumulate statistics
        self.data.arr += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time

        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1.0/self.arrival)

        # schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival"))

        self.users += 1

        # create a record for the client
        client = self.Client(self.type1,time)

        # check the buffer size before adding a new packet into the MM1 queue
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            # increase the dropped packets count
            self.data.drop += 1
            self.users -= 1

        # Ensures that the server only starts serving a new client when there is exactly one user in the system and
        # the server is idle. It helps avoid scheduling duplicate departure events or attempting to serve multiple
        # clients simultaneously.
        if self.users==1:

            # sample the service time
            service_time = random.gauss(self.mu, self.sigma)   # We schedule departure according to normal distribution
            #service_time = 1 + random.uniform(0, SEVICE_TIME)

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))

    # ******************************************************************************

    # departures *******************************************************************
    def Departure(self,time, queue):
        #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )

        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time

        # get the first element from the queue
        client = queue.pop(0)

        # do whatever we need to do when clients go away

        self.data.delay += (time-client.arrival_time)
        self.users -= 1

        # see whether there are more clients to in the line
        if self.users >0:
            # sample the service time
            service_time = random.expovariate(1.0/self.service)

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))


    # ******************************************************************************
    # the "main" of the simulation
    # ******************************************************************************
    def run(self):
        self.users = 0
        self.result= {}
        self.data = self.Measure(0,0,0,0,0,0)
        self.MM1 = []
        self.time = 0
        # the list of events in the form: (time, type)
        self.FES = None
        self.FES = PriorityQueue()
        # schedule the first arrival at t=0
        self.FES.put((0, "arrival"))
        # simulate until the simulated time reaches a constant
        while self.time < self.sim_time:
            (self.time, self.event_type) = self.FES.get()

            if self.event_type == "arrival":
                self.Arrival(self.time, self.MM1)

            elif self.event_type == "departure":
                self.Departure(self.time, self.MM1)
                

        # Create a dictionary of data related to the simulation
        self.result = {
            "No. of users in the queue": self.users,
            "No. of arrivals": self.data.arr,
            "No. of departures": self.data.dep,
            "Dropped packets": self.data.drop,
            "Loss probability": self.data.drop / self.data.arr,
            "Buffer size": self.max_buffer_size if self.max_buffer_size != float("inf") else "infinite",
            "Load": self.load,
            "Arrival rate": self.data.arr / self.time,
            "Departure rate": self.data.dep / self.time,
            "Average number of users": self.data.ut / self.time,
            "Average delay": self.data.delay / self.data.dep,
            "Actual queue size": len(self.MM1)
        }

        return self.data, self.result




def plot_graph(data1, data2, label1, label2, title):
    plt.plot(data1, data2)
    plt.xlabel(label1)
    plt.ylabel(label2)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # simulator inputs : service, arrival , sim_time, buffer_size
    packet_simulator = simulator(10,20,500000,10)
    arrival_rates  = list(range(1, 20))[:100]
    finalresult = []
    for i in arrival_rates:
        packet_simulator = simulator(10,i,500000,10)
        finalresult.append([packet_simulator.run()[1]])

    # Loss Probability vs. Arrival Rate
    loss_prob_values = [result[0]["Loss probability"] for result in finalresult]
    plot_graph(arrival_rates, loss_prob_values, "Arrival Rate", "Loss Probability", "Loss Probability of normal distribution vs. Arrival Rate")

    # Utilization vs. Arrival Rate
    utilization_values = [result[0]["Average number of users"] for result in finalresult]
    plot_graph(arrival_rates, utilization_values, "Arrival Rate", "Utilization", "Utilization of normal distribution vs. Arrival Rate")


# In[15]:


import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt


# ******************************************************************************
# Constants
# ******************************************************************************
class simulator:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.service = 1/service  # SERVICE is the average service time; service rate = 1/SERVICE
        self.arrival = 1/arrival  # ARRIVAL is the average inter-arrival time; arrival rate = 1/ARRIVAL
        self.load= self.service / self.arrival  # This relationship holds for M/M/1
        self.max_buffer_size = max_buffer_size
        self.type1 = 1
        self.sim_time = sim_time
        self.arrivals=0
        self.users=0
        self.data = None
        self.BusyServer=False # True: server is currently busy; False: server is currently idle
        self.MM1= None
        self.FES = None
        self.result = None
        self.amin = 1  # Minimum value for uniform distribution
        self.amax = 10# Maximum value for uniform distribution
        random.seed(42)

    # ******************************************************************************
    # To take the measurements
    # ******************************************************************************
    class Measure:
        def __init__(self,Narr,Ndep,NAveraegUser,OldTimeEvent,AverageDelay,Drop):
            self.arr = Narr
            self.dep = Ndep
            self.ut = NAveraegUser
            self.oldT = OldTimeEvent
            self.delay = AverageDelay
            self.drop = Drop

    # ******************************************************************************
    # Client
    # ******************************************************************************
    class Client:
        def __init__(self,type,arrival_time):
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

    # arrivals *********************************************************************
    def Arrival(self,time, queue):

        #print("Arrival no. ",data.arr+1," at time ",time," with ",users," users" )

        # cumulate statistics
        self.data.arr += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time

        # sample the time until the next event
        inter_arrival = random.expovariate(lambd=1.0/self.arrival)

        # schedule the next arrival
        self.FES.put((time + inter_arrival, "arrival"))

        self.users += 1

        # create a record for the client
        client = self.Client(self.type1,time)

        # check the buffer size before adding a new packet into the MM1 queue
        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            # increase the dropped packets count
            self.data.drop += 1
            self.users -= 1

        # Ensures that the server only starts serving a new client when there is exactly one user in the system and
        # the server is idle. It helps avoid scheduling duplicate departure events or attempting to serve multiple
        # clients simultaneously.
        if self.users==1:

            # sample the service time
            service_time = random.uniform(self.amin, self.amax)  # We schedule departure according to uniform distribution
            #service_time = 1 + random.uniform(0, SEVICE_TIME)

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))

    # ******************************************************************************

    # departures *******************************************************************
    def Departure(self,time, queue):
        #print("Departure no. ",data.dep+1," at time ",time," with ",users," users" )

        # cumulate statistics
        self.data.dep += 1
        self.data.ut += self.users*(time-self.data.oldT)
        self.data.oldT = time

        # get the first element from the queue
        client = queue.pop(0)

        # do whatever we need to do when clients go away

        self.data.delay += (time-client.arrival_time)
        self.users -= 1

        # see whether there are more clients to in the line
        if self.users >0:
            # sample the service time
            service_time = random.expovariate(1.0/self.service)

            # schedule when the client will finish the server
            self.FES.put((time + service_time, "departure"))


    # ******************************************************************************
    # the "main" of the simulation
    # ******************************************************************************
    def run(self):
        self.users = 0
        self.result= {}
        self.data = self.Measure(0,0,0,0,0,0)
        self.MM1 = []
        self.time = 0
        # the list of events in the form: (time, type)
        self.FES = None
        self.FES = PriorityQueue()
        # schedule the first arrival at t=0
        self.FES.put((0, "arrival"))
        # simulate until the simulated time reaches a constant
        while self.time < self.sim_time:
            (self.time, self.event_type) = self.FES.get()

            if self.event_type == "arrival":
                self.Arrival(self.time, self.MM1)

            elif self.event_type == "departure":
                self.Departure(self.time, self.MM1)

    

        # Create a dictionary of data related to the simulation
        self.result = {
            "No. of users in the queue": self.users,
            "No. of arrivals": self.data.arr,
            "No. of departures": self.data.dep,
            "Dropped packets": self.data.drop,
            "Loss probability": self.data.drop / self.data.arr,
            "Buffer size": self.max_buffer_size if self.max_buffer_size != float("inf") else "infinite",
            "Load": self.load,
            "Arrival rate": self.data.arr / self.time,
            "Departure rate": self.data.dep / self.time,
            "Average number of users": self.data.ut / self.time,
            "Average delay": self.data.delay / self.data.dep,
            "Actual queue size": len(self.MM1)
        }

        return self.data, self.result

   

      


def plot_graph(data1, data2, label1, label2, title):
    plt.plot(data1, data2)
    plt.xlabel(label1)
    plt.ylabel(label2)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    # simulator inputs : service, arrival , sim_time, buffer_size
    packet_simulator = simulator(10,20,500000,10)
    arrival_rates  = list(range(1, 20))[:100]
    finalresult = []
    for i in arrival_rates:
        packet_simulator = simulator(10,i,500000,10)
        finalresult.append([packet_simulator.run()[1]])

    # Loss Probability vs. Arrival Rate
    loss_prob_values = [result[0]["Loss probability"] for result in finalresult]
    plot_graph(arrival_rates, loss_prob_values, "Arrival Rate", "Loss Probability", "Loss Probability of uniform distribution vs. Arrival Rate")

    # Utilization vs. Arrival Rate
    utilization_values = [result[0]["Average number of users"] for result in finalresult]
    plot_graph(arrival_rates, utilization_values, "Arrival Rate", "Utilization", "Utilization of uniform distribution vs. Arrival Rate")

    


# In[ ]:




