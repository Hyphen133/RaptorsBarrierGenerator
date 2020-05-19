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
        image = np.array(countours_image)
        slic_out = slic(image)



        for segs in (10, 50, 100, 300, 500, 1000):
            segments = felzenszwalb(image, scale=segs)
            plt.imshow(segments)
            plt.show(z)
            # random_colors = [(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)) for i in range(int(np.max(segments)+1))]
            # # segments = slic(image, n_segments=segs, sigma=4)
            # colored_segments = np.zeros((segments.shape[0], segments.shape[1],3))
            # for i in range(colored_segments.shape[0]):
            #     for j in range(colored_segments.shape[1]):
            #         colored_segments[i,j] = random_colors[segments[i,j]]
            #
            # fig = plt.figure(figsize=(12, 4))
            # ax = fig.add_axes([0, 0, 1, 1])
            # ax.imshow(mark_boundaries(image, segments))
            # # ax.imshow(colored_segments)
        # plt.show()
        # map_coloring.extract_colored_map(countours_image)

        #Then