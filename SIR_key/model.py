from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import SIRAgent

class SIRModel(Model):
    def __init__(self, width=20, height=20, 
                 seed=None, infection_duration=14, 
                 infected_density=0.1, vaccination=False):
        super().__init__(seed=seed)
        # establish grid properties
        self.grid = SingleGrid(width, height, torus=False)
        self.width = width
        self.height = height
        # model parameters
        self.infection_duration = infection_duration # user can play around with the length of infection
        self.infected_density = infected_density # initial density of infected agents
        self.vaccination = vaccination # whether vaccination is enabled
        # create a list to hold agents (instead of scheduler)
        self.agent_list = []

        # place agents
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.infected_density:
                agent = SIRAgent(self, 'I')
            else:
                agent = SIRAgent(self, 'S')
            self.grid.place_agent(agent, pos)
            self.agent_list.append(agent)

        # initialize data collector and model reporters
        self.datacollector = DataCollector(
            model_reporters={
                "num_susceptible": lambda m: sum(agent.state == 'S' for agent in m.agent_list),
                "num_infected": lambda m: sum(agent.state == 'I' for agent in m.agent_list),
                "num_recovered": lambda m: sum(agent.state == 'R' for agent in m.agent_list)
            }
        )
    def step(self):
        # if vaccination is enabled, vaccinate agents first thing each step
        if self.vaccination:
            for agent in self.agent_list:
                agent.vaccinate()
        # then, check for exposure and transmission
        for agent in self.agent_list:
            agent.exposure()
        for agent in self.agent_list:
            agent.transmission()
        # collect data for model reporters
        self.datacollector.collect(self)
        