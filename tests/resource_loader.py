import os

from PIL.PpmImagePlugin import PpmImageFile


class ResourceLoader:
    @staticmethod
    def get_test_map_filepath(filename):
        return os.path.join(os.getcwd(), '..', 'test_resources' , 'maps', filename)
