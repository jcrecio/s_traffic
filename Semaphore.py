import mesa
import random

from Constants import DOWN, LEFT, RIGHT, UP

class Semaphore(mesa.Agent):
    def __init__(self, unique_id, position, directions, model) -> None:
        super().__init__(unique_id, model)
        self.position = position
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
    def is_open_direction(self, position_coming_into):
        if (position_coming_into[0] < self.position[0]): 
            return self.current_direction == LEFT
        if (position_coming_into[1] < self.position[1]): 
            return self.current_direction == DOWN
        if (position_coming_into[0] > self.position[0]): 
            return self.current_direction == RIGHT
        if (position_coming_into[1] > self.position[1]): 
            return self.current_direction == UP