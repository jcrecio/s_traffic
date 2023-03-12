import mesa
from Down import Down
from Left import Left
#import matplotlib.pyplot as plt

from Obstacle import Obstacle
from Right import Right
from Semaphore import Semaphore

from TrafficModel import TrafficModel
from Up import Up
from Vehicle import Vehicle


def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if (type(agent) is Vehicle):
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal
        
    if (type(agent) is Semaphore):
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.7
        return portrayal
    
    if (type(agent) is Obstacle):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["r"] = 1
        return portrayal

    if (type(agent) is Up):
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal

    if (type(agent) is Down):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal
    if (type(agent) is Right):
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal
    if (type(agent) is Left):
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 30, 30, 800, 800)
server = mesa.visualization.ModularServer(
    TrafficModel, [grid], "Traffic model", {"rows": 30, "columns": 30, "duration": 100, "ratio_obstacles": 0.3, "ratio_vehicles": 0.35, "wait_before_remove": 10, "seed": 30}
)
server.port = 8521  # The default
server.launch()