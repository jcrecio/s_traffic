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

    def move_agent(self, position, agent):
        self.model.move_agent(position, agent)
    
    def get_time_allowed_stopped(self):
        return self.model.get_time_allowed_stopped()

    def communicate_long_stop(self, position):
        return self.model.communicate_long_stop(position)