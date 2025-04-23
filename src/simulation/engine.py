from models.Fighter import Fighter

class Simulator:
    
    def __init__(self, Fighter2, Fighter1, round_time, rounds):
        self.f1 = Fighter1
        self.f2 = Fighter2
        self.rounds = rounds
        self.round_time = round_time
        self.current_round = 1
        self.current_time = 0