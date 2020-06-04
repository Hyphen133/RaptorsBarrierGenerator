from collections import deque

import numpy as np
from PIL import Image
from scipy import signal
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
from skimage import measure


class SmartBruteForce:
    NOT_CHECKED = 255
    PASSABLE = 128
    BLOCKED = 64
    BOUNDARY = 0

    def __init__(self,robot_config) -> None:
        super().__init__()
        self.robot_config = robot_config

    def generate_polygon_regions(self, image, plot=False):
        before_thicken_image = np.copy(image)
        after_thicken_image = self.thicken_boundaries(image)

        if plot:
            plt.imshow(before_thicken_image, cmap='gray')
            plt.title("Before thicken boundaries")
            plt.show()


            plt.imshow(after_thicken_image, cmap='gray')
            plt.title("After thicken")
            plt.show()


        boundary_region = self.create_boundary_region(after_thicken_image,before_thicken_image)
        passable_region, impassable_regions = self.generate_regions(after_thicken_image, plot=plot)
        impassable_regions.append(boundary_region)

        return passable_region.polygonize(), [region.polygonize() for region in impassable_regions]


    def create_boundary_region(self, after_thicken_image, before_thicken_image):
        return Region(np.array(np.not_equal(after_thicken_image,before_thicken_image),dtype=int))


    def thicken_boundaries(self, image):
        img = np.array(image)
        line_threshold = self.robot_config.get_diameter()
        WHITE_PIXEL = 255
        out_img = WHITE_PIXEL - img
        array = self.create_circle_array(line_threshold // 2, line_threshold // 2, line_threshold + 1, line_threshold // 2)
        out_img = signal.convolve2d(out_img, array, mode='same')
        out_img = (1 - np.array(out_img > 0, dtype=int)) * WHITE_PIXEL
        return out_img

    def generate_regions(self, map_image, plot=False):
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

            if plot:
                plt.title("Passable region")
                passable_region.show_boundary()

                plt.title("Passable region after pologinization")
                for region in passable_region.polygonize():
                    plt.plot(*region.exterior.xy)
                plt.show()

                for i, region in enumerate(blocked_regions):
                    plt.title("Impassable region " + str(i))
                    region.show_boundary()
                    region.show_area()

                    plt.title("After pologinization")
                    for poly in region.polygonize():
                        plt.plot(poly.exterior.xy)
                    plt.show()


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

    def polygonize(self):
        return self.extract_polygons_geometries_from_img(self.get_area())

    def extract_polygons_geometries_from_img(self, img, coutours_level=0.0001, poly_simplification_level=1.0):
        #add padding booundary for areas that touch boundaries of image
        padded_area = np.pad(self.get_area(), [(1, ), (1, )], mode='constant')

        countours = measure.find_contours(padded_area, coutours_level)
        return [Polygon(c).simplify(poly_simplification_level) for c in countours]

