# CONSOLIDATE COORDINATE GENERATION INTO FUNCTION
from mesa import Model
from mesa.space import ContinuousSpace
from agents import ElFarolAgent
import numpy as np

class ElFarolModel(Model):
    def __init__(self, N=100, memory_size=5, num_strategies=10, 
                 width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.grid = ContinuousSpace(width, 
                                    height, 
                                    torus=False)
        self.num_agents = N
        self.memory_size = memory_size
        self.num_strategies = num_strategies
        self.history = [self.random.randint(0, 100) 
                        for _ in range(2 * memory_size)]
        self.attendance = 0
        
        self.agent_list = []

        # Generate homes in left half and lower right quadrant
        num_left = (self.num_agents // 3) * 2 # ensure even distribution of agents in each home quadrant
        num_lower_right = self.num_agents - num_left
        
        self.homes = []
        
        # Left half homes (x: 0 to width//2, y: 0 to height)
        home_grid_size_left = int(np.ceil(np.sqrt(num_left)))
        home_spacing_x_left = (width // 2) / home_grid_size_left
        home_spacing_y_left = height / home_grid_size_left
        for i in range(num_left):
            gx = i % home_grid_size_left
            gy = i // home_grid_size_left
            home_x = gx * home_spacing_x_left + self.random.uniform(
                0, home_spacing_x_left * 0.5)
            home_y = gy * home_spacing_y_left + self.random.uniform(
                0, home_spacing_y_left * 0.5)
            self.homes.append((home_x, home_y))
        
        # Lower right quadrant homes (x: width//2 to width, y: 0 to height//2)
        home_grid_size_right = int(np.ceil(np.sqrt(num_lower_right)))
        home_spacing_x_right = (width // 2) / home_grid_size_right
        home_spacing_y_right = (height // 2) / home_grid_size_right
        for i in range(num_lower_right):
            gx = i % home_grid_size_right
            gy = i // home_grid_size_right
            home_x = (width // 2) + gx * home_spacing_x_right + self.random.uniform(
                0, home_spacing_x_right * 0.5)
            home_y = gy * home_spacing_y_right + self.random.uniform(
                0, home_spacing_y_right * 0.5)
            self.homes.append((home_x, home_y))

        # Generate bar positions (upper right quadrant)
        self.bar = []
        bar_grid_size = int(np.ceil(np.sqrt(self.num_agents)))
        bar_spacing_x = (width // 2) / bar_grid_size
        bar_spacing_y = (height // 2) / bar_grid_size
        for i in range(self.num_agents):
            gx = i % bar_grid_size
            gy = i // bar_grid_size
            bar_x = (width // 2) + gx * bar_spacing_x + self.random.uniform(
                0, bar_spacing_x * 0.5)
            bar_y = (height // 2) + gy * bar_spacing_y + self.random.uniform(
                0, bar_spacing_y * 0.5)
            self.bar.append((bar_x, bar_y))

        # Create agents with assigned home and bar positions
        for i in range(self.num_agents):
            home_pos = self.homes[i]
            bar_pos = self.bar[i]
            strategies = [self.random_strategy() 
                          for _ in range(self.num_strategies)]
            agent = ElFarolAgent(self, strategies, home_pos, bar_pos)
            self.agent_list.append(agent)
            self.grid.place_agent(agent, home_pos)

    def random_strategy(self):
        return [1.0 - self.random.random() * 2.0 
                for _ in range(self.memory_size + 1)]
    
    def step(self):
        self.attendance = 0  # reset count

        # PHASE 1: Think (prediction + decision)
        for agent in self.agent_list:
            agent.decide()

        # PHASE 2: Act (move + count attendance)
        for agent in self.agent_list:
            agent.advance()

        # Update history
        self.history = [self.attendance] + self.history[:-1]