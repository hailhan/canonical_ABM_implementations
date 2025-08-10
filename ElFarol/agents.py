from mesa import Agent

class ElFarolAgent(Agent):
    def __init__(self, model, strategies, home_pos, bar_pos):
        super().__init__(model)
        self.strategies = strategies
        self.best_strategy = strategies[0]
        self.attend = False
        self.prediction = 0
        self.home_pos = home_pos
        self.bar_pos = bar_pos

    def predict(self):
        history = self.model.history
        self.prediction = self.predict_attendance(self.best_strategy, history[:self.model.memory_size])
        self.attend = self.prediction <= self.model.overcrowding_threshold

    def advance(self):
        # Move agent to their unique home or bar position
        new_pos = self.bar_pos if self.attend else self.home_pos
        self.model.grid.move_agent(self, new_pos)

        # Update attendance count
        if self.attend:
            self.model.attendance += 1

        # Step 3: Update best strategy
        self.update_strategies()
    
    def update_strategies(self):
        best_score = self.model.memory_size * 100 + 1
        best = self.best_strategy
        for strategy in self.strategies:
            score = 0
            for week in range(1, self.model.memory_size + 1):
                prediction = self.predict_attendance(strategy, self.model.history[week:week + self.model.memory_size])
                actual = self.model.history[week - 1]
                score += abs(actual - prediction)
            if score <= best_score:
                best_score = score
                best = strategy
        self.best_strategy = best

    def predict_attendance(self, strategy, subhistory):
        const = strategy[0]
        weights = strategy[1:]
        weighted_sum = sum(w * x for w, x in zip(weights, subhistory))
        return 100 * const + weighted_sum