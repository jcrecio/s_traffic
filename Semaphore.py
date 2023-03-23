import mesa
import random

from Constants import BACK, LEFT, RIGHT, FRONT

class Semaphore(mesa.Agent):
    def __init__(self, unique_id, position, directions, model) -> None:
        super().__init__(unique_id, model)
        self.position = position
        self.directions = directions

        # Time that the semaphore is open in every direction
        self.time_each_direction = random.randint(4, 12)
        self.timer = self.time_each_direction

        self.current_direction = random.randrange(len(directions))

    def step(self):
        if self.timer == 0:
            self.timer = self.time_each_direction
            self.next_direction()
        else:
            self.timer -= 1

    def next_direction(self):
        self.current_direction = (self.current_direction + 1) % len(self.directions)
    
    """ Vehicles talks to semaphores that are adjacent (the discovery happens with townhall agent)
    to check if it is green/open on the incoming direction 
    Example: semaphore will allow a vehicle to pass if current direction of semaphore is the same where the vehicle comes
             vehicle direction: → and semaphore open in → then vehicle can move
             vehicle direction: ↓ and semaphore open in → then vehicle waits or goes somewhere else
    """
    def is_open_direction(self, position_coming_from):
        if (position_coming_from[0] < self.position[0]): 
            return self.current_direction == BACK
        if (position_coming_from[1] < self.position[1]): 
            return self.current_direction == RIGHT
        if (position_coming_from[0] > self.position[0]): 
            return self.current_direction == FRONT
        if (position_coming_from[1] > self.position[1]): 
            return self.current_direction == LEFT
    
    def get_current_direction(self):
        return self.current_direction