from mesa import Agent

class AudienceMember(Agent):
    neighbor_structure = ["five", "cones"] # establish possible neighbor structures
    def __init__(self, model, neighbor_structure="five"):
        super().__init__(model)
        self.structure = neighbor_structure
        self.enjoyment = model.random.uniform(0, 1) # agent's instinctive enjoyment of the performance (greater than 0.5 means they enjoy it)
        self.standing = self.enjoyment > 0.5 # agent's initial behavior (standing or sitting) determined by enjoyment
        self.neighbors = [] # initialize neighbor list as a stored agent feature (since agents don't move, neighbors don't change)

    def get_neighbors(self):
        # determine agent neighbors based on structure
        x, y = self.pos
        grid = self.model.grid
        if self.structure == "five":
            # five-neighbor structure is the agents to the E, W, NE, NW, and N of the agent
            coords = [(x, y + 1), 
                         (x + 1, y + 1), 
                         (x + 1, y), 
                         (x - 1, y), 
                         (x - 1, y + 1)]
        else:
            # cone structure includes five neighbors plus the 5 agents two rows ahead and the 7 agents three rows ahead
            coords = [(x, y + 1), 
                      (x + 1, y + 1), 
                      (x + 1, y), 
                      (x - 1, y), 
                      (x - 1, y + 1),
                      (x, y + 2),
                      (x + 1, y + 2),
                      (x + 2, y + 2),
                      (x - 1, y + 2),
                      (x - 2, y + 2),
                      (x, y + 3),
                      (x+1, y+3),
                      (x+2, y+3),
                      (x+3, y+3),
                      (x-1, y+3),
                      (x-2, y+3),
                      (x-3, y+3)]
        
        # filter valid positions and retrieve agents
        for coord in coords:
            if not grid.out_of_bounds(coord):
                agents_in_cell = grid.get_cell_list_contents([coord])
                self.neighbors.extend(agents_in_cell) # add neighbors to agent's neighbor list
    
    def evaluate(self):
        # evaluate whether the agent should stand based on neighbors' standing behavior
        standing_neighbors = sum(neighbor.standing for neighbor in self.neighbors)
        return standing_neighbors > len(self.neighbors) / 2
    
    def determine_new_state(self):
        # determine the new state based on the evaluation
        self.new_state = self.evaluate()

    def update_state(self):
        # update the agent's standing state based on the new state
        self.standing = self.new_state

    def step(self):
        # determine the new state and update standing
        new_state = self.evaluate()
        self.standing = new_state

    def dissatisfaction(self):
        # calculate dissatisfaction based on whether the agent is standing against its enjoyment
        desired_state = self.evaluate()
        return int(self.standing != desired_state)