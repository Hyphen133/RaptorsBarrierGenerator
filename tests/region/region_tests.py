from unittest import TestCase

from src.barrier_generator.smart_brute_force.smart_brute_force import Region
from src.map_processing.map_loading import FilePathMapLoader
import numpy as np

class RegionTests(TestCase):
    def test_extract_boundary_from_full_area(self):
        # Given
        region = self.load_region_from_test_file('area1.bmp')

        # When
        region.show_area()
        polygonized_region = region.polygonize()

        # Then
        self.assertTrue(len(polygonized_region), 1)

    def test_split_areas_with_single_innering(self):
        # Given
        region = self.load_region_from_test_file('area2.bmp')

        # When
        polygonized_region = region.polygonize()

        # Then
        self.assertTrue(len(polygonized_region), 2)
        self.assertFalse(polygonized_region[0].contains(polygonized_region[1]) or polygonized_region[1].contains(polygonized_region[0]))

    def load_region_from_test_file(self, filepath):
        #Makes PASSABLE from white
        region_map = np.array(FilePathMapLoader(filepath).load_image())/2 + 0.5
        region = Region(region_map)
        return region

    def test_split_areas_with_multiple_innering(self):
        # Given
        region = self.load_region_from_test_file('area4.bmp')

        # When
        polygonized_region = region.polygonize()

        # Then
        self.assertTrue(len(polygonized_region), 3)

    def test_throws_exception_from_full_area_touching_boundary(self):
        # Given
        region = self.load_region_from_test_file('area3.bmp')

        # When
        polygonized_region = region.polygonize()

        # Then
        

    def test_throws_exception_on_area_touching_bonudary(self):
        #TODO -> implement
        pass