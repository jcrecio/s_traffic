import random
import mesa
from Constants import DOWN, LEFT, OBSTACLE, PROBABILITY_STOCHASTIC_MOVEMENT, RIGHT, SEMAPHORE, UP
from Obstacle import Obstacle
from Semaphore import Semaphore

""" This is used to obtain the orthogonal directions for a given direction.
    Examples: UP    -> [LEFT, RIGHT]
              RIGHT -> [UP, DOWN]
"""
orthogonal_directions = {
    0: [[0,-1, LEFT],[0,1, RIGHT]],
    1: [[-1,0, UP],[1,0, DOWN]],
    2: [[0,1, RIGHT],[0,-1, LEFT]],
    3: [[-1,0, UP],[1,0, DOWN]]
}

""" It returns the coordinates of a given direction. 
    Example: UP   -> -1,0
             LEFT -> 0,-1
"""
map_direction_coordinates = {
    0: [-1,0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position
        self.has_moved = False
        self.townhall = townhall
        self.being_stopped = 0
        self.all_time_stopped = 0

    """ It returns the orthogonal directions for a given one. """
    def get_orthogonal_directions(self, direction, position):
        possible_orthogonal_directions = []

        orthogonal_directions = orthogonal_directions[direction]
        for s in orthogonal_directions:
            possible_orthogonal_directions.append([position[0] + s[0], position[1] + s[1], s[2]])
            
        return possible_orthogonal_directions
          
    def move(self, position):
        self.has_moved = True
        self.position = position
        self.townhall.move_agent(position, self)

    """ It gets the available directions for the vehicle in the current position """
    def get_available_directions(self):
        # Direction indicated by the current square
        current_direction = self.townhall.get_square(self.position[0], self.position[1])
        
        # if (direction_front != OBSTACLE):
        possible_lateral_directions = self.get_orthogonal_directions(current_direction, self.position)
        # else:
        #     possible_lateral_directions = []
        
        coordinates_current_direction = map_direction_coordinates[current_direction]
        available_directions = []
        content_front = self.townhall.get_square(coordinates_current_direction[0], coordinates_current_direction[1])
        if content_front != OBSTACLE \
                and content_front != None:
            available_directions.append([coordinates_current_direction[0] + self.position[0],
                                 coordinates_current_direction[1] + self.position[1]])
        for dir in possible_lateral_directions:
            if self.townhall.get_square(dir[0], dir[1]) != OBSTACLE \
                and self.townhall.get_square(dir[0], dir[1]) != None:
                available_directions.append([dir[0], dir[1]])
        return available_directions

    """ It tries to move in a specific direction as long as the possible semaphores allows it, and there is no 
        vehicles or obstacles in the way.
    """
    def try_move(self, direction_to_move):
       agents_next_square = self.townhall.get_agent_on_square(direction_to_move[0], direction_to_move[1])
       if agents_next_square == None: return
       if (len(agents_next_square) == 0): 
           self.move(direction_to_move)
           return
       
       content_next_square = self.townhall.get_square(direction_to_move[0], direction_to_move[1])
       semaphore_in_square = [agent for agent in agents_next_square if type(agent) is Semaphore]
       if (len(semaphore_in_square) > 0 or content_next_square == SEMAPHORE):
           is_open_direction = semaphore_in_square[0].is_open_direction(self.position)
           if  is_open_direction:
                self.move(direction_to_move)
           else: self.all_time_stopped += 1
       else: 
           vehicle_in_square = [agent for agent in agents_next_square if type(agent) is Vehicle]
           if (len(vehicle_in_square) > 0 or direction_to_move == OBSTACLE): 
               self.all_time_stopped += 1
           else:
               obstacles_in_square = [agent for agent in agents_next_square if type(agent) is Obstacle]
               if (len(obstacles_in_square) > 0):
                   self.all_time_stopped += 1
               else: self.move(direction_to_move)


    def step(self):
       possible_directions_to_move = self.get_available_directions()
       if ((possible_directions_to_move == None or len(possible_directions_to_move) == 0) and self.has_moved): 
           self.being_stopped += 1
           if (self.being_stopped > self.townhall.get_time_allowed_stopped()):
               self.townhall.communicate_long_stop(self.position)
           return
    
       direction_chosen = self.random.randrange(len(possible_directions_to_move))
       self.try_move(possible_directions_to_move[direction_chosen])


    def get_all_time_stopped(self):
        return self.all_time_stopped