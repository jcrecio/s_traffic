import uuid
import mesa
import random
import numpy as np
from Semaphore import Semaphore

from Vehicle import Vehicle

OBSTACLE = -1
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
PROBABILITY_SLIP = 0.2

class TrafficModel(mesa.Model):
    def __init__(self, rows, columns, duration, ratio_obstacles, ratio_vehicles, wait_before_remove, seed):
        self.rows = rows
        self.columns = columns
        self.duration = duration
        self.ratio_obstacles = ratio_obstacles
        self.vehicles = (rows * columns) * ratio_vehicles
        self.wait_before_remove = wait_before_remove
        self.schedule = mesa.time.RandomActivation(self)
        self.seed = random(seed)
        
        self.init()

    def init(self):
        # Squares can be empty and have a direction (0,1,2,3) or can be obstacles (-1)
        self.squares = np.zeros(self.rows, self.columns)

        # Mesa grid with the agents
        self.grid = mesa.space.MultiGrid(self.rows, self.columns, False)

        self.add_squares()
        self.add_semaphores()
        self.generate_entry_point()
        self.add_vehicles()

    def add_squares(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if (self.seed.random() < self.ratio_obstacles):
                    # Add an obstacle
                    self.squares[i, j] = OBSTACLE
                else:
                    # Add a direction
                    self.squares[i, j] = self.seed.random(3)

    def add_semaphores(self):
        # Checks with squares have direction intersections to add semaphores
        # If any has intersections from all directions, it modifies one to make the square valid
        for i in range(1, self.rows - 2):
            for j in range(1, self.columns - 2):
                inward = 0
                directions = list()
                if (self.squares[i, j-1] == 2): 
                    inward += 1
                    directions.append(UP)
                if (self.squares[i+1, j] == 3): 
                    inward += 1
                    directions.append(RIGHT)
                if (self.squares[i, j+1] == 0): 
                    inward +=1
                    directions.append(DOWN)
                if (self.squares[i-1, j] == 1): 
                    inward += 1
                    directions.append(LEFT)

                # all directions flow in, modify one
                random_direction = self.seed.random(3)
                directions = range(3)
                match random_direction:
                    case 0: self.squares[i, j-1] = self.seed.random.choice([x for x in directions if x != DOWN])
                    case 1: self.squares[i+1, j] = self.seed.random.choice([x for x in directions if x != LEFT])
                    case 2: self.squares[i, j+1] = self.seed.random.choice([x for x in directions if x != UP])
                    case 3: self.squares[i-1, j] = self.seed.random.choice([x for x in directions if x != RIGHT])
                # there is intersection, add semaphore
                if (inward > 1):
                    s = Semaphore(uuid.uuid4(), directions)
                    self.schedule.add(s)
                    self.grid.place_agent(s, (i, j))

    def generate_entry_point(self):
        x = self.random(3)
        match x:
            case 0: self.entry_point = [0, self.seed.random(self.columns - 1)]
            case 1: self.entry_point = [self.columns - 1, self.seed.random(self.rows - -1)]
            case 2: self.entry_point = [self.rows - 1, self.seed.random(self.columns - 1)]
            case 3: self.entry_point = [self.seed.random(self.rows - 1), 0]

    def add_vehicles(self):
        for i in range(self.vehicles):
            a = Vehicle(i, self)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()