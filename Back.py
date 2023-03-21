import mesa

class Back(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)