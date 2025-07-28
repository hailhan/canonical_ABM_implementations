from mesa import Model
from mesa.space import SingleGrid
from agents import SIRAgent

class SIRModel(Model):
    def __init__(self, width=20, height=20, seed=None, infection_duration=14, infected_density=0.1):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.infection_duration = infection_duration
        self.infected_density = infected_density
        # establish grid properties
        self.grid = SingleGrid(width, height, torus=False)
        
        self.agent_list = []
        # place agents
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.infected_density:
                agent = SIRAgent(self, 'I')
            else:
                agent = SIRAgent(self, 'S')
            self.grid.place_agent(agent, pos)
            self.agent_list.append(agent)

    def step(self):
        for agent in self.agent_list:
            agent.exposure()
        for agent in self.agent_list:
            agent.transmission()
        