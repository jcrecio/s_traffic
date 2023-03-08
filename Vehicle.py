import random
import mesa
from Constants import DOWN, LEFT, OBSTACLE, PROBABILITY_STOCHASTIC_MOVEMENT, RIGHT, SEMAPHORE, UP
from Semaphore import Semaphore

all_stochastic_directions = {
    0: [[-1,0, LEFT],[1,0, RIGHT]],
    1: [[0,-1, UP],[0,1, DOWN]],
    2: [[1,0, RIGHT],[-1,0, LEFT]],
    3: [[0,-1, UP],[0,1, DOWN]]
}

map_direction_coordinates = {
    0: [0,-1],
    1: [1, 0],
    2: [0, 1],
    3: [-1, 0]
}

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position
        self.townhall = townhall

    def get_stochastic_directions(self, direction, position):
        possible_stochastic_directions = []

        stochastic_directions = all_stochastic_directions[direction]
        for s in stochastic_directions:
            possible_stochastic_directions.append([position[0] + s[0], position[1] + s[1], s[2]])
            
        return possible_stochastic_directions

    def choose_next_square(self):
        direction = self.townhall.get_square(self.position[0], self.position[1])
        if (random.random() < PROBABILITY_STOCHASTIC_MOVEMENT): 
            possible_stochastic_directions = self.get_stochastic_directions(direction, self.position)
            stochastic_directions = []
            for dir in possible_stochastic_directions:
                if self.townhall.get_square(dir[0], dir[1]) == dir[2]:
                    stochastic_directions.append([dir[0], dir[1]])
            if (len(stochastic_directions) > 0): return random.choice(stochastic_directions)

        direction_coordinates = map_direction_coordinates[direction]
        return [self.position[0]+direction_coordinates[0], self.position[1]+direction_coordinates[1]]
                    
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
       if (len(agent_next_square) == 0): 
           self.move(direction_to_move)
           return
       if content_next_square == SEMAPHORE:
           if agent_next_square[0].is_open_direction(self.position):
                self.move(self, content_next_square)
                return
       self.move(direction_to_move)
