import math
## Using experimental agent type with native "cell" property that saves its current position in cellular grid
from mesa.experimental.cell_space import CellAgent

## Helper function to get distance between two cells
def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    ## Initiate agent, inherit model property from parent class
    def __init__(self, model, cell, sugar=0, metabolism=0, vision = 0):
        super().__init__(model)
        ## Set variable traits based on model parameters
        self.cell = cell
        self.sugar = sugar
        self.init_sugar = sugar  # store initial sugar for fertility
        self.metabolism = metabolism
        self.vision = vision
        self.age = 0 # age for determining fertility
        self.fertility = False # agents are not fertile by default
        self.sex = model.random.randint(0, 1) # agent sex is randomly assigned with equal probability (0=female, 1=male)
    ## Define movement action
    def move(self):
        ## Determine currently empty cells within line of sight
        possibles = [
            cell
            for cell in self.cell.get_neighborhood(self.vision, include_center=True)
            if cell.is_empty 
        ]
        ## Determine how much sugar is in each possible movement target
        sugar_values = [
            cell.sugar
            for cell in possibles
        ]
        ## Calculate the maximum possible sugar value in possible targets
        if not sugar_values:
            return
        max_sugar = max(sugar_values)
        ## Get indices of cell(s) with maximum sugar potential within range
        candidates_index = [
            i for i in range(len(sugar_values)) if math.isclose(sugar_values[i], max_sugar)
        ]
        ## Indentify cell(s) with maximum possible sugar
        candidates = [
            possibles[i]
            for i in candidates_index
        ]
        ## Find the closest cells with maximum possible sugar
        min_dist = min(get_distance(self.cell, cell) for cell in candidates)
        final_candidates = [
            cell
            for cell in candidates
            if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
        ]
        ## Choose one of the closest cells with maximum sugar (randomly if more than one)
        self.cell = self.random.choice(final_candidates)
    ## consumer sugar in current cell, depleting it, then consumer metabolism
    def gather_and_eat(self):
        self.sugar += self.cell.sugar
        self.cell.sugar = 0
        self.sugar -= self.metabolism
    ## If an agent has zero or negative suger, it dies and is removed from the model
    def see_if_die(self):
        if self.sugar <= 0:
            # added additional check to handle "ghost" agents
            if self.cell is not None:
                self.cell.remove_agent(self)
            self.model.agents.remove(self)

    ## Functions for reproduction
    def determine_fertility(self):
        # agents must be at least as old as the age of consent and have at least their initial sugar holdings to be fertile
        if self.sugar >= self.init_sugar and self.age >= self.model.age_of_consent:
            self.fertility = True
        else:
            self.fertility = False

    def reproduce(self):
        if self.fertility:
            # select a random neighbor agent at random
            neighbor_cells = self.cell.get_neighborhood(include_center=False)
            potential_partners = [
                agent for cell in neighbor_cells for agent in cell.agents
                if isinstance(agent, SugarAgent)  # optional safety check
                ]
            # fertile agents will try to reproduce with ALL neighbors
            for partner in potential_partners:
                # if the selected neighbor is fertile and the opposite sex from current agent, then reproduction happens
                if partner.fertility and partner.sex != self.sex:
                    empty_neighbors = [cell for cell in self.cell.get_neighborhood(1, include_center=False) if cell.is_empty]
                    if empty_neighbors:
                        baby_cell = self.random.choice(empty_neighbors)
                    else:
                        baby_cell = self.cell  # fallback if no room
                    # create offspring agent with average properties of both parents
                    offspring = SugarAgent(
                        model=self.model,
                        cell=baby_cell,
                        sugar=((self.sugar/2) + (partner.sugar/2)),
                        metabolism= self.model.random.choice([self.metabolism, partner.metabolism]),
                        vision=self.model.random.choice([self.vision, partner.vision]),
                    )
                    baby_cell.add_agent(offspring)
                    self.model.agents.add(offspring)
                    # after reproduction, the agents will lose the amount of sugar they gave to their offspring
                    self.sugar -=self.sugar/2
                    partner.sugar -= partner.sugar/2
            if self.sugar < self.init_sugar:
                # if the agent has less than initial sugar after each reproduction, it will not be able to reproduce with any remaining partners
                self.fertility = False