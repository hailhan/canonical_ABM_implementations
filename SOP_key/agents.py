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
        # create a function to facilitate neighbor lookup based on the chosen structure
        x, y = self.pos
        grid = self.model.grid

        # define offsets for each structure
        offsets_five = [
            (0, 1),    # N
            (1, 1),    # NE
            (1, 0),    # E
            (-1, 0),   # W
           (-1, 1),   # NW
        ]
        offsets_cones = offsets_five + [
            (0, 2), (1, 2), (2, 2), (-1, 2), (-2, 2),   # two rows ahead
            (0, 3), (1, 3), (2, 3), (3, 3), (-1, 3), (-2, 3), (-3, 3)  # three rows ahead
        ]

        # select offsets based on structure
        offsets = offsets_five if self.structure == "five" else offsets_cones

        self.neighbors = []  # reset neighbor list
        for dx, dy in offsets:
            coord = (x + dx, y + dy)
            if not grid.out_of_bounds(coord):
                agents_in_cell = grid.get_cell_list_contents([coord])
                self.neighbors.extend(agents_in_cell)
    
    # these look redundant, but are necessary for different update orders (see implementation in model.py)
    def evaluate(self):
        # evaluate whether the agent should stand based on neighbors' standing behavior
        standing_neighbors = sum(neighbor.standing for neighbor in self.neighbors)
        return standing_neighbors > len(self.neighbors) / 2
    
    def determine_new_state(self): # for asynchronous updates
        # determine the new state based on the evaluation
        self.new_state = self.evaluate()

    def update_state(self): # for asynchronous updates
        # update the agent's standing state based on the new state
        self.standing = self.new_state

    def step(self): # for synchronous updates
        # determine the new state and update standing simultaneously
        new_state = self.evaluate()
        self.standing = new_state

    def dissatisfaction(self): # for incentive-based updates
        # calculate dissatisfaction based on whether the agent is standing against its enjoyment
        desired_state = self.evaluate()
        return int(self.standing != desired_state)