from shapely.geometry import LineString, Point

from src.barrier_generator.min_distance_utils import get_min_distance_pair_points, convert_line_to_formula, \
    calculate_delta_x, line_contains_point, Direction, get_intersection_points


class BarrierGenerator():
    def __init__(self,robot_config) -> None:
        super().__init__()
        self.robot_config = robot_config

    def generate_barrier_boundaries(self, geometries_list):
        external_boundary_geometry, internal_object_geometries = self.extract_internal_and_external_boundaries(geometries_list)
        new_lines = self.create_additional_lines_shorter_than_threshold(external_boundary_geometry, internal_object_geometries, self.robot_config.get_diameter())

    def extract_internal_and_external_boundaries(self, geometries):
        external_boundary_geometry = geometries[0]
        internal_object_geometries = []
        if len(geometries) > 1:
            internal_object_geometries.extend(geometries[1:])

        return external_boundary_geometry, internal_object_geometries


    def create_additional_lines_shorter_than_threshold(self,external_boundary_geometry, internal_objects_geometries,
                                                       length_threshold):

        # Extracting all lines that are that repserent inner line of external boundary and outer lines of internal objects
        all_lines = []
        all_lines.extend(self.divide_polygon_into_set_of_lines(external_boundary_geometry.get_internal_boundary()))
        for internal_object_geometry in internal_objects_geometries:
            all_lines.extend(self.divide_polygon_into_set_of_lines(internal_object_geometry.get_external_boundary()))

        new_lines = []
        for line1 in all_lines:
            for line2 in all_lines:
                if line1 == line2:
                    break

                # If lines already interset get_min_distance_pair_points throws AssertionError
                try:
                    x, y, distance = get_min_distance_pair_points(line1, line2)
                except AssertionError:
                    distance = 0

                if distance < length_threshold:
                    #There are 2 cases we can move to left/right from min distance point
                    #TODO -> fix point line generation on edges
                    point_left_1, point_left_2 = self.return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(line1,
                                                                                                            line2,
                                                                                                            length_threshold,
                                                                                                            Direction.LEFT)
                    point_right_1, point_right_2 = self.return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(line1,
                                                                                                            line2,
                                                                                                            length_threshold,
                                                                                                            Direction.RIGHT)
                    new_lines.append(LineString([point_left_1, point_left_2]))
                    new_lines.append(LineString([point_right_1, point_right_2]))

        return new_lines

    def divide_polygon_into_set_of_lines(self,polygon):
        return [LineString([polygon.boundary.coords[i], polygon.boundary.coords[i + 1]]) for i in
                range(len(polygon.boundary.coords) - 1)]

    def return_points_on_lines_with_distance_closest_to_target_when_moving_both_points(self, line1, line2,
                                                                                       target_distance, direction,
                                                                                       delta_y=1):
        line1_formula = convert_line_to_formula(line1)
        line2_formula = convert_line_to_formula(line2)

        current_point_on_line1, current_point_on_line2, current_distance = self.get_minimum_distance_points_for_lines(line1, line2)

        is_line1_point_on_edge = False
        is_line2_point_on_edge = False

        while not (is_line1_point_on_edge and is_line2_point_on_edge) and current_distance < target_distance:
            # Update points
            new_line_point_x1 = current_point_on_line1[0] + direction.value * calculate_delta_x(line1_formula, delta_y)
            new_line_point_x2 = current_point_on_line2[0] + direction.value * calculate_delta_x(line2_formula, delta_y)

            # if not is_line1_point_on_edge:
            new_candidate_point_on_line1 = (new_line_point_x1, line1_formula(new_line_point_x1))
            # if not is_line2_point_on_edge:
            new_candidate_point_on_line2 = (new_line_point_x2, line2_formula(new_line_point_x2))

            if line_contains_point(line1, Point(new_candidate_point_on_line1)):
                current_point_on_line1 = new_candidate_point_on_line1
            else:
                is_line1_point_on_edge = True

            if line_contains_point(line2, Point(new_candidate_point_on_line2)):
                current_point_on_line2 = new_candidate_point_on_line2
            else:
                is_line2_point_on_edge = True

            current_distance = Point(current_point_on_line1).distance(Point(current_point_on_line2))

        return current_point_on_line1, current_point_on_line2

    def get_minimum_distance_points_for_lines(self, line1, line2):
        try:
            current_point_on_line1, current_point_on_line2, current_distance = get_min_distance_pair_points(line1,
                                                                                                       line2)
        except AssertionError:
            current_distance = 0
            current_point_on_line1,  current_point_on_line2 = get_intersection_points(line1,line2)

        return current_point_on_line1, current_point_on_line2, current_distance
