from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import TreeAgent

class ForestFireModel(Model):
    def __init__(self, width=10, height=10, p=0.6, seed=None):
        super().__init__(seed=seed)
        # initialize grid
        self.grid = SingleGrid(width, height, torus=False)
        self.width = width
        self.height = height
        # initialize parameters
        self.p = p # probability of a cell being Tree
        self.agent_list = []
        self.running = True
   
        # initialize data collector and model reporters
        self.datacollector = DataCollector(
            model_reporters={ # proportion of trees that are burning at a given time (relative to all trees)
                "burned_prop": lambda m: (sum(agent.state == "Burning" for agent in m.agent_list) /
                                          (sum(agent.state != "Empty" for agent in m.agent_list) + 1e-5)
                                          )
                                          }
                                         )
        
        # place agents on the grid
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.p:
                agent = TreeAgent(self, 'Tree')
            else:
                agent = TreeAgent(self, 'Empty')
            self.grid.place_agent(agent, pos)
            self.agent_list.append(agent)
        # set center tree on fire always
        center_pos = (self.width // 2, self.height // 2)
        for agent in self.grid.get_cell_list_contents(center_pos):
            agent.state = 'Burning'

    def step(self):
        for agent in self.agent_list:
            agent.on_fire() # find next state for all agents
        changes = 0
        for agent in self.agent_list:
            if agent.advance():
                changes += 1 # count number of state changes
        # collect data and update model state
        self.datacollector.collect(self)
        if changes == 0: # stop model if no changes between steps
            self.running = False