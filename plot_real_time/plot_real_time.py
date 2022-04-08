import sys
import threading
import time
import numpy as np
from osbrain import (
    Agent,
    run_agent,
    run_nameserver,
)
import matplotlib.pyplot as plt
from data_extractor import DATA_SEND


def setup_clients(addr1, ns):
    setup_agent(addr1, ns)

def setup_agent(addr, ns):
    global data_client
    data_client = run_agent('data_client', serializer = 'json')
    data_client.connect(addr, handler = {'Parameters_1':log_message, '2_Parameters': log_message_2})
    data_client.data = np.array([0])
    data_client.data_2 = np.array([0])

def log_message(agent,message):
    global data_client
    agent.data = np.append(agent.data, message)

def log_message_2(agent, message):
    global data_client
    agent.data_2 = np.append(agent.data_2, message)


class Plot_Real_Time(Agent):
    def __init__(self):
        super().__init__()
        self.fig, self.ax = plt.subplots()
        self.plot_real_time,  = self.ax.plot([],[])
        self.ns = run_nameserver(addr="127.0.0.1:8888")
        self.data_agent = run_agent('agent_data', serializer='json', base=DATA_SEND)
        self.addr1 = self.data_agent.bind('PUB', alias='main', serializer='json')
        self.run_agent_on()
        time.sleep(2)
        setup_clients(self.addr1, self.ns)
        thread_plot = threading.Thread(target=self.update_loop)
        thread_plot.daemon = True
        thread_plot.start()

    def run_agent_on(self):
        try:
            self.data_agent.after(0, 'setup')
        except:
            self.ns.shutdown()
            sys.exit()

    def update_loop(self):
        while True:
            self.update_plot()
            time.sleep(1)

    def update_plot(self):
        global data_client
        self.x = data_client.data
        self.y = data_client.data_2
        self.ax.set_ylim(np.amin(self.y), np.max(self.y))
        self.ax.set_xlim(np.amin(self.x), np.max(self.x))
        self.plot_real_time.set_data(self.x,self.y)
        plt.draw()

if __name__ == "__main__":
    Plot_Real_Time()
    plt.show()