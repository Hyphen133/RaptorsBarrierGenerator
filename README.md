## Requiements

pip install scipy==1.1.0

## Motivation
Many relationships are easier to be found on vectors


## Finding countours


measure.find_contours(grayscale_img, level)

Findings on usage:
* It is worth to start at 1.0
* Continue with lower values if not countours were found
* It returns 2 boundaries for each polygon "inner and outer"
* Outer boundary alone may be cause as inner and then inner corresponds to inner shapes



## Using shapely.geometry.Polygon

.simplify(level) can be used to reduce complexity of polygon

Findings
* It returns set of ndarray points for complex polygons
* At less complex polygons (high level f.ex 20) it retursn Polygon class
