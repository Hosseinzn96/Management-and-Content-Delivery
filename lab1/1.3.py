#!/usr/bin/env python
# coding: utf-8

# In[5]:


import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt


# ******************************************************************************
# Constants
# ******************************************************************************
#!/usr/bin/python3
class Simulator:
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
        self.MM1= None
        self.FES = None
        self.result = None
        self.time = None
        random.seed(50)

    class Measure:
        def __init__(self):
            self.arr = 0
            self.dep = 0
            self.ut = 0
            self.oldT = 0
            self.delay = 0
            self.drop = 0

    class Client:
        def __init__(self, type, arrival_time):
            self.type = type
            self.arrival_time = arrival_time

    class Server:
        def __init__(self, service_time):
            self.idle = True
            self.users = 0
            self.service_time = service_time

    def Arrival(self, time, queue, server_obj):
        server_obj.users += 1

        self.data.arr += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        inter_arrival = random.expovariate(lambd=1.0 / self.arrival)
        self.FES.put((time + inter_arrival, "arrival"))

        client = self.Client(self.type1, time)

        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            self.data.drop += 1
            server_obj.users -= 1

        if server_obj.idle:
            server_obj.idle = False

            service_time = random.expovariate(1.0 / self.service)

            self.FES.put((time + service_time, "departure", server_obj))

    def Departure(self, time, queue, server_obj):
        self.data.dep += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        if len(queue) > 0:
            client = queue.pop(0)

            self.data.delay += (time - client.arrival_time)
            server_obj.users -= 1

            if server_obj.users > 0:
                service_time = random.expovariate(1.0 / self.service)
                self.FES.put((time + service_time, "departure", server_obj))
            else:
                server_obj.idle = True
        else:
            server_obj.idle = True

    def run(self):
        self.data = self.Measure()
        self.result = {}
        self.MM1 = []
        self.time = 0
        self.FES = PriorityQueue()
        self.Server1 = self.Server(self.service * 0.8)
        self.Server2 = self.Server(self.service)
        self.Server3 = self.Server(self.service * 1.2)
        self.Server4 = self.Server(self.service * 1.4)
        self.FES.put((0, "arrival"))

        while self.time < self.sim_time:
            (self.time, self.event_type, *server_obj) = self.FES.get()

            self.servers = [self.Server1, self.Server2, self.Server3, self.Server4]
            if self.event_type == "arrival":
                selected_server = random.choice(self.servers)
                self.Arrival(self.time, self.MM1, selected_server)
            elif self.event_type == "departure":
                self.Departure(self.time, self.MM1, server_obj[0])

        self.users = self.Server1.users + self.Server2.users + self.Server3.users + self.Server4.users



        

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
    packet_simulator = Simulator(10,20,50000,10)
    arrival_rates  = list(range(1, 15))[:100]
    finalresult = []
    for i in arrival_rates:
        packet_simulator = Simulator(10,i,500000,10)
        finalresult.append([packet_simulator.run()[1]])

   
    # Utilization vs. Arrival Rate
    utilization_values = [result[0]["Average number of users"] for result in finalresult]
    plot_graph(arrival_rates, utilization_values, "Arrival Rate", "Utilization", "Utilization of random assignment vs. Arrival Rate")
    
     #Loss Probability vs. Arrival Rate
    loss_prob_values = [result[0]["Loss probability"] for result in finalresult]
    plot_graph(arrival_rates, loss_prob_values, "Arrival Rate", "Loss Probability", "Loss Probability of random assignment vs. Arrival Rate")
   


# In[7]:



import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt


# ******************************************************************************
# Constants
# ******************************************************************************
#!/usr/bin/python3
class Simulator:
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
        self.MM1= None
        self.FES = None
        self.result = None
        self.time = None
        random.seed(42)

    class Measure:
        def __init__(self):
            self.arr = 0
            self.dep = 0
            self.ut = 0
            self.oldT = 0
            self.delay = 0
            self.drop = 0

    class Client:
        def __init__(self, type, arrival_time):
            self.type = type
            self.arrival_time = arrival_time

    class Server:
        def __init__(self, service_time):
            self.idle = True
            self.users = 0
            self.service_time = service_time

    def Arrival(self, time, queue, server_obj):
        server_obj.users += 1

        self.data.arr += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        inter_arrival = random.expovariate(lambd=1.0 / self.arrival)
        self.FES.put((time + inter_arrival, "arrival"))

        client = self.Client(self.type1, time)

        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            self.data.drop += 1
            server_obj.users -= 1

        if server_obj.idle:
            server_obj.idle = False

            service_time = random.expovariate(1.0 / self.service)

            self.FES.put((time + service_time, "departure", server_obj))

    def Departure(self, time, queue, server_obj):
        self.data.dep += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        if len(queue) > 0:
            client = queue.pop(0)

            self.data.delay += (time - client.arrival_time)
            server_obj.users -= 1

            if server_obj.users > 0:
                service_time = random.expovariate(1.0 / self.service)
                self.FES.put((time + service_time, "departure", server_obj))
            else:
                server_obj.idle = True
        else:
            server_obj.idle = True

    def run(self):
        self.data = self.Measure()
        self.result = {}
        self.MM1 = []
        self.time = 0
        self.FES = PriorityQueue()
        self.Server1 = self.Server(self.service * 0.8)
        self.Server2 = self.Server(self.service)
        self.Server3 = self.Server(self.service * 1.2)
        self.Server4 = self.Server(self.service * 1.4)
        self.servers = [self.Server1, self.Server2, self.Server3, self.Server4]
        self.last_assigned_server = -1
        self.FES.put((0, "arrival"))

        while self.time < self.sim_time:
            (self.time, self.event_type, *server_obj) = self.FES.get()

            if self.event_type == "arrival":
                self.last_assigned_server = (self.last_assigned_server + 1) % len(self.servers)
                selected_server = self.servers[self.last_assigned_server]
                self.Arrival(self.time, self.MM1, selected_server)
            elif self.event_type == "departure":
                self.Departure(self.time, self.MM1, server_obj[0])

        self.users = self.Server1.users + self.Server2.users + self.Server3.users + self.Server4.users

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
    packet_simulator = Simulator(10,20,50000,10)
    arrival_rates  = list(range(1, 15))[:100]
    finalresult = []
    for i in arrival_rates:
        packet_simulator = Simulator(10,i,500000,10)
        finalresult.append([packet_simulator.run()[1]])

   
    # Utilization vs. Arrival Rate
    utilization_values = [result[0]["Average number of users"] for result in finalresult]
    plot_graph(arrival_rates, utilization_values, "Arrival Rate", "Utilization", "Utilization of round robin vs. Arrival Rate")
     # Loss Probability vs. Arrival Rate
    loss_prob_values = [result[0]["Loss probability"] for result in finalresult]
    plot_graph(arrival_rates, loss_prob_values, "Arrival Rate", "Loss Probability", "Loss Probability of fastest server vs. Arrival Rate")


