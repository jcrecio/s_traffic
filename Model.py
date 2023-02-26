import mesa
import random
from Obstacle import Obstable
from Square import Square

from Vehicle import Vehicle

class TrafficModel(mesa.Model):
    def __init__(self, rows, columns, duration, ratio_obstacles, ratio_vehicles, wait_before_remove, seed):
        self.rows = rows
        self.columns = columns
        self.duration = duration
        self.obstables = (rows * columns) * ratio_obstacles
        self.vehicles = (rows * columns) * ratio_vehicles
        self.wait_before_remove = wait_before_remove
        self.schedule = mesa.time.RandomActivation(self)
        self.seed = random(seed)

        self.grid = mesa.space.MultiGrid(rows, columns, False)

        self.generate_directions()
        self.generate_obstacles()
        self.generate_entry_point()

        for i in range(self.vehicles):
            a = Vehicle(i, self)
            self.schedule.add(a)

    def generate_directions(self):
        for i in range(self.rows):
            for j in range(self.columns):
                s = Square(self.seed.random(3))
                self.grid.place_agent(s, i, j)

    def generate_obstacles(self):
        for i in range(self.obstables):
            o = Obstable()
            self.grid.place_agent(o, (self.seed.random(), self.seed.random()))

    def generate_entry_point(self):
        x = self.random(3)
        match x:
            case 0: self.entry_point = Square(2, 0, self.seed.random(self.columns - 1), self.model)
            case 1: self.entry_point = Square(2, self.columns - 1, self.seed.random(self.rows - -1), self.model)
            case 2: self.entry_point = Square(2, self.rows - 1, self.seed.random(self.columns - 1), self.model)
            case 3: self.entry_point = Square(2, self.seed.random(self.rows - 1), 0, self.model)

    def step(self):
        self.schedule.step()