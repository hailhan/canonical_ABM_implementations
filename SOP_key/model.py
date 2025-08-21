from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import AudienceMember


class SOPModel(Model):
    # model reporter helper functions
    def majority_action(self):
        # determines the majority action (standing or sitting) in the model
        standing = sum(agent.standing for agent in self.agent_list)
        sitting = len(self.agent_list) - standing
        return 1 if standing > sitting else 0  # 1=standing, 0=sitting

    def stick_in_the_muds(self):
        # calculates the proportion of agents in the minority action
        majority = self.majority_action()
        if majority == 1:
            return sum(not agent.standing for agent in self.agent_list) / len(self.agent_list)
        else:
            return sum(agent.standing for agent in self.agent_list) / len(self.agent_list)

    def informational_efficiency(self, initial_majority):
        # Returns 1 if majority matches initial, else 0
        return int(self.majority_action() == initial_majority)

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
        self.update = update
        self.neighbor_structure = neighbor_structure
        # establish grid properties
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=False)
        self.agent_list = []
        
        # initialize agents by placing them in the grid
        self.init_agents()
        
        # set up data collector to gather model statistics
        self.datacollector = DataCollector(
            model_reporters={
                "proportion_against_instinct": lambda m:m.proportion_against_instinct(),
                "majority_action": lambda m: m.majority_action(),
                "stick_in_the_muds": lambda m: m.stick_in_the_muds(),
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