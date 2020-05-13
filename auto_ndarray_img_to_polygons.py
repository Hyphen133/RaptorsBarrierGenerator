from shapely.geometry import Polygon, LineString
from skimage import color, measure

from min_distance_line_points import get_min_distance_pair_points, \
    return_points_on_lines_with_distance_closest_to_target_when_moving_both_points, Direction


def extract_poly_coords(geom):
    if geom.type == 'Polygon':
        exterior_coords = geom.exterior.coords[:]
        interior_coords = []
        for interior in geom.interiors:
            interior_coords += interior.coords[:]
    elif geom.type == 'MultiPolygon':
        exterior_coords = []
        interior_coords = []
        for part in geom:
            epc = extract_poly_coords(part)  # Recursive call
            exterior_coords += epc['exterior_coords']
            interior_coords += epc['interior_coords']
    else:
        raise ValueError('Unhandled geometry type: ' + repr(geom.type))
    return {'exterior_coords': exterior_coords,
            'interior_coords': interior_coords}


def extract_polygon_geometries_from_img(img, coutours_level=0.01, poly_simplification_level=20.0):
    gray = color.colorconv.rgb2grey(img)
    contours = measure.find_contours(gray, coutours_level)

    geometries = []
    for geometry_index in range(int(len(contours) / 2)):
        outer_boundary = Polygon(contours[2 * geometry_index]).simplify(poly_simplification_level)
        inner_boundary = Polygon(contours[2 * geometry_index + 1]).simplify(poly_simplification_level)
        geometries.append(Geometry(inner_boundary, outer_boundary))

    return geometries


class Geometry():
    def __init__(self, internal, external) -> None:
        super().__init__()
        self.internal = internal
        self.external = external

    def get_internal(self):
        return self.internal

    def get_external(self):
        return self.external


def divide_polygon_into_set_of_lines(polygon):
    return [LineString([polygon.boundary.coords[i], polygon.boundary.coords[i + 1]]) for i in
            range(len(polygon.boundary.coords) - 1)]


def create_additional_lines_shorter_than_threshold(external_boundary_geometry, internal_objects_geometries,
                                                   length_threshold):
    # all_boundaries = [geometry.external for geometry in internal_objects_geometries]
    # all_boundaries.append(external_boundary_geometry.internal)

    all_lines = []

    all_lines.extend(divide_polygon_into_set_of_lines(external_boundary_geometry.internal))
    for internal_object_geometry in internal_objects_geometries:
        all_lines.extend(divide_polygon_into_set_of_lines(internal_object_geometry.external))

    new_lines = []
    for line1 in all_lines:
        for line2 in all_lines:
            if line1 == line2:
                break

            # If lines interset get_min_distance_pair_points throws AssertionError
            #Drawing lines
            try:
                x, y, distance = get_min_distance_pair_points(line1, line2)
            except AssertionError:
                distance = 0

            if distance < length_threshold:
                # new_lines.append(LineString([x, y]))
                x1, y1 = return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(line1,line2,length_threshold,Direction.LEFT)
                x2, y2 = return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(line1,line2,length_threshold,Direction.RIGHT)
                new_lines.append(LineString([x1, y1]))
                new_lines.append(LineString([x2, y2]))

    return new_lines
