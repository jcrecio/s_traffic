""" In this model, the vehicles move like in a normal road, left, front or right, as long as those
    directions are accessible.
"""

import mesa
import random
from Constants import BACK, LEFT, OBSTACLE, RIGHT, SEMAPHORE, FRONT
from Semaphore import Semaphore

""" This is used to obtain the orthogonal directions for a given direction.
    Examples: FRONT -> orthogonals are [LEFT, RIGHT]
              RIGHT -> orthogonals are [FRONT, DOWN]
"""
orthogonal_directions = {
    0: [[0,-1, LEFT],[0,1, RIGHT]], # ↑: (←,→)
    1: [[-1,0, FRONT],[1,0, BACK]], # →: (↑,↓)
    2: [[0,1, RIGHT],[0,-1, LEFT]], # ↓: (←,→)
    3: [[-1,0, FRONT],[1,0, BACK]]  # ←: (↑,↓)
}

""" It returns the coordinates of a given direction.
    Example: FRONT -> -1,0
             LEFT  -> 0,-1
"""
map_direction_coordinates = {
    0: [-1,0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}

opposite_directions = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    FRONT: BACK,
    BACK: FRONT
}

class Vehicle(mesa.Agent):
    def __init__(self, unique_id, position, townhall) -> None:
        super().__init__(unique_id, townhall)
        self.position = position
        self.townhall = townhall

        # time waiting for other vehicles
        self.time_waiting_for_vehicles = 0

        # time waiting in semaphores
        self.time_waiting_for_semaphores = 0

        # wait_for_park is used to determine if a car cannot longer move so it is parked
        self.wait_for_park = 0

        # Random color used in representation
        self.color = self.get_random_color()

    """ It returns the orthogonal directions for a given one. """
    def get_orthogonal_directions(self, direction, position):
        possible_orthogonal_directions = []

        all_orthogonal_directions = orthogonal_directions[direction]
        for s in all_orthogonal_directions:
            possible_orthogonal_directions.append([position[0] + s[0], position[1] + s[1], s[2]])
            
        return possible_orthogonal_directions
          
    def move(self, position):
        self.position = position
        self.townhall.move_agent(position, self)

    """ It gets the available directions for the vehicle in the current position 
        They can be the leading front direction plus the lateral ones if they are active and accessible
        For instance, if a vehicle is a square that goes LEFT, posible directions are UP and DOWN as long as they are
        active and accessible, this is: LEFT square contains 'LEFT' direction and it does not have a vehicle or obstacle.
    """
    
    def get_available_directions(self):
        current_direction = self.townhall.get_square(self.position[0], self.position[1])
        possible_directions = self.get_orthogonal_directions(current_direction, self.position)
        
        coordinates_current_direction = map_direction_coordinates[current_direction]
        available_directions = []
        content_front = self.townhall.get_square(
            self.position[0] + coordinates_current_direction[0], 
            self.position[1] + coordinates_current_direction[1])
        
        if content_front != OBSTACLE and content_front != None:
            if opposite_directions[content_front] != current_direction:
                available_directions.append([coordinates_current_direction[0] + self.position[0],
                                    coordinates_current_direction[1] + self.position[1]])
            
        for dir in possible_directions:
            square_in_direction = self.townhall.get_square(dir[0], dir[1])
            if square_in_direction == dir[2] or square_in_direction == SEMAPHORE:
                available_directions.append([dir[0], dir[1]])

        return available_directions

    # """ It tries to move in a specific direction as long as the possible semaphores allows it, and there is no 
    #     vehicles or obstacles in the way.
    # """
    # def try_move(self, direction_to_move):
    #    agents_next_square = self.townhall.get_agent_on_square(direction_to_move[0], direction_to_move[1])
    #    if agents_next_square == None: return
    #    if (len(agents_next_square) == 0): 
    #        self.move(direction_to_move)
    #        return

    #    content_next_square = self.townhall.get_square(direction_to_move[0], direction_to_move[1])
    #    semaphore_in_square = [agent for agent in agents_next_square if type(agent) is Semaphore]
    #    if (len(semaphore_in_square) > 0 or content_next_square == SEMAPHORE):
    #        is_open_direction = semaphore_in_square[0].is_open_direction(self.position)
    #        if  is_open_direction:
    #             self.move(direction_to_move)
    #        else: 
    #            self.time_waiting_for_semaphores += 1
    #    else: 
    #        vehicle_in_square = [agent for agent in agents_next_square if type(agent) is Vehicle]
    #        if (len(vehicle_in_square) > 0):
    #            self.time_waiting_for_vehicles += 1
    #        else:
    #            if (self.townhall.get_square(direction_to_move[0], direction_to_move[1]) == OBSTACLE):
    #                self.all_time_stopped += 1
    #            else: self.move(direction_to_move)

    def get_accesible_directions(self, possible_directions):
        accessible_directions = list()
        for possible_direction in possible_directions:
            agents_next_square = self.townhall.get_agent_on_square(possible_direction[0], possible_direction[1])
            if agents_next_square == None or len(agents_next_square) == 0: continue
            
            content_next_square = self.townhall.get_square(possible_direction[0], possible_direction[1])
            semaphore_in_square = [agent for agent in agents_next_square if type(agent) is Semaphore]
            if (len(semaphore_in_square) > 0 or content_next_square == SEMAPHORE):
                is_open_direction = semaphore_in_square[0].is_open_direction(self.position)
                if is_open_direction:
                    accessible_directions.append(possible_direction)
                    continue
                else: continue
            else: 
                vehicle_in_square = [agent for agent in agents_next_square if type(agent) is Vehicle]
                if (len(vehicle_in_square) == 0 and \
                    self.townhall.get_square(possible_direction[0], possible_direction[1]) != OBSTACLE):
                    accessible_directions.append(possible_direction)
        return accessible_directions

    def step(self):
       possible_directions_to_move = self.get_available_directions()

       # If no possible direction to move:
       if ((possible_directions_to_move == None or len(possible_directions_to_move) == 0)): 
           self.wait_for_park += 1
           if (self.wait_for_park > self.townhall.get_time_allowed_stopped()):
               self.townhall.park_vehicle(self.position)
           return
       
       # From all posible directions, filter out the ones that are not feasible now
       accesible_directions = self.get_accesible_directions(possible_directions_to_move) 

       # Choose a random accessible direction and move there
       if (len(accesible_directions) > 0):
            direction_chosen = self.random.randrange(len(accesible_directions))
            self.move(accesible_directions[direction_chosen])
       else: # if not available accessible directions, choose any to decide what to wait for (vehicle or semaphore)
           direction_chosen = possible_directions_to_move[self.random.randrange(len(possible_directions_to_move))]
           agents_next_square = self.townhall.get_agent_on_square(direction_chosen[0], direction_chosen[1])
           content_next_square = self.townhall.get_square(direction_chosen[0], direction_chosen[1])
           semaphore_in_square = [agent for agent in agents_next_square if type(agent) is Semaphore]
           if (len(semaphore_in_square) > 0 or content_next_square == SEMAPHORE):
                self.time_waiting_for_semaphores += 1
           else: self.time_waiting_for_vehicles += 1

    def get_time_waiting_for_semaphores(self):
        return self.time_waiting_for_semaphores
    
    def get_time_waiting_for_vehicles(self):
        return self.time_waiting_for_vehicles
    
    def get_color(self):
        return self.color
    
    def get_random_color(self):
        color = "".join([random.choice("0123456789abcdef") for _ in range(6)])
        return "#" + color
