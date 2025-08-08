from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import ElFarolAgent
import random

class ElFarolModel(Model):
    def __init__(self, N=100, memory_size=5, num_strategies=10, 
                 overcrowding_threshold=0.6, width=10, 
                 height=10, seed=None):
        super().__init__(seed=seed)
        self.num_agents = N
        self.memory_size = memory_size
        self.num_strategies = num_strategies
        self.history = [random.randint(0, 100) for _ in range(2 * memory_size)]
        self.overcrowding_threshold = overcrowding_threshold
        self.grid = MultiGrid(width, height, torus=False)
        self.width = width
        self.height = height
        
        self.agent_list = []

        # Define home and bar patches
        self.homes = [(x, y) for x in range(width) for y in range(height)
                             if y < height // 2 or (x < width // 2 and y >= height // 2)]
        self.bar = [(x, y) for x in range(width) for y in range(height)
                            if x > width // 2 and y > height // 2]
        
        # Create agents
        for i in range(self.num_agents):
            strategies = [self.random_strategy() for _ in range(self.num_strategies)]
            agent = ElFarolAgent(self, strategies)
            self.agent_list.append(agent)
            pos = self.random.choice(self.homes) # give the agent a random home
            self.grid.place_agent(agent, pos)
        self.running = True

    def random_strategy(self):
        return [1.0 - self.random.random() * 2.0 for _ in range(self.memory_size + 1)]
    
    def step(self):
        self.attendance = 0  # reset count

        # PHASE 1: Think (prediction + decision)
        for agent in self.agent_list:
            agent.predict()

        # PHASE 2: Act (move + count attendance)
        for agent in self.agent_list:
            agent.advance()

        # Update history
        self.history = [self.attendance] + self.history[:-1]