import random
import mesa
from Constants import DOWN, LEFT, OBSTACLE, PROBABILITY_SLIP, RIGHT, SEMAPHORE, UP
from Semaphore import Semaphore

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position
        self.townhall = townhall

    def choose_next_square(self):
        match self.townhall.get_square(self.position[0], self.position[1]):
            case 0: #UP
                stochastic_directions = []
                if self.townhall.get_square(self.position[0] - 1, self.position[1]) == LEFT:
                    stochastic_directions.append([self.position[0] - 1, self.position[1]])
                if self.townhall.get_square(self.position[0] + 1, self.position[1]) == RIGHT:
                    stochastic_directions.append([self.position[0] + 1, self.position[1]])
                if (len(stochastic_directions) == 0):
                    return [self.position[0], self.position[1] - 1]
                else:
                    if (random.random() < PROBABILITY_SLIP): 
                        return random.choice(stochastic_directions)
                    else: 
                        return [self.position[0], self.position[1] - 1]
            case 1: #RIGHT
                stochastic_directions = []
                if self.townhall.get_square(self.position[0], self.position[1] - 1) == UP:
                    stochastic_directions.append([self.position[0], self.position[1] - 1])
                if self.townhall.get_square(self.position[0] + 1, self.position[1] + 1) == DOWN:
                    stochastic_directions.append([self.position[0] + 1, self.position[1] + 1])
                if (len(stochastic_directions) == 0):
                     return [self.position[0] + 1, self.position[1]]
                else:
                    if (random.random() < PROBABILITY_SLIP): 
                        return random.choice(stochastic_directions)
                    else: 
                        return [self.position[0] + 1, self.position[1]]
            case 2: #DOWN
                stochastic_directions = []
                if self.townhall.get_square(self.position[0] + 1, self.position[1]) == RIGHT:
                    stochastic_directions.append([self.position[0] + 1, self.position[1]])
                if self.townhall.get_square(self.position[0] - 1, self.position[1]) == LEFT:
                    stochastic_directions.append([self.position[0] - 1, self.position[1]])
                if (len(stochastic_directions) == 0):
                     return [self.position[0], self.position[1] + 1]
                else:
                    if (random.random() < PROBABILITY_SLIP): 
                         return  random.choice(stochastic_directions)
                    else: 
                         return [self.position[0] + 1, self.position[1] + 1]
            case 3: #LEFT
                stochastic_directions = []
                if self.townhall.get_square(self.position[0], self.position[1] - 1) == UP:
                    stochastic_directions.append([self.position[0], self.position[1] - 1])
                if self.townhall.get_square(self.position[0], self.position[1] + 1) == DOWN:
                    stochastic_directions.append([self.position[0], self.position[1] + 1])
                if (len(stochastic_directions) == 0):
                     return [self.position[0] - 1, self.position[1]]
                else:
                    if (random.random() < PROBABILITY_SLIP): 
                         return random.choice(stochastic_directions)
                    else: 
                         return [self.position[0] - 1, self.position[1]]
                    
    def move(self, position):
        self.position = position
        self.townhall.move_agent(position, self)

    def step(self):
       direction_to_move = self.choose_next_square()
       if (direction_to_move == None): return
       content_next_square = self.townhall.get_square(direction_to_move[0], direction_to_move[1])
       if content_next_square == OBSTACLE: 
           #stochastic move?
           return

       agent_next_square = self.townhall.get_agent_on_square(direction_to_move[0], direction_to_move[1])
       if agent_next_square == None: return
       if (len(agent_next_square)): 
           self.move(direction_to_move)
           return
       if content_next_square == SEMAPHORE:
           if agent_next_square[0].is_open_direction(self.position):
                self.move(self, content_next_square)
                return
       self.move(direction_to_move)
