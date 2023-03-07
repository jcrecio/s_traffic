import mesa

# This class is just to draw obstacles in the board
class Obstacle(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)

        