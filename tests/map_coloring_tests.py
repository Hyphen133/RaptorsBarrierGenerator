import random

from fast_slic import Slic

from src.barrier_generator.map_coloring import MapColoring
from src.map_processing.map_loading import FilePathMapLoader
from tests.test_base import TestBase
import numpy as np
from skimage.segmentation import slic, felzenszwalb
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt

# http://melvincabatuan.github.io/SLIC-Superpixels/
class MapColoringTests(TestBase):
    def test_color_map(self):
        #Given
        countours_image_filepath = self.resource_loader.get_resource_by_filepath('contours_to_be_colored.png')
        map_loader = FilePathMapLoader(countours_image_filepath)
        countours_image = map_loader.load_image_rgb()
        map_coloring = MapColoring()

        #When
        segmentation_map = map_coloring.extract_colored_map(countours_image)

        #Then
        plt.imshow(segmentation_map)
        plt.show()