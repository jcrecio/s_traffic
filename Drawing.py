from Agents.SemaphoreAgent import SemaphoreAgent
from Agents.VehicleAgent import VehicleAgent
from Directions import Back, EntryPoint, Front, Left, Right, Obstacle

def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Color": "red",
        "Filled": "true",
        "Layer": 0,
        "r": 0.5,
    }

    if (type(agent) is VehicleAgent):
        portrayal["Color"] = agent.get_color()
        portrayal["Layer"] = 0
        portrayal["r"] = 0.3
        return portrayal
    elif (type(agent) is SemaphoreAgent):
        portrayal = {
                "Shape": "arrowHead",
                "scale": 0.55,
                "Color": "green",
                "Filled": "false",
                "Layer": 0,
                "arrowhead_shape": {"width": 15, "height": 10}
        }
        if (agent.current_direction == 0): 
            portrayal["heading_x"] = -1
            portrayal["heading_y"] = 0
        elif (agent.current_direction == 2): 
            portrayal["heading_x"] = 1
            portrayal["heading_y"] = 0
        elif (agent.current_direction == 1): 
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = 1
        elif (agent.current_direction == 3): 
            portrayal["heading_x"] = 0
            portrayal["heading_y"] = -1
        return portrayal
    elif (type(agent) is Obstacle):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "black"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        return portrayal
    elif (type(agent) is EntryPoint):
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        portrayal["w"] = 0.9
        portrayal["h"] = 0.9
        return portrayal
    
    portrayal = {
            "Shape": "arrowHead",
            "scale": 0.5,
            "Color": "purple",
            "Filled": "false",
            "Layer": 0,
        }
    if (type(agent) is Front): 
        portrayal["heading_x"] = -1
        portrayal["heading_y"] = 0
    elif (type(agent) is Back): 
        portrayal["heading_x"] = 1
        portrayal["heading_y"] = 0
    elif (type(agent) is Right): 
        portrayal["heading_x"] = 0
        portrayal["heading_y"] = 1
    elif (type(agent) is Left): 
        portrayal["heading_x"] = 0
        portrayal["heading_y"] = -1
    return portrayal