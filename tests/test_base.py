from unittest import TestCase

from PIL.Image import Image


class TestBase(TestCase):

    def is_PIL_Image(self,image):
        self.assertTrue(isinstance(image, Image))