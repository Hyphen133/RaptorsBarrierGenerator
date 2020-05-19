import numpy as np

class MapColoring:

    def extract_colored_map(self, image_with_boundaries):
        image_array = np.array(image_with_boundaries, dtype=np.uint8)
        self.colored_map = np.zeros((image_array.shape[0], image_array.shape[1]))
        self.last_position = (0,0)

        color_index = 1

        while not self.is_map_colored():
            self.find_starting_pixel()
            self.color_area(color_index, self.last_position)
            color_index+=1


    def is_map_colored(self):
        return np.min(self.colored_map) > 0

    def find_starting_pixel(self):
        x, y = self.last_position

        if y == self.colored_map.shape[1] -1 and x == self.colored_map.shape[0]:
            raise ValueError("Finished iteration unexpectedly")
        elif self.colored_map[self.last_position[0], self.last_position[1]] == 0:
            return self.last_position
        else:
            if y == self.colored_map.shape[1] -1:
                self.last_position = (x+1,0)
            else:
                self.last_position = (x,y+1)

            self.find_starting_pixel()


    def color_area(self, color, current_pixel):
        x,y = current_pixel
        self.colored_map[x,y] = color
