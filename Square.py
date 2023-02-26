import mesa

class Square(mesa.Agent):
    def __init__(self, unique_id, direction, x, y, model) -> None:
        super().__init__(unique_id, model)
        self.direction = direction
        self.x = x
        self.y = y