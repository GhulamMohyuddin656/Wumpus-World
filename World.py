import random
class WumpusWorld:
    def __init__(self,row,col):
        self.row=row
        self.col=col
        self.grid=[[{"p":False,"w":False,"b":False,"s":False,"g":False,"gt":False} for _ in range (col)] for _ in range(row)]
        self.placeHazards()
        self.generate_percepts()
        self.add_gold()
        
        
    def placeHazards(self):
        #1 Place Wumpus
        Wumpus_placed=False
        while not Wumpus_placed:
            r,c=random.randint(0,self.row-1),random.randint(0,self.col-1)
            if (r,c) not in [(0,0),(0,1),(1,0)]:
                self.grid[r][c]["w"]=True
                Wumpus_placed=True
        #2 Place Pits with 20% chance
        
        for r in range(self.row):
            for c in range(self.col):
                if (r,c) not in [(0,0),(0,1),(1,0)]:
                    if random.random()<0.2:
                        self.grid[r][c]["p"]=True
    
    def add_gold(self):
        gold_placed=False
        while not gold_placed:
            r=random.randint(0,self.row-1)
            c=random.randint(0,self.col-1)
            
            #Conditions To place Gold
            #Not pit
            #Not Wumpus
            #Not Origin
            if (r,c)!=(0,0) and not self.grid[r][c]['p'] and not self.grid[r][c]['w']:
                self.grid[r][c]['g']=True
                self.grid[r][c]['gt']=True
                gold_placed=True
    
    
    def generate_percepts(self):
        for r in range(self.row):
            for c in range(self.col):
                if self.grid[r][c]['p'] and (not self.grid[r][c]['w']):
                    
                    self.add_percept_to_neighbours(r,c,'b')
                if not self.grid[r][c]['p'] and (self.grid[r][c]['w']):
                    self.add_percept_to_neighbours(r,c,'s')
    def add_percept_to_neighbour(self,r,c,type):
        for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr,nc=r+dr,c+dc
            if 0<=nr<self.size and 0<=nr<self.size:
                self.grid[nr][nc][type]=True