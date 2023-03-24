'''
Author: Juan Carlos Recio Abad
Date: Match 23rd of 2023

Traffic simulation for subject "Sistemas Multiagente" of Universitary course
"Master en ingeniería del software e inteligencia artificial"
'''

import sys
import mesa
from Drawing import agent_portrayal
from TrafficModel import TrafficModel

rows = int(sys.argv[1])
columns = int(sys.argv[2])
duration = int(sys.argv[3])
ratio_obstacles = float(sys.argv[4])
ratio_vehicles = float(sys.argv[5])
wait_before_remove = int(sys.argv[6])
seed = int(sys.argv[7])
display = int(sys.argv[8])

if (display == 1): # with graphical display
    grids = [mesa.visualization.CanvasGrid(agent_portrayal, rows, columns, 600, 600)]
    server = mesa.visualization.ModularServer(
    TrafficModel, grids, "Traffic model", {"rows": rows, "columns": columns, "duration": duration,
                                             "ratio_obstacles": ratio_obstacles, "ratio_vehicles": ratio_vehicles, 
                                             "wait_before_remove": wait_before_remove, "seed": seed}
    )
    server.port = 8521
    server.launch()
else: # without graphical display
    traffic_model = TrafficModel(rows, columns, duration, ratio_obstacles, ratio_vehicles, wait_before_remove, seed)
    for i in range(duration):
        if (i % 75 == 0): print('Running step ' + str(i))
        traffic_model.step()
    
    traffic_model.show_summary()
