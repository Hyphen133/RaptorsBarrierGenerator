import os

from PIL.PpmImagePlugin import PpmImageFile


class ResourceLoader:
    def get_test_map_filepath(self,filename):
        return os.path.join(os.getcwd(), '..', 'test_resources', 'maps', filename)
