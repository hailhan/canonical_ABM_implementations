from mesa import Agent
import random

class CultureAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.features = [random.randint(0, 9) for _ in range(5)]

    def interact(self):
        neighbors = self.model.grid.get_neighbors(self.pos, moore=False, include_center=False)
        other_agent = random.choice(neighbors)

        differences = [i for i in range(len(self.features)) if self.features[i] != other_agent.features[i]]
        if not differences:
            return  # they are identical; nothing to change
        similarity = sum(a == b for a, b in zip(self.features, other_agent.features)) / len(self.features)
        if random.random() < similarity:
            feature_to_change = random.choice(differences)
            self.features[feature_to_change] = other_agent.features[feature_to_change]