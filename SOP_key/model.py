from mesa import Model
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector
from agents import AudienceMember

class SOPModel(Model):
    
    def __init__(self, width=20, height=20, update="Sync", neighbor_structure="five", seed=None):
        super().__init__(seed=seed)
        self.update = update
        self.structure = neighbor_structure
        # establish grid properties
        self.width = width
        self.height = height
        self.grid = SingleGrid(width, height, torus=False)
        self.agent_list = []
        
        # equilibrium tracking
        self.num_ticks_to_steady = None
        self.steady_state_reached = False
        self.previous_states = []
        self.SM = None
        self.IE = None

        # initialize agents by placing them in the grid
        self.init_agents()

        # store initial majority action for IE
        self.initial_majority = self.get_majority_action()

        # set up data collector to gather model statistics
        self.datacollector = DataCollector(
            model_reporters={
                "proportion_against_instinct": lambda m: m.proportion_against_instinct(),
                "NI": lambda m: m.num_ticks_to_steady,
                "SM": lambda m: m.SM,
                "IE": lambda m: m.IE,
            }
        )
        self.running = True  # model is running by default
    
    def init_agents(self):
        # initialize and place agents on the grid
        for x in range(self.width):
            for y in range(self.height):
                agent = AudienceMember(
                    self,
                )
                self.grid.place_agent(agent, (x, y))
                self.agent_list.append(agent)

        for agent, (x, y) in self.grid.coord_iter():
            agent.get_neighbors()

    def proportion_against_instinct(self): # for data collection
        # calculate the proportion of agents acting against their instinct
        total = len(self.agent_list)
        if total == 0:
            return 0
        against_instinct = sum(
            (agent.enjoyment < 0.5 and agent.standing) or
            (agent.enjoyment > 0.5 and not agent.standing)
            for agent in self.agent_list
        )
        return against_instinct / total

    def get_majority_action(self): # for equilibrium checks
        standing_count = sum(agent.standing for agent in self.agent_list)
        return 1 if standing_count >= len(self.agent_list) / 2 else 0

    def check_equilibrium(self):
        # detect steady state or cycles and compute NI, SM, and IE if steady state is reached
        current_state = tuple(agent.standing for agent in self.agent_list)
        if current_state in self.previous_states:
            if not self.steady_state_reached:
                self.num_ticks_to_steady = len(self.previous_states)
                self.steady_state_reached = True

                # compute SM: % of agents doing opposite of majority in steady state
                majority = self.get_majority_action()  # majority in steady state
                if majority == 1:  # majority is standing
                    opposite_count = sum(not agent.standing for agent in self.agent_list)
                else:  # majority is sitting
                    opposite_count = sum(agent.standing for agent in self.agent_list)
                self.SM = opposite_count / len(self.agent_list)

                # compute IE: % of time steady-state majority matches initial majority
                self.IE = 1.0 if self.initial_majority == majority else 0.0

                # stop the model if steady state is reached
                self.running = False

        self.previous_states.append(current_state)

    def step(self):
        # execute the model step based on the update order
        if self.update == "Sync":
            # determine state before updating
            for agent in self.agent_list:
                agent.determine_new_state()
            for agent in self.agent_list:
                agent.update_state()
        elif self.update == "AsyncRandom":
            # determine state and update at same time, in random order
            shuffled_agents = self.random.sample(self.agent_list, len(self.agent_list))
            for agent in shuffled_agents:
                agent.determine_update()
        elif self.update == "AsyncIncentive":
            # determine state and update at same time, sorted by dissonance
            sorted_agents = sorted(
                self.agent_list, key=lambda a: a.dissonance(), reverse=True
            )
            for agent in sorted_agents:
                agent.determine_update()

        # check for equilibrium
        self.check_equilibrium()

        # collect data
        self.datacollector.collect(self)