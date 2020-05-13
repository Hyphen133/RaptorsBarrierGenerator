from scipy.misc import imread
from shapely.geometry import Polygon
from skimage import color, measure
import matplotlib.pyplot as plt

# https://gist.github.com/urschrei/a391f6e18a551f8cbfec377903920eca?fbclid=IwAR3egjGXzB4iOBLptmBaMHXAVJhWb92j85KeuBpub09CQwV5lTREPmWdqtI#file-poly-png

# read a PNG
from show_polygon import show_polygon

img = imread("poly2.png")
coutours_level = 0.01
poly_simplification_level = 20.0

# convert to greyscale if need be
gray = color.colorconv.rgb2grey(img)
    
contours = measure.find_contours(gray, coutours_level)


for contour_cords in contours:
    poly = Polygon(contour_cords).simplify(poly_simplification_level)
    show_polygon(poly, show=False)

plt.show()

# write out to cwd as JSON
# with open("polygon.json", "w") as f:
#     f.write(geojson.dumps(poly))