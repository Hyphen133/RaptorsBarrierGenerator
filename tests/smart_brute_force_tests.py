from PIL import Image
from scipy import signal

from src.barrier_generator.robot_config import RobotConfig
from src.barrier_generator.smart_brute_force.smart_brute_force import SmartBruteForce
from tests.test_base import TestBase
import numpy as np
import matplotlib.pyplot as plt

class SmartBruteForceTests(TestBase):
    def test_generate_additional_lines(self):
        # given
        img = np.array(Image.open("../test_resources/poly2.bmp").convert('L'))
        line_threshold = 50
        # starting_position = (75,650)
        starting_position = (150, 350)
        robot_config = RobotConfig(line_threshold, starting_position)
        barrier_generator = SmartBruteForce(robot_config)

        #tmp

        img2 = 255-img

        a, b = 25, 25
        n = 51
        r = 25

        array = barrier_generator.create_circle_array(a, b, n, r)

        # scharr = np.array([[1, 1, 1],
        #                    [1, 1, 1],
        #                    [1, 1, 1]])  # Gx + j*Gy
        img2 = signal.convolve2d(img2, array, mode='same')
        img2 = (1-np.array(img2 >0 , dtype=int))*255


        plt.imshow(img2, cmap='gray')
        plt.show()

        # when
        image = barrier_generator.generate_regions(img)


        # then
        passable_img = np.array(image == SmartBruteForce.PASSABLE, dtype=int) * 255
        plt.imshow(passable_img, cmap='gray')
        plt.show()

        plt.imshow(np.array((255-passable_img)*img2 > 0, dtype=int), cmap='gray')
        plt.show()

        # self.assertEqual(img.shape[:2], np.array(image).shape[:2])

