from unittest import TestCase

import matplotlib.pyplot as plt
from PIL import Image
from shapely.geometry import Polygon, LineString
import numpy as np

from auto_ndarray_img_to_polygons import extract_polygon_geometries_from_img, divide_polygon_into_set_of_lines, \
    create_additional_lines_shorter_than_threshold
from min_distance_line_points import get_min_distance_pair_points, Direction, convert_line_to_formula, \
    return_points_on_lines_with_distance_closest_to_target_when_moving_both_points
from show_polygon import show_geometry, show_line


# from scipy.misc import imread


class PolygonizeTests(TestCase):
    def test_extract_geometries_from_image(self):
        # given
        img = imread("../test_resources/poly2.png")

        # when
        geometries = extract_polygon_geometries_from_img(img)

        # then
        self.assertEqual(2, len(geometries))

    def test_divide_polygon_into_lines(self):
        # given
        polygon = Polygon([[0, 0], [1, 0], [1, 1], [0, 1]])

        # when
        lines = divide_polygon_into_set_of_lines(polygon)

        # then
        self.assertEqual(4, len(lines))

    def test_min_distance_points(self):
        # given
        line1 = LineString([(0, 0), (2, 2)])
        line2 = LineString([(3, 2), (6, 6)])

        # when
        x, y, distance = get_min_distance_pair_points(line1, line2)

        # then
        self.assertEqual(1.0, distance)

    def test_add_lines(self):
        # given
        img = np.array(Image.open("../test_resources/poly2.png"))
        # img = imread("../test_resources/poly2.png")
        geometries = extract_polygon_geometries_from_img(img)
        external_boundary_geometry = geometries[0]
        internal_object_geometries = []
        if len(geometries) > 1:
            internal_object_geometries.extend(geometries[1:])

        line_threshold = 50

        # when
        new_lines = create_additional_lines_shorter_than_threshold(external_boundary_geometry,
                                                                   internal_object_geometries,
                                                                   line_threshold)

        # then
        show_geometry(external_boundary_geometry, show=False)
        for geometry in internal_object_geometries:
            show_geometry(geometry, show=False)
        for line in new_lines:
            show_line(line, show=False)
        plt.show()



    def test_line_to_formula_conversion(self):
        #given
        line1 = LineString([(0, 0), (5, 0)])

        #when
        line_formula = convert_line_to_formula(line1)

        #then
        self.assertEqual(0,line_formula(5))


    def test_moving_from_lines(self):
        #given
        line1 = LineString([(0, 0), (100, 100)])
        line2 = LineString([(0, 0), (100, 800)])

        #when
        point1, point2 =return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(line1, line2, 400,Direction.RIGHT)

        #then
        print()