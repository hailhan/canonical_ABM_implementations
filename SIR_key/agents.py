from mesa import Agent
import random

# add vaccination state and functionality later

class SIRAgent(Agent):
    def __init__(self, model, state):
        super().__init__(model)
        self.state = state
        self.days_in_state = 0
        self.exposed = None

    def exposure(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=True, include_center=False)
        if any(agent.state == 'I' for agent in neighbors):
            self.exposed = True
        else:
            self.exposed = False

    def transmission(self):
        if self.state == 'S' and self.exposed == True:
            self.state = 'I'
            self.days_in_state = 0
        elif self.state == 'I':
            self.days_in_state += 1
            if self.days_in_state >= self.model.infection_duration:
                self.state = 'R'
        else:
            self.days_in_state += 1