import os,sys
from osbrain import Agent
import numpy as np

class DATA_SEND(Agent):
    def setup(self):
        try:
            self.j = 1
            self.each(1,'update_data')
        except:
            print("wrong....---")
            self.shutdown()
            sys.exit()

    def send_data(self, value):
        self.send('main',value, topic='Parameters_1')

    def send_data_2(self, value):
        self.send('main',value, topic='2_Parameters')

    def update_data(self):
        try:
            value = self.j
            self.send_data(value)
            value = np.random.rand()*100
            self.send_data_2(value)
            self.j = self.j + 1
        except:
            pass

