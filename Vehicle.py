import mesa

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position

    def step(self):
        


        