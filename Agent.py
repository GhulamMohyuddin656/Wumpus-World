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
                        
                # If we are on a breeze then one of its neighbors is a pit
                b_clause=[f"-b{r}{c}"]+[f"p{nr}{nc}" for nr,nc in neighbors]
                self.kb.append(set(b_clause))
                # If a neighbor is a pit then this cell has a breeze
                for nr, nc in neighbors:
                    self.kb.append({f"-p{nr}{nc}", f"b{r}{c}"})

                # If we are on a stench then one of its neighbors is the Wumpus
                s_clause=[f"-s{r}{c}"]+[f"w{nr}{nc}" for nr,nc in neighbors]
                self.kb.append(set(s_clause))
                # If a neighbor has the Wumpus then this cell has a stench
                for nr, nc in neighbors:
                    self.kb.append({f"-w{nr}{nc}", f"s{r}{c}"})
    def tell(self,type,r,c,occured):
        if occured:
            self.kb.append({f"{type}{r}{c}"})
        else:
            self.kb.append({f"-{type}{r}{c}"})
                