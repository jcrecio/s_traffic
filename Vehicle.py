import mesa

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, model) -> None:
        super().__init__(unique_id, model)
        self.position = position


        