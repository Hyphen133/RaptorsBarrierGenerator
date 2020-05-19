from src.barrier_generator.map_coloring import MapColoring
from src.map_processing.map_loading import FilePathMapLoader
from tests.test_base import TestBase


class MapColoringTests(TestBase):
    def test_color_map(self):
        #Given
        countours_image_filepath = self.resource_loader.get_resource_by_filepath('contours_to_be_colored.png')
        map_loader = FilePathMapLoader(countours_image_filepath)
        countours_image = map_loader.load_image()
        map_coloring = MapColoring()

        #When
        map_coloring.extract_colored_map(countours_image)

        #Then