import os
from unittest import TestCase

from PIL import Image
from PIL.ImageFile import ImageFile

from src.map_processing.database_config import DatabaseConfig
from src.map_processing.map_loading import MapLoader, FilePathMapLoader
from tests.test_base import Assertions, TestBase
from tests.resource_loader import ResourceLoader


class MapLoadingTests(TestBase):
    def test_database_integration(self):
        #given
        database_config = DatabaseConfig()
        map_loader = MapLoader(database_config)

        #when
        map = map_loader.load_image()

        #then
        self.is_PIL_Image(map)

    def test_filepath_map_loader(self):
        # given
        filepath = ResourceLoader.get_test_map_filepath('apartment.pgm')
        map_processing = FilePathMapLoader(filepath)

        # when
        map = map_processing.load_image()

        # then
        self.is_PIL_Image(map)