from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import CultureAgent

class CultureModel(Model):
    def __init__(self, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        # establish grid properties
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=False)
        # create a list to hold agents
        self.agent_list = []
        
        # place agents
        for _, pos in self.grid.coord_iter():
            agent = CultureAgent(self)
            self.grid.place_agent(agent, pos)
            self.agent_list.append(agent)
        # initialize data collector and model reporters
        self.datacollector = DataCollector(
            model_reporters={
                "region_counts": lambda m: m.count_regions()
                }
                )
    
    def count_regions(self):
        # function for data collection to count cultural regions
        visited = set()
        regions = 0
        
        def dfs(pos, target_features):
            # sub-function to perform depth-first search (DFS) to count regions
            stack = [pos] # stack structures region count procedure
            while stack:
                current = stack.pop()
                if current in visited:
                    continue # if already visited, skip this agent
                agent = self.grid.get_cell_list_contents([current])[0]
                if agent.features != target_features:
                    continue # if features don't match, skip this agent
                visited.add(current)
                neighbors = self.grid.get_neighborhood(current, 
                                                       moore=True, # includes diagonal neighbors
                                                       include_center=False
                                                       )
                stack.extend([n for n in neighbors if n not in visited])

        for x in range(self.width):
            for y in range(self.height):
                pos = (x, y)
                if pos in visited:
                    continue
                agent = self.grid.get_cell_list_contents([pos])[0]
                dfs(pos, agent.features)
                regions += 1 # once DFS completes, add new region to count
        return regions
    
    def step(self):
        for agent in self.agent_list:
            # run interaction for each agent
            agent.interact()
        # collect data after each step
        self.datacollector.collect(self)