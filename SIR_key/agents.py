from mesa import Agent
import random

class SIRAgent(Agent):
    def __init__(self, model, state):
        super().__init__(model)
        self.state = state # each agent has one of four disease states: 'S', 'I', 'R', or 'V'
        self.days_in_state = 0 # how many days the agent has been in the current state
        self.exposed = None # whether the agent has been exposed to the disease (ie. has an infected neighbor)
        self.vax_willingness = model.random.uniform(0, 1)  # willingness to get vaccinated (closer to 1 means more likely to vaccinate)

    def vaccinate(self):
        # if the agent is susceptible and their vaccine willingess is greater than a random number, they become vaccinated
        if self.state == 'S' and self.vax_willingness > self.model.random.random():
            # the higher the willingness, the greater the probability of vaccination
            self.state = 'V'

    def exposure(self):
        # susceptible agents are exposed to the disease if any of their neighbors are infected
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        if any(agent.state == 'I' for agent in neighbors):
            self.exposed = True
        else:
            self.exposed = False

    def transmission(self):
        if self.state == 'S' and self.exposed == True:
            self.state = 'I' # agents who are exposed always become infected
            self.days_in_state = 0 # state count resets with state change
        elif self.state == 'I':
            self.days_in_state += 1
            if self.days_in_state >= self.model.infection_duration:
                self.state = 'R' # agents recover after a certain number of days in the infected state
                self.days_in_state = 0 # reset the days in state count
        else: # 'R' and 'V' states do not change, so we just increment the days in state
            self.days_in_state += 1