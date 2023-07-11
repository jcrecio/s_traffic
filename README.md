## 1. Running the model
To set up the environment:
1. Create a virtual environment with venv.
2. Install the dependencies in the environment using `pip install -r requirements.txt`.

To run the system, simply execute the following command:
> main.py [input parameters]

The parameters are:
```- rows = number of rows in the grid
- columns = number of columns in the grid
- duration = duration in seconds (simulation time)
- ratio_obstacles = float, ratio of obstacles with respect to the total number of cells, e.g., 0.15
- ratio_vehicles = float, ratio of vehicles with respect to the total number of cells, e.g., 0.2
- wait_before_remove = seconds it takes to remove a vehicle that cannot move anymore
- seed = seed for simulation reproduction, e.g., 1111
- display = 1 to show graphics, 0 to not show
```

`main.py 20 20 3600 0.15 0.2 10 1113 0`

(20 rows, 20 columns, duration of 3600s, 15% obstacles, 20% vehicles, 10s before parking, seed of 1113, and no graphical display)
Alternatively, you can use the attached launch.json file to run and debug the code with VSCode.

Simulation Explanation:

## 2. Initialization
- Directions are generated in the cells as follows: an initial direction is generated, and with a 70% probability, it remains stable until the remaining 30% generates an orthogonal change in direction.
- At the same time, obstacles (non-passable cells) are generated with the rate indicated in the parameters.
- Then, the directions of the cells are adjusted to avoid obvious loops and ensure that the cells on the edges do not point outward.
- Traffic lights are added at intersections.
- An entry point for vehicles is generated.
- All available vehicles are specified with the rate indicated in the parameters.

## 3. Behaviour
Townhall Agent:

- It is an agent that allows vehicles to know the environment, discover what is in the cells they move through, and determine if there are other vehicles or traffic lights. It functions as a kind of GPS/omniscient agent to guide the vehicles.
  
It is a way to decouple the vehicles directly from the model.

Vehicle Agents:

- They move 1 cell per time/second. They follow the direction specified by the cells.
- In detail, they will move to the cell dictated by the current cell or to the lateral/orthogonal cells if movement in that direction is defined (as in a regular road with left and right turns).
- If they are blocked without space for X seconds, it is considered that they are parking, and a new vehicle is introduced into the system.
- If they are blocked but there is free space they can take, they commit an "infraction" and go another way. 
  This allows the strict rules of the simulation to avoid easily blocking the system.

Traffic Light Agents:

- They are located at intersections and change the direction in which traffic is allowed every X seconds.
Each traffic light operates at its own pace (one may change to green in its current direction every 5 seconds, while another may do so every 8 seconds). They only allow the directions that generated the intersection to turn green.

## 4. Results
When the simulation ends, it will display the time consumed by each vehicle waiting for other vehicles and waiting for traffic lights.
It will also show the average and total accumulated time.
Additionally, it will show the positions in the system where vehicles parked because they could not move further.

## 5. Graphical Representation
- Agents are represented as colored dots.
- Traffic lights are represented as green arrows pointing in the direction of allowed access.
- Townhall has no representation.
- Artificial representation agents: (I used agents because using JavaScript was quite complicated just for that, and I wanted to dedicate time to the actual project instead of JavaScript and drawing graphics.)
	- Normal cells show an arrow indicating the traffic direction.
	- Obstacles or non-passable cells are represented as black squares.
	- Entry point is red.

## 6. Next steps
- Communication between vehicles to optimize routes.