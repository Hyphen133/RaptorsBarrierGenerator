from PIL import Image
from flask import Flask
import urllib.request
import timeit
import os
from src.api.barrier_generation_controller import BarrierGenerationFacade
from tests.resource_loader import ResourceLoader
from flask import jsonify, request
from src.map_processing.map_loading import MapLoader
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    robot_diameter = int(request.args.get('robot_diameter'))
    robot_starting_x = int(request.args.get('robot_starting_x'))
    robot_starting_y = int(request.args.get('robot_starting_y'))

    robot_starting_position = (robot_starting_x, robot_starting_y)

    start = timeit.default_timer()

    # map_pgm = get_files(URL)
    path = 'test_resources/maps/apartment.pgm'

    map_pgm = Image.open(path, 'r')
    bgf = BarrierGenerationFacade()

    barriers = bgf.generate_barriers(map_pgm, robot_diameter, robot_starting_position)

    all_polygons = []
    for generated_polygons in barriers:
        generated_polygons_s = []
        for polygon in generated_polygons:
            polygon_s = []
            for vertex in list(polygon.exterior.coords):
                polygon_s.append('({},{})'.format(vertex[0], vertex[1]))
            generated_polygons_s.append('[{}]'.format(','.join(polygon_s)))
        all_polygons.append(','.join(generated_polygons_s))
    all_polygons = '[{}]'.format(','.join(all_polygons))

    stop = timeit.default_timer()

    return all_polygons


@app.route('/performance_tests')
def performance_test():
    test_map_name = request.args.get('test_map_name')

    performance_test_result = {'accuracy': 0.96, 'test_map_name': test_map_name, 'passed': True, 'time': 0.1}
    return jsonify(performance_test_result)


@app.route('/map_request_test')
def map_request_test():
    database_config = {}
    map_loader = MapLoader(database_config)
    performance_test_result = {'time': 0.1, 'passed': True, 'db': os.environ.get('database-url')}
    return jsonify(performance_test_result)


def get_files(path):
    response_pgm = urllib.request.urlopen(path)
    map_pgm = response_pgm.read()
    return map_pgm


if __name__ == '__main__':
    app.run(debug=True)
