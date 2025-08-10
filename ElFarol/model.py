from mesa import Model
from mesa.space import ContinuousSpace
from agents import ElFarolAgent
import numpy as np

class ElFarolModel(Model):
    def __init__(self, N=100, memory_size=5, num_strategies=10, 
                 overcrowding_threshold=0.6, width=10, 
                 height=10, seed=None):
        super().__init__(seed=seed)
        print("ElFarolModel __init__ called")
        self.grid = ContinuousSpace(width, height, torus=False)
        #self.space = self.grid
        self.num_agents = N
        self.memory_size = memory_size
        self.num_strategies = num_strategies
        self.history = [self.random.randint(0, 100) for _ in range(2 * memory_size)]
        self.overcrowding_threshold = overcrowding_threshold
        self.attendance = 0
        
        self.agent_list = []

        # Generate unique home positions (outside upper right quadrant)
        self.homes = []
        home_grid_size = int(np.ceil(np.sqrt(self.num_agents)))
        home_spacing_x = (width // 2) / home_grid_size
        home_spacing_y = height / home_grid_size
        for i in range(self.num_agents):
            gx = i % home_grid_size
            gy = i // home_grid_size
            home_x = gx * home_spacing_x + self.random.uniform(0, home_spacing_x * 0.5)
            home_y = gy * home_spacing_y + self.random.uniform(0, home_spacing_y * 0.5)
            self.homes.append((home_x, home_y))

        # Generate unique bar positions (upper right quadrant)
        self.bar = []
        bar_grid_size = int(np.ceil(np.sqrt(self.num_agents)))
        bar_spacing_x = (width // 2) / bar_grid_size
        bar_spacing_y = (height // 2) / bar_grid_size
        for i in range(self.num_agents):
            gx = i % bar_grid_size
            gy = i // bar_grid_size
            bar_x = (width // 2) + gx * bar_spacing_x + self.random.uniform(0, bar_spacing_x * 0.5)
            bar_y = (height // 2) + gy * bar_spacing_y + self.random.uniform(0, bar_spacing_y * 0.5)
            self.bar.append((bar_x, bar_y))

        # Assign each agent a unique home and bar position
        for i in range(self.num_agents):
            home_pos = self.homes[i]
            bar_pos = self.bar[i]
            strategies = [self.random_strategy() for _ in range(self.num_strategies)]
            agent = ElFarolAgent(self, strategies, home_pos, bar_pos)
            self.agent_list.append(agent)
            self.grid.place_agent(agent, home_pos)

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