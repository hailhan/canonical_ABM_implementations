from mesa import Model
from mesa.space import SingleGrid
from agents import CultureAgent

class CultureModel(Model):
    def __init__(self, width=10, height=10, seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        # establish grid properties
        self.grid = SingleGrid(width, height, torus=False)
        
        self.agent_list = []
        # place agents
        for _, pos in self.grid.coord_iter():
            agent = CultureAgent(self)
            self.grid.place_agent(agent, pos)
            self.agent_list.append(agent)

    def step(self):
        for agent in self.agent_list:
            agent.interact()