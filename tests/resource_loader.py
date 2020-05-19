import os

from PIL.PpmImagePlugin import PpmImageFile


class ResourceLoader:
    def get_test_map_filepath(self,filename):
        return os.path.join(os.getcwd(), '..', 'test_resources', 'maps', filename)

    def get_resource_by_filepath(self,filepath):
        return os.path.join(os.getcwd(), '..', 'test_resources', filepath)

