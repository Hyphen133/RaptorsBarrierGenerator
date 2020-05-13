
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import numpy as np

class MapProcessing():
    def extract_contours(self, map_image):
        # Remove grey
        arr = np.array(map_image)
        arr[arr < 200] = 0
        arr[arr >= 200] = 255
        image = Image.fromarray(arr)

        # Add thickness
        image = image.filter(ImageFilter.BoxBlur(2))
        arr = np.array(image)
        arr[arr < 250] = 0
        arr[arr >= 250] = 255
        image = Image.fromarray(arr)

        return image

    def show_image(image):
        plt.imshow(image)
        plt.show()