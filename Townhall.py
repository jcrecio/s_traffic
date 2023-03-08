import mesa

class Townhall(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.model = model

    def get_square(self, x, y):
        return self.model.get_square(x, y)
    
    def get_agent_on_square(self, x, y):
        return self.model.get_agent(x, y)
    
    def place_agent(self, position, agent):
        self.model.place_agent(position, agent)