# In[6]:



import random
from queue import Queue, PriorityQueue
import matplotlib.pyplot as plt


# ******************************************************************************
# Constants
# ******************************************************************************
#!/usr/bin/python3
class Simulator:
    def __init__(self, service, arrival, sim_time, max_buffer_size = float('inf')):
        self.service = 1/service  # In this scenario, service time is varying based on the servers, so it is not used
        self.arrival = 1/arrival  # ARRIVAL is the average inter-arrival time; arrival rate = 1/ARRIVAL
        self.load= self.service / self.arrival  # This relationship holds for M/M/1
        self.max_buffer_size = max_buffer_size
        self.type1 = 1
        self.sim_time = sim_time
        self.arrivals=0
        self.users=0
        self.data = None
        self.MM1= None
        self.FES = None
        self.result = None
        self.time = None
        random.seed(42)

    class Measure:
        def __init__(self):
            self.arr = 0
            self.dep = 0
            self.ut = 0
            self.oldT = 0
            self.delay = 0
            self.drop = 0

    class Client:
        def __init__(self, type, arrival_time):
            self.type = type
            self.arrival_time = arrival_time

    class Server:
        def __init__(self, service_time):
            self.idle = True
            self.users = 0
            self.service_time = service_time

    def Arrival(self, time, queue, server_obj):
        server_obj.users += 1

        self.data.arr += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        inter_arrival = random.expovariate(lambd=1.0 / self.arrival)
        self.FES.put((time + inter_arrival, "arrival"))

        client = self.Client(self.type1, time)

        if len(queue) < self.max_buffer_size:
            queue.append(client)
        else:
            self.data.drop += 1
            server_obj.users -= 1

        if server_obj.idle:
            server_obj.idle = False

            service_time = random.expovariate(1.0 / self.service)

            self.FES.put((time + service_time, "departure", server_obj))

    def Departure(self, time, queue, server_obj):
        self.data.dep += 1
        self.data.ut += server_obj.users * (time - self.data.oldT)
        self.data.oldT = time

        if len(queue) > 0:
            client = queue.pop(0)

            self.data.delay += (time - client.arrival_time)
            server_obj.users -= 1

            if server_obj.users > 0:
                service_time = random.expovariate(1.0 / server_obj.service_time)
                self.FES.put((time + service_time, "departure", server_obj))
            else:
                server_obj.idle = True
        else:
            server_obj.idle = True

    def run(self):
        self.data = self.Measure()
        self.result = {}
        self.MM1 = []
        self.time = 0
        self.FES = PriorityQueue()
        self.Server1 = self.Server(self.service * 0.8)
        self.Server2 = self.Server(self.service)
        self.Server3 = self.Server(self.service * 1.2)
        self.Server4 = self.Server(self.service * 1.4)
        self.servers = [self.Server1, self.Server2, self.Server3, self.Server4]
        self.last_assigned_server = -1
        self.FES.put((0, "arrival"))

        while self.time < self.sim_time:
            (self.time, self.event_type, *server_obj) = self.FES.get()

            if self.event_type == "arrival":
                # Find the server with the minimum service time
                selected_server = min(self.servers, key=lambda s: s.service_time if s.idle else float('inf'))

                # If all servers are busy, choose the next one according to their order
                if not selected_server.idle:
                    self.last_assigned_server = (self.last_assigned_server + 1) % len(self.servers)
                    selected_server = self.servers[self.last_assigned_server]

                self.Arrival(self.time, self.MM1, selected_server)
            elif self.event_type == "departure":
                self.Departure(self.time, self.MM1, server_obj[0])

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



if __name__ == "__main__":
    # simulator inputs : service, arrival , sim_time, buffer_size
    packet_simulator = Simulator(10,20,50000,10)
    arrival_rates  = list(range(1, 15))[:100]
    finalresult = []
    for i in arrival_rates:
        packet_simulator = Simulator(10,i,500000,10)
        finalresult.append([packet_simulator.run()[1]])

  
    # Utilization vs. Arrival Rate
    utilization_values = [result[0]["Average number of users"] for result in finalresult]
    plot_graph(arrival_rates, utilization_values, "Arrival Rate", "Utilization", "Utilization of fastest server vs. Arrival Rate")

  # Loss Probability vs. Arrival Rate
    loss_prob_values = [result[0]["Loss probability"] for result in finalresult]
    plot_graph(arrival_rates, loss_prob_values, "Arrival Rate", "Loss Probability", "Loss Probability of round robin vs. Arrival Rate")


# In[ ]:




