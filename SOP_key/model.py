from mesa import Model
from mesa.space import SingleGrid
from agents import AudienceMember


class SOPModel(Model):
    update_order = ["Sync", "AsyncRandom", "AsyncIncentive"]
    
    def __init__(self, width=20, height=20, update="Sync", neighbor_structure="five", seed=None):
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.update = update
        self.neighbor_structure = neighbor_structure
        # establish grid properties
        self.grid = SingleGrid(width, height, torus=False)
        self.agent_list = []  # Renamed to avoid conflict with Mesa internals

        self.init_agents()

    def init_agents(self):
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

    def step(self):
        
        if self.update == "Sync":
            for agent in self.agent_list:
                agent.determine_new_state()
            for agent in self.agent_list:
                agent.update_state()

        elif self.update == "AsyncRandom":
            shuffled_agents = self.random.sample(self.agent_list, len(self.agent_list))
            for agent in shuffled_agents:
                agent.step()

        elif self.update == "AsyncIncentive":
            sorted_agents = sorted(
                self.agent_list, key=lambda a: a.dissatisfaction(), reverse=True
            )
            for agent in sorted_agents:
                agent.step()
