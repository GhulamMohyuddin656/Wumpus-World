import random

class WumpusAgent:
    def __init__(self,size):
        self.size=size
        self.kb=[]
        self.visited=set()
        self.add_initial_rules()
        