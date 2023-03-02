import mesa

class Semaphore(mesa.Agent):
    def __init__(self, unique_id, directions, model) -> None:
        super().__init__(unique_id, model)
        self.directions = directions