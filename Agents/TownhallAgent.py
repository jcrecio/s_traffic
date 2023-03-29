import mesa

class TownhallAgent(mesa.Agent):
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

    def park_vehicle(self, position):
        return self.model.park_vehicle(position)

    def get_direction_open_for_semaphore(self, position):
        return self.model.get_direction_open_for_semaphore(position)