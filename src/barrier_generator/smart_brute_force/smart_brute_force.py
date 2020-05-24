from collections import deque

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

class SmartBruteForce:
    NOT_CHECKED = 255
    PASSABLE = 128
    BLOCKED = 64
    BOUNDARY = 0

    def __init__(self,robot_config) -> None:
        super().__init__()
        self.robot_config = robot_config

    def thicken_boundaries(self, img):
        line_threshold = self.robot_config.get_diameter()
        WHITE_PIXEL = 255
        out_img = WHITE_PIXEL - img
        array = self.create_circle_array(line_threshold // 2, line_threshold // 2, line_threshold + 1, line_threshold // 2)
        out_img = signal.convolve2d(out_img, array, mode='same')
        out_img = (1 - np.array(out_img > 0, dtype=int)) * WHITE_PIXEL
        return out_img

    def generate_regions(self, map_image):
        blocked_regions = []
        map = np.copy(map_image)

        passable_region_map = self.generate_region(map, self.robot_config.get_starting_position())
        map = self.merge_region_to_map(map, passable_region_map)
        passable_region = Region(passable_region_map)

        try:
            while True:
                next_region_starting_position = self.find_next_region_position(map)
                region_map = self.generate_region(map, next_region_starting_position)
                map = self.merge_region_to_map(map, region_map)
                blocked_regions.append(Region(region_map))
        except ValueError:
            return passable_region, blocked_regions

    def merge_region_to_map(self, map, region):
        return map * np.array(region != SmartBruteForce.PASSABLE, dtype=int)

    def find_next_region_position(self, map_image):
        next_region_starting_position = np.argwhere(map_image == SmartBruteForce.NOT_CHECKED)
        try:
            return next_region_starting_position[0]
        except Exception:
            raise ValueError("No more UNCHECKED regions found!!")


    def generate_region(self, map_image, region_starting_position):
        positions_to_be_checked = deque([region_starting_position])
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

    def create_circle_array(self, center_x, center_y, square_side, radius, value=1):
        y, x = np.ogrid[-center_x:square_side - center_x, -center_y:square_side - center_y]
        mask = x * x + y * y <= radius * radius
        array = np.zeros((square_side, square_side))
        array[mask] = value
        return array

class Region():
    def __init__(self, region_map) -> None:
        super().__init__()
        self.region_map = region_map

    def get_boundary(self):
        return (1-np.array(self.region_map==SmartBruteForce.BLOCKED,dtype=int)*255)

    def get_area(self):
        return (1 - np.array(self.region_map == SmartBruteForce.PASSABLE, dtype=int)*255)

    def show_area(self):
        plt.imshow(self.get_area(), cmap='gray')
        plt.show()

    def show_boundary(self):
        plt.imshow(self.get_boundary(), cmap='gray')
        plt.show()