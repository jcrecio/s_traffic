import mesa

class Semaphore(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)