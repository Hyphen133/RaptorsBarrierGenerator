from PIL import Image

from src.map_processing.database_config import DatabaseConfig


class MapLoader():
    def __init__(self,database_config) -> None:
        super().__init__()
        self.database_config = database_config

    def load_image(self):
        pass


class FilePathMapLoader():
    def __init__(self, filepath) -> None:
        super().__init__()
        self.filepath = filepath

    def load_image(self):
        return Image.open(self.filepath)