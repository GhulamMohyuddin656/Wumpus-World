import random

class WumpusAgent:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.kb=[]
        self.visited=set()
        self.add_initial_rules()
        
    def add_initial_rules(self):
        for r in range(self.row):
            for c in range(self.col):
                
                # Get neighbors for the logic rules
                neighbors = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.row and 0 <= nc < self.col:
                        neighbors.append((nr, nc))
                        
                