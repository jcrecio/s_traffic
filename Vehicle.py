import random
import mesa
from Directions import DOWN, LEFT, OBSTACLE, RIGHT, UP

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position

    def step(self):
        vehicle_direction = self.townhall.get_square(self.position[0], self.position[1])
        match vehicle_direction:
            case int(UP):
                stochastic_directions = []
                if self.townhall.get_square(self.position[0] - 1, self.position[1]) == LEFT:
                    stochastic_directions.append(LEFT)
                if self.townhall.get_square(self.position[0] + 1, self.position[1]) == RIGHT:
                    stochastic_directions.append(RIGHT)
                if (len(stochastic_directions) == 0):
                    direction = UP
                else:
                    if (random.random() < 0.2): 
                        direction = random.choice(stochastic_directions)
                    else: 
                        direction = UP
            case int(RIGHT):
                stochastic_directions = []
                if self.townhall.get_square(self.position[0], self.position[1] - 1) == UP:
                    stochastic_directions.append(UP)
                if self.townhall.get_square(self.position[0] + 1, self.position[1] + 1) == DOWN:
                    stochastic_directions.append(DOWN)
                if (len(stochastic_directions) == 0):
                    direction = RIGHT
                else:
                    if (random.random() < 0.2): 
                        direction = random.choice(stochastic_directions)
                    else: 
                        direction = RIGHT
            case int(DOWN):
                stochastic_directions = []
                if self.townhall.get_square(self.position[0] + 1, self.position[1]) == RIGHT:
                    stochastic_directions.append(RIGHT)
                if self.townhall.get_square(self.position[0] - 1, self.position[1]) == LEFT:
                    stochastic_directions.append(LEFT)
                if (len(stochastic_directions) == 0):
                    direction = DOWN
                else:
                    if (random.random() < 0.2): 
                        direction = random.choice(stochastic_directions)
                    else: 
                        direction = DOWN
            case int(LEFT):
                stochastic_directions = []
                if self.townhall.get_square(self.position[0], self.position[1] - 1) == UP:
                    stochastic_directions.append(UP)
                if self.townhall.get_square(self.position[0], self.position[1] + 1) == DOWN:
                    stochastic_directions.append(DOWN)
                if (len(stochastic_directions) == 0):
                    direction = LEFT
                else:
                    if (random.random() < 0.2): 
                        direction = random.choice(stochastic_directions)
                    else: 
                        direction = LEFT