from mesa import Agent

class TreeAgent(Agent):
    def __init__(self, model, state):
        super().__init__(model)
        self.state = state  # possible states: 'Tree', 'Burning', 'Empty'
        self.next_state = state

    def on_fire(self):
        # check if Trees have a burning neighbor; if so, set next state to 'Burning'
        if self.state =='Tree':
            neighbors = self.model.grid.get_neighbors( # have to recalculate neighbors every step to account for state changes
                self.pos,
                moore=False, # cardinal directions only
                include_center=False
            )
            for neighbor in neighbors:
                if neighbor.state == 'Burning':
                    self.next_state = 'Burning'
                    return
    
    def advance(self):
        # update agent state if necessary
        changed = self.state != self.next_state
        self.state = self.next_state
        return changed