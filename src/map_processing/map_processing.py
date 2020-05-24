
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFilter


class MapProcessing():
    def extract_contours(self, map_image):
        arr = np.array(map_image)
        image = Image.fromarray(arr)
        image = image.filter(ImageFilter.CONTOUR)
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        #TODO -> verify box blur value
        image = image.filter(ImageFilter.BoxBlur(0.3))
        arr = np.array(image)

        #Remove any blur to black values
        arr[arr < 250] = 0
        arr[arr >= 250] = 255

        #Countour side effect
        arr2 = np.ones_like(arr)*255
        arr2[2:-2,2:-2] = arr[2:-2,2:-2]
        image = Image.fromarray(arr2)

        return image

    def show_image(self,image, cmap='gray'):
        plt.imshow(image, cmap=cmap)
        plt.show()