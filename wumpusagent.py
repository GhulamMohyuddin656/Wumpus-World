class WumpusAgent:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.kb = []
        self.visited = set()
        self.safe_known = set([(0,0)])
        self.inference_steps = 0  # Tracks resolution steps for the dashboard
        self.add_initial_rules()

    def add_initial_rules(self):
        for r in range(self.row):
            for c in range(self.col):
                neighbors = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.row and 0 <= nc < self.col:
                        neighbors.append((nr, nc))
                
                # Breeze rules
                b_clause = [f"-b{r}{c}"] + [f"p{nr}{nc}" for nr, nc in neighbors]
                self.kb.append(frozenset(b_clause))
                for nr, nc in neighbors:
                    self.kb.append(frozenset([f"-p{nr}{nc}", f"b{r}{c}"]))

                # Stench rules
                s_clause = [f"-s{r}{c}"] + [f"w{nr}{nc}" for nr, nc in neighbors]
                self.kb.append(frozenset(s_clause))
                for nr, nc in neighbors:
                    self.kb.append(frozenset([f"-w{nr}{nc}", f"s{r}{c}"]))

    def tell(self, type_str, r, c, occurred):
        fact = f"{type_str}{r}{c}" if occurred else f"-{type_str}{r}{c}"
        new_clause = frozenset([fact])
        if new_clause not in self.kb:
            self.kb.append(new_clause)

    def resolve(self, ci, cj):
        self.inference_steps += 1 # Count every resolution attempt
        for literal in ci:
            complement = literal[1:] if literal.startswith("-") else "-" + literal
            if complement in cj:
                res = set(ci) | set(cj)
                res.remove(literal)
                res.remove(complement)
                return frozenset(res)
        return None

    def prove(self, query):
        negated_query = query[1:] if query.startswith("-") else "-" + query
        clauses = list(self.kb)
        clauses.append(frozenset([negated_query]))
        new_clauses = set()
        
        while True:
            n = len(clauses)
            for i in range(n):
                for j in range(i + 1, n):
                    resolvent = self.resolve(clauses[i], clauses[j])
                    if resolvent is not None:
                        if len(resolvent) == 0:
                            return True
                        new_clauses.add(resolvent)
            
            if new_clauses.issubset(set(clauses)):
                return False
            for c in new_clauses:
                if c not in clauses:
                    clauses.append(c)

    def ask_is_safe(self, r, c):
        if (r,c) in self.safe_known:
            return True
        no_pit = self.prove(f"-p{r}{c}")
        no_wumpus = self.prove(f"-w{r}{c}")
        if no_pit and no_wumpus:
            self.safe_known.add((r,c))
            return True
        return False