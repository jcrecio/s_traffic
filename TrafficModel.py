import uuid
import mesa
import random
import numpy as np
from Constants import BACK, LEFT, OBSTACLE, RIGHT, SEMAPHORE, FRONT
from Back import Back
from Left import Left
from Obstacle import Obstacle
from Right import Right
from Semaphore import Semaphore
from Townhall import Townhall
from Front import Front
from Vehicle import Vehicle

""" Model for traffic simulation """
class TrafficModel(mesa.Model):
    def __init__(self, rows, columns, duration, ratio_obstacles, ratio_vehicles, wait_before_remove, seed):
        self.rows = rows
        self.columns = columns
        self.duration = duration
        self.ratio_obstacles = ratio_obstacles
        self.ratio_vehicles = ratio_vehicles
        self.vehicles = int((rows * columns) * ratio_vehicles)
        self.wait_before_remove = wait_before_remove
        self.schedule = mesa.time.RandomActivation(self)
        random.seed(seed)
        self.total_wait_vehicles = 0
        
        self.init()

    def init(self):
        # Agent intermediary which is used by vehicles as a 'GPS' to know how to move
        self.townhall = Townhall(uuid.uuid4(), self)

        # Squares can be empty and have a direction (0,1,2,3) or can be obstacles (-1) or semaphores (-2)
        self.squares = np.zeros((self.rows, self.columns))

        # Mesa grid with the agents
        self.grid = mesa.space.MultiGrid(self.rows, self.columns, False)

        self.add_squares()
        self.add_semaphores()
        self.generate_entry_point()
        self.add_vehicles()

    # Adds a specific object into a square, like a direction as FRONT, BACK, etc or an OBSTACLE
    def add_square(self, i, j, object):
        self.schedule.add(object)
        self.grid.place_agent(object, (i, j)) 

    """ Adds all the squares in the grid, meaning it creates all the directions and obstacles in the grid 
    """
    def add_squares(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if (random.random() < self.ratio_obstacles):
                    # Add an obstacle
                    self.squares[i, j] = OBSTACLE
                    self.add_square(i, j, Obstacle(uuid.uuid4(), self))
                else:
                    # Add a direction
                    self.squares[i, j] = random.randrange(4)
                    if (self.squares[i, j] == FRONT): self.add_square(i, j, Front(uuid.uuid4(), self)) 
                    elif (self.squares[i, j] == RIGHT): self.add_square(i, j, Right(uuid.uuid4(), self))  
                    elif (self.squares[i, j] == BACK): self.add_square(i, j, Back(uuid.uuid4(), self))  
                    elif (self.squares[i, j] == LEFT): self.add_square(i, j, Left(uuid.uuid4(), self))  
    """
    Adds semaphores in all the squares of the grid that have intersections
    Besides, if any square have all directions flowing in, it modifies randomly one to avoid close loops
    """
    def add_semaphores(self):
        for i in range(1, self.rows - 2):
            for j in range(1, self.columns - 2):
                if (self.squares[i, j] == OBSTACLE): continue

                # Inward stores how many directions flow in the square
                inward = 0
                directions = list()
                if (self.squares[i, j-1] == BACK): 
                    inward += 1
                    directions.append(FRONT)
                if (self.squares[i+1, j] == LEFT): 
                    inward += 1
                    directions.append(RIGHT)
                if (self.squares[i, j+1] == FRONT): 
                    inward +=1
                    directions.append(BACK)
                if (self.squares[i-1, j] == RIGHT): 
                    inward += 1
                    directions.append(LEFT)

                if (inward == 4):
                    # all directions flow in, modify at least one to avoid closed loops in one square
                    random_direction = random.randrange(4)
                    directions = range(4)
                    match random_direction:
                        case 0: self.squares[i, j-1] = random.choice([x for x in directions if x != BACK])
                        case 1: self.squares[i+1, j] = random.choice([x for x in directions if x != LEFT])
                        case 2: self.squares[i, j+1] = random.choice([x for x in directions if x != FRONT])
                        case 3: self.squares[i-1, j] = random.choice([x for x in directions if x != RIGHT])

                # there is intersection, add semaphore
                if (inward > 1):
                    s = Semaphore(uuid.uuid4(), [i,j], directions, self)
                    self.schedule.add(s)
                    self.grid.place_agent(s, (i, j))
                    self.squares[i, j] = SEMAPHORE

    """ It decides the entry point where all the cars start the journey """
    def generate_entry_point(self):
        x = random.randrange(4)
        match x:
            case 0: self.entry_point = [0, random.randrange(self.columns - 1)]
            case 1: self.entry_point = [self.columns - 1, random.randrange(self.rows -1)]
            case 2: self.entry_point = [self.rows - 1, random.randrange(self.columns - 1)]
            case 3: self.entry_point = [random.randrange(self.rows - 1), 0]

        valid_directions_for_entry_point = []
        if (self.entry_point[0] > 0): valid_directions_for_entry_point.append(FRONT)
        if (self.entry_point[0] < self.columns - 1): valid_directions_for_entry_point.append(BACK)
        if (self.entry_point[1] > 0): valid_directions_for_entry_point.append(LEFT)
        if (self.entry_point[1] < self.rows - 1): valid_directions_for_entry_point.append(RIGHT)

        self.squares[self.entry_point[0], self.entry_point[1]] = random.choice(valid_directions_for_entry_point)
        agents_to_remove = self.grid.get_cell_list_contents([[self.entry_point[0],self.entry_point[1]]])
        for agent in agents_to_remove:
            self.grid.remove_agent(agent)
            self.schedule.remove(agent)
        position = self.entry_point[0], self.entry_point[1]
        match self.squares[self.entry_point[0], self.entry_point[1]]:
            case 0:
                up = Front(uuid.uuid4(), self)
                self.grid.place_agent(up, position)
                self.schedule.add(up)
            case 1:
                right = Right(uuid.uuid4(), self)
                self.grid.place_agent(right, position)
                self.schedule.add(right)
            case 2:
                down = Back(uuid.uuid4(), self)
                self.grid.place_agent(down, position)
                self.schedule.add(down)
            case 3:
                left = Left(uuid.uuid4(), self)
                self.grid.place_agent(left, position)
                self.schedule.add(left)

    """
    Adds a vehicle with a specific ID
    """
    def add_vehicle(self, i):
        a = Vehicle(i, self.entry_point, self.townhall)
        self.schedule.add(a)
        self.grid.place_agent(a, (self.entry_point[0], self.entry_point[1]))

    """ Adds all the vehicles specified in the constructor """
    def add_vehicles(self):
        for i in range(self.vehicles):
            self.add_vehicle(i)

    """ It goes 1 step in the simulation until it reaches the maximum duration """
    def step(self):
        if (self.schedule.steps > self.duration):
            self.running = False
            print("Tiempo medio por vehiculo que está parado en semáforo o esperando por otro veíhuclo.")
            print(self.total_wait_vehicles / self.vehicles)
        self.schedule.step()

    def get_square(self, r, c):
        if r >= 0 and r < self.rows and c >= 0 and c < self.columns:
            square = self.squares[r, c]
            if (square == SEMAPHORE):
                agents_in_square = self.grid.get_cell_list_contents([[r, c]])
                other_agent_in_square \
                    = type([agent for agent in agents_in_square if not isinstance(agent, Semaphore)][0])
                if (other_agent_in_square is Front): return FRONT
                if (other_agent_in_square is Right): return RIGHT
                if (other_agent_in_square is Back): return BACK
                if (other_agent_in_square is Left): return LEFT
                return OBSTACLE
            return square
        
        # Out of bounds square requested
        return None

    def get_agent(self, r, c):
        if r >= 0 and r < self.rows and c >= 0 and c < self.columns:
            return self.grid.get_cell_list_contents([[r,c]])
        
        # Out of bounds square requested
        return None
    
    def place_agent(self, position, agent):
        self.grid.place_agent(agent, (position[0], position[1]))

    def move_agent(self, position, agent):
        self.grid.move_agent(agent, (position[0], position[1]))
    
    def get_time_allowed_stopped(self):
        return self.wait_before_remove

    """ When a vehicle is stopped for long time, it is considered parked so it returs to entry point """
    def communicate_long_stop(self, position):
        agents = self.get_agent(position[0], position[1])
        agent_to_remove = [agent for agent in agents if type(agent) is Vehicle][0]
        self.total_wait_vehicles += agent_to_remove.get_all_time_stopped()
        self.schedule.remove(agent_to_remove)
        self.grid.remove_agent(agent_to_remove)

        self.add_vehicle(uuid.uuid4())