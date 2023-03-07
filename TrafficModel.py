import uuid
import mesa
import random
import numpy as np
from Obstacle import Obstacle
from Semaphore import Semaphore
from Townhall import Townhall

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
        self.vehicles = int((rows * columns) * ratio_vehicles)
        self.wait_before_remove = wait_before_remove
        self.schedule = mesa.time.RandomActivation(self)
        random.seed(seed)
        
        self.init()

    def init(self):
        # Agent intermediary which is used by vehicles as a 'GPS' to know how to move
        self.townhall = Townhall(uuid.uuid4(), self)

        # Squares can be empty and have a direction (0,1,2,3) or can be obstacles (-1)
        self.squares = np.zeros((self.rows, self.columns))

        # Mesa grid with the agents
        self.grid = mesa.space.MultiGrid(self.rows, self.columns, False)

        self.add_squares()
        self.add_semaphores()
        self.generate_entry_point()
        self.add_vehicles()

    def add_squares(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if (random.random() < self.ratio_obstacles):
                    # Add an obstacle
                    self.squares[i, j] = OBSTACLE
                    # Adds an artificial agent that is used only for visualization
                    self.schedule.add(Obstacle(uuid.uuid4(), self))
                else:
                    # Add a direction
                    self.squares[i, j] = random.randrange(3)

    def add_semaphores(self):
        # Checks with squares have direction intersections to add semaphores
        # If any has intersections from all directions, it modifies one to make the square valid
        for i in range(1, self.rows - 2):
            for j in range(1, self.columns - 2):
                inward = 0
                directions = list()
                if (self.squares[i, j-1] == DOWN): 
                    inward += 1
                    directions.append(UP)
                if (self.squares[i+1, j] == LEFT): 
                    inward += 1
                    directions.append(RIGHT)
                if (self.squares[i, j+1] == UP): 
                    inward +=1
                    directions.append(DOWN)
                if (self.squares[i-1, j] == RIGHT): 
                    inward += 1
                    directions.append(LEFT)

                # all directions flow in, modify one
                random_direction = random.randrange(3)
                directions = range(3)
                match random_direction:
                    case 0: self.squares[i, j-1] = random.choice([x for x in directions if x != DOWN])
                    case 1: self.squares[i+1, j] = random.choice([x for x in directions if x != LEFT])
                    case 2: self.squares[i, j+1] = random.choice([x for x in directions if x != UP])
                    case 3: self.squares[i-1, j] = random.choice([x for x in directions if x != RIGHT])
                # there is intersection, add semaphore
                if (inward > 1):
                    s = Semaphore(uuid.uuid4(), directions, self)
                    self.schedule.add(s)
                    self.grid.place_agent(s, (i, j))

    def generate_entry_point(self):
        x = random.randrange(3)
        match x:
            case 0: self.entry_point = [0, random.randrange(self.columns - 1)]
            case 1: self.entry_point = [self.columns - 1, random.randrange(self.rows - -1)]
            case 2: self.entry_point = [self.rows - 1, random.randrange(self.columns - 1)]
            case 3: self.entry_point = [random.randrange(self.rows - 1), 0]

    def add_vehicles(self):
        for i in range(self.vehicles):
            a = Vehicle(i, None, self.townhall)
            self.schedule.add(a)

    def step(self):
        self.schedule.step()

    def get_square(self, r, c):
        return self.squares[r, c]