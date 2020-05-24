from collections import deque

import numpy as np

class SmartBruteForce:
    NOT_CHECKED = 255
    PASSABLE = 128
    BLOCKED = 64
    BOUNDARY = 0

    def __init__(self,robot_config) -> None:
        super().__init__()
        self.robot_config = robot_config

    # def extract_unpassable_regions(self, boundary_map):
    #     pass

    def generate_regions(self, map_image):
        positions_to_be_checked = deque([self.robot_config.get_starting_position()])
        position_map = np.ones_like(np.array(map_image))*SmartBruteForce.NOT_CHECKED

        MAP_HEIGHT, MAP_WIDTH = map_image.shape

        while len(positions_to_be_checked) > 0:
            current_x,current_y = positions_to_be_checked.popleft()

            if map_image[current_x, current_y] == SmartBruteForce.NOT_CHECKED:
                # if map_image[current_x, current_y] == SmartBruteForce.BOUNDARY:
                #     position_map[current_x, current_y] = SmartBruteForce.BLOCKED

                if self.is_robot_position_possible(map_image, current_x,current_y):
                    position_map[current_x,current_y] = SmartBruteForce.PASSABLE

                    if current_x-1 >= 0:
                        pos = (current_x-1,current_y)
                        self.add_position(position_map, pos, positions_to_be_checked)
                    if current_x+1 < MAP_HEIGHT:
                        pos = (current_x + 1, current_y)
                        self.add_position(position_map, pos, positions_to_be_checked)
                    if current_y-1 >= 0:
                        pos = (current_x, current_y-1)
                        self.add_position(position_map, pos, positions_to_be_checked)
                    if current_y+1 < MAP_WIDTH:
                        pos = (current_x, current_y+1)
                        self.add_position(position_map, pos, positions_to_be_checked)
                else:
                    position_map[current_x,current_y] = SmartBruteForce.BLOCKED

        return position_map

    def generate_regions_after_boardening(self, map_image):
        positions_to_be_checked = deque([self.robot_config.get_starting_position()])
        position_map = np.ones_like(np.array(map_image))*SmartBruteForce.NOT_CHECKED

        MAP_HEIGHT, MAP_WIDTH = map_image.shape

        while len(positions_to_be_checked) > 0:
            current_x,current_y = positions_to_be_checked.popleft()

            if map_image[current_x, current_y] != SmartBruteForce.BOUNDARY:
                position_map[current_x,current_y] = SmartBruteForce.PASSABLE

                if current_x-1 >= 0:
                    pos = (current_x-1,current_y)
                    self.add_position(position_map, pos, positions_to_be_checked)
                if current_x+1 < MAP_HEIGHT:
                    pos = (current_x + 1, current_y)
                    self.add_position(position_map, pos, positions_to_be_checked)
                if current_y-1 >= 0:
                    pos = (current_x, current_y-1)
                    self.add_position(position_map, pos, positions_to_be_checked)
                if current_y+1 < MAP_WIDTH:
                    pos = (current_x, current_y+1)
                    self.add_position(position_map, pos, positions_to_be_checked)
            else:
                position_map[current_x,current_y] = SmartBruteForce.BLOCKED

        return position_map

    def add_position(self, position_map, pos, positions_to_be_checked):
        if position_map[pos[0], pos[1]] == SmartBruteForce.NOT_CHECKED and pos not in positions_to_be_checked:
            positions_to_be_checked.append(pos)

    def is_robot_position_possible(self, map_image, current_x, current_y):
        robot_radius = self.robot_config.get_diameter() // 2
        MAP_HEIGHT,MAP_WIDTH = map_image.shape

        slice_x1 = max(current_x-robot_radius,0)
        slice_y1 = min(current_x+robot_radius,MAP_HEIGHT-1)+1
        slice_x2 = max(current_y-robot_radius,0)
        slice_y2 = min(current_y+robot_radius,MAP_WIDTH-1)+1
        sliced_map = map_image[slice_x1:slice_y1 ,slice_x2:slice_y2]

        found_boundary = self.found_boundary_in_circle(robot_radius, sliced_map)

        return np.min(sliced_map.shape)>0 and found_boundary
        # return np.min(sliced_map.shape)>0 and np.min(sliced_map) >= SmartBruteForce.PASSABLE

    def found_boundary_in_circle(self, robot_radius, sliced_map):
        circle_array = self.create_circle_array(robot_radius, robot_radius, 2 * robot_radius + 1, robot_radius)
        found_boundary = np.min(sliced_map * (255 * (1 - circle_array) + 1) > SmartBruteForce.BOUNDARY)
        return found_boundary

    def create_circle_array(self, center_x, center_y, square_side, radius, value=1):
        y, x = np.ogrid[-center_x:square_side - center_x, -center_y:square_side - center_y]
        mask = x * x + y * y <= radius * radius
        array = np.zeros((square_side, square_side))
        array[mask] = value
        return array

