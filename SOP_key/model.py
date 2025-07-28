from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import AudienceMember


class SOPModel(Model):
    update_order = ["Sync", "AsyncRandom", "AsyncIncentive"] # define possible update orders
    
    def init_agents(self):
        # initialize agents in the grid
        agent_id = 0
        for x in range(self.width):
            for y in range(self.height):
                agent = AudienceMember(
                    self,
                    self.neighbor_structure
                    )
                self.grid.place_agent(agent, (x, y))
                self.agent_list.append(agent)
                agent_id += 1

        for agent, (x, y) in self.grid.coord_iter():
            agent.get_neighbors()

    def __init__(self, width=20, height=20, update="Sync", neighbor_structure="five", seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.update = update
        self.neighbor_structure = neighbor_structure
        # establish grid properties
        self.grid = SingleGrid(width, height, torus=False)
        self.agent_list = []  # Renamed to avoid conflict with Mesa internals
        
        # initialize agents by placing them in the grid
        self.init_agents()
        
        # set up data collector to gather model statistics
        self.datacollector = DataCollector(
            model_reporters={
                "proportion_against_instinct": lambda m:m.proportion_against_instinct()
            }
        )

    def proportion_against_instinct(self):
        # measures the proportion of agents that are acting opposite their enjoyment (for data collection)
        total = len(self.agent_list)
        if total == 0:
           return 0
        against_instinct = sum(
            (agent.enjoyment < 0.5 and agent.standing) or
            (agent.enjoyment > 0.5 and not agent.standing)
            for agent in self.agent_list
            )
        return against_instinct / total

    def step(self):
        # execute the model step based on the update order
        if self.update == "Sync":
            # synchronous update: all agents evaluate and update their state at the same time
            for agent in self.agent_list:
                agent.determine_new_state()
            for agent in self.agent_list:
                agent.update_state()
        elif self.update == "AsyncRandom":
            # asynchronous random update: agents are shuffled and updated one by one
            shuffled_agents = self.random.sample(self.agent_list, len(self.agent_list))
            for agent in shuffled_agents:
                agent.step()
        elif self.update == "AsyncIncentive":
            # asynchronous incentive update: agents are sorted by dissatisfaction and updated in that order
            sorted_agents = sorted(
                self.agent_list, key=lambda a: a.dissatisfaction(), reverse=True
            )
            for agent in sorted_agents:
                agent.step()
        # collect data after each step
        self.datacollector.collect(self)