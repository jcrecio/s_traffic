import mesa
import random

class Semaphore(mesa.Agent):
    def __init__(self, unique_id, directions, model) -> None:
        super().__init__(unique_id, model)
        self.directions = directions
        self.time_each_direction = random.randint(1, 4)
        
        self.current_direction = random.randrange(len(directions))
        self.timer = self.time_each_direction

    def step(self):
        if self.timer == 0:
            self.timer = self.time_each_direction
            self.next_direction()
        else:
            self.timer -= 1

    def next_direction(self):
        self.current_direction = (self.current_direction + 1) % len(self.directions)
    
    # Vehicles talks to semaphores that are close (discovered previously with townhall agent) to see if it is green/open on that direction
    def is_open_direction(self, direction):
        return self.current_direction == direction