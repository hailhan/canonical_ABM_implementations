from mesa import Agent
import random

class CultureAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        # give each agents a list of five "features", each of which can take a value from 0 to 9
        self.features = [random.randint(0, 9) for _ in range(5)]

    def interact(self):
        # determine agent's neighbors and choose one at random to potentially interact with
        neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
        other_agent = random.choice(neighbors)
        
        # determine which features, if any, are different between the two agents
        differences = [i for i in range(len(self.features)) if self.features[i] != other_agent.features[i]]
        if not differences:
            return  # they are identical; nothing to change
        # calculate similarity as the number of matching features divided by total features
        similarity = sum(a == b for a, b in zip(self.features, other_agent.features)) / len(self.features)
        # with probability equal to similarity, change one of the agent's features to match the other agent's
        if random.random() < similarity: 
            feature_to_change = random.choice(differences)
            self.features[feature_to_change] = other_agent.features[feature_to_change]