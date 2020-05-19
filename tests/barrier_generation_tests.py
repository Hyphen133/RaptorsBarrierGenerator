from PIL import Image

from src.barrier_generator.barrier_generator import BarrierGenerator
from src.barrier_generator.boundary_extractor import BoundaryExtractor
from src.barrier_generator.robot_config import RobotConfig
from tests.test_base import TestBase

import numpy as np
import matplotlib.pyplot as plt

class BarrierGenerationTests(TestBase):
    def test_generate_additional_lines(self):
        # given
        img = np.array(Image.open("../test_resources/poly2.png").convert('L'))
        line_threshold = 50
        boundary_extractor = BoundaryExtractor()
        robot_config = RobotConfig(line_threshold)
        barrier_generator = BarrierGenerator(robot_config)

        # when
        image = barrier_generator.generate_barrier_boundaries(boundary_extractor.extract_boundary_geometries(img),img)

        # then
        plt.imshow(image)
        plt.show()
        # self.assertEqual(img.shape[:2], np.array(image).shape[:2])