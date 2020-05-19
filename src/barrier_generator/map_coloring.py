import numpy as np
from skimage.segmentation import felzenszwalb


class MapColoring:
    def __init__(self,segs=50) -> None:
        super().__init__()
        self.segs = segs

    def extract_colored_map(self, image_with_boundaries):
        return felzenszwalb(image_with_boundaries, scale=self.segs)
