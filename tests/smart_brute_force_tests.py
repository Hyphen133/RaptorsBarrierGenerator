from PIL import Image
from scipy import signal

from src.barrier_generator.robot_config import RobotConfig
from src.barrier_generator.smart_brute_force.smart_brute_force import SmartBruteForce
from tests.test_base import TestBase
import numpy as np
import matplotlib.pyplot as plt

class SmartBruteForceTests(TestBase):
    def test_generate_regions(self):
        # given
        img = np.array(Image.open("../test_resources/poly2.bmp").convert('L'))
        line_threshold = 40
        # starting_position = (75,650)
        starting_position = (150, 350)
        robot_config = RobotConfig(line_threshold, starting_position)
        barrier_generator = SmartBruteForce(robot_config)

        #tmp
        thickened_boundary_image = barrier_generator.thicken_boundaries(img)

        plt.imshow(thickened_boundary_image, cmap='gray')
        plt.title("With widthen boundaries")
        plt.show()

        # when
        passable_region, impassable_regions = barrier_generator.generate_regions(thickened_boundary_image)

        plt.title("Passable region")
        passable_region.show_boundary()

        plt.title("Passable region after pologinization")
        for region in passable_region.polygonize():
            plt.plot(*region.exterior.xy)
        plt.show()

        # for i,region in enumerate(impassable_regions):
        #     plt.title("Impassable region " + str(i))
        #     region.show_boundary()
        #
        #     plt.title("After pologinization")
        #     plt.plot(*region.polygonize().exterior.xy)
        #     plt.show()




