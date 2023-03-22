import mesa
# These classes are just to draw in the graphical grid to not spend too much time playing with ugly javascript..

class Back(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
class Front(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
class Left(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
class Right(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
class Obstacle(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
class EntryPoint(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)