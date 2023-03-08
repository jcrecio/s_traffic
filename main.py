import mesa
from Obstacle import Obstacle
from Semaphore import Semaphore

from TrafficModel import TrafficModel
from Vehicle import Vehicle


def agent_portrayal(agent):
    portrayal = {
        "Shape": "arrowHead",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if (type(agent) is Vehicle):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        return portrayal
        
    if (type(agent) is Semaphore):
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        return portrayal
    
    if (type(agent) is Obstacle):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        return portrayal

    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 15, 15, 800, 800)
server = mesa.visualization.ModularServer(
    TrafficModel, [grid], "Traffic model", {"rows": 100, "columns": 100, "duration": 100, "ratio_obstacles": 0.07, "ratio_vehicles": 0.21, "wait_before_remove": 10, "seed": 3}
)
server.port = 8521  # The default
server.launch()