import mesa
from Down import Down
from Left import Left

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
    elif (type(agent) is Semaphore):
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.9
        return portrayal
    elif (type(agent) is Obstacle):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        return portrayal
    
    portrayal = {
            "Shape": "arrowHead",
            "scale": 0.5,
            "Color": "purple",
            "Filled": "false",
            "Layer": 0,
        }
    if (type(agent) is Up): 
        portrayal["heading_x"] = -1
        portrayal["heading_y"] = 0
    elif (type(agent) is Down): 
        portrayal["heading_x"] = 1
        portrayal["heading_y"] = 0
    elif (type(agent) is Right): 
        portrayal["heading_x"] = 0
        portrayal["heading_y"] = 1
    elif (type(agent) is Left): 
        portrayal["heading_x"] = 0
        portrayal["heading_y"] = -1
    return portrayal

rows = 30
columns = 15
grid = mesa.visualization.CanvasGrid(agent_portrayal, rows, columns, 600, 600)
server = mesa.visualization.ModularServer(
    TrafficModel, [grid], "Traffic model", {"rows": rows, "columns": columns, "duration": 3600, "ratio_obstacles": 0.2, "ratio_vehicles": 0.1, "wait_before_remove": 10, "seed": 30}
)
server.port = 8521  # The default
server.launch()