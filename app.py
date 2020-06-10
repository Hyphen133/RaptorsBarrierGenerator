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
from urllib.parse import urljoin
import numpy as np
from io import BytesIO
import yaml
load_dotenv()

app = Flask(__name__)


@app.route('/')
def index():
    map_folder_name = request.args.get('map_folder_name')
    map_file_name = request.args.get('map_file_name')
    robot_diameter = int(request.args.get('robot_diameter'))
    # robot_starting_x = int(request.args.get('robot_starting_x'))
    # robot_starting_y = int(request.args.get('robot_starting_y'))



    start = timeit.default_timer()

    file_url = urljoin(os.environ.get('database-url'), ''.join([map_folder_name,'/', map_file_name]))

    map_pgm = get_files(''.join([file_url, '.pgm']))
    map_pgm = Image.open(BytesIO(map_pgm))
    map_yaml = get_files(''.join([file_url, '.yaml']))

    map_yaml = yaml.load(map_yaml, Loader=yaml.FullLoader)
    print(np.array(map_pgm).size)




    robot_starting_position = (int(abs(map_yaml['origin'][0])), int(abs(map_yaml['origin'][1])))
    robot_starting_position = (2000,2000)
    
    bgf = BarrierGenerationFacade()

    barriers = bgf.generate_barriers(map_pgm, robot_diameter, robot_starting_position)

    all_polygons = []
    for polygon in barriers:
        polygon_s = []
        for vertex in list(polygon.exterior.coords):
            polygon_s.append('({},{})'.format(int(round(vertex[0])), int(round(vertex[1]))))
        all_polygons.append('[{}]'.format(','.join(polygon_s)))
    all_polygons = '[{}]'.format(','.join(all_polygons))

    stop = timeit.default_timer()

    return all_polygons

@app.route('/dummy_map')
def index2():
    robot_diameter = int(request.args.get('robot_diameter'))
    robot_starting_x = int(request.args.get('robot_starting_x'))
    robot_starting_y = int(request.args.get('robot_starting_y'))

    robot_starting_position = (robot_starting_x, robot_starting_y)

    start = timeit.default_timer()

    path = 'test_resources/maps/apartment.pgm'

    map_pgm = Image.open(path, 'r')
    bgf = BarrierGenerationFacade()

    barriers = bgf.generate_barriers(map_pgm, robot_diameter, robot_starting_position)

    all_polygons = []
    for polygon in barriers:
        polygon_s = []
        for vertex in list(polygon.exterior.coords):
            polygon_s.append('({},{})'.format(int(round(vertex[0])), int(round(vertex[1]))))
        all_polygons.append('[{}]'.format(','.join(polygon_s)))
    all_polygons = '[{}]'.format(','.join(all_polygons))

    stop = timeit.default_timer()

    return all_polygons


@app.route('/performance_test')
def performance_test():
    robot_starting_position = (75, 250)

    start = timeit.default_timer()

    path = 'test_resources/maps/apartment.pgm'

    map_pgm = Image.open(path, 'r')
    bgf = BarrierGenerationFacade()

    barriers = bgf.generate_barriers(map_pgm, 10, robot_starting_position)
    stop = timeit.default_timer()

    performance_test_result = {'apartment': 'apartment.pgm', 'passed': True, 'time': stop-start}
    return jsonify(performance_test_result)


@app.route('/map_request_test')
def map_request_test():
    map_folder_name = request.args.get('map_folder_name')
    map_file_name = request.args.get('map_file_name')

    start = timeit.default_timer()
    file_url = urljoin(os.environ.get('database-url'), ''.join([map_folder_name,'/', map_file_name]))

    map_pgm = get_files(''.join([file_url, '.pgm']))
    map_yaml = get_files(''.join([file_url, '.yaml']))


    stop = timeit.default_timer()
    performance_test_result = {'time': stop-start, 'passed': True}
    return jsonify(performance_test_result)


def get_files(path):
    response_pgm = urllib.request.urlopen(path)
    map_pgm = response_pgm.read()
    return map_pgm


if __name__ == '__main__':
    app.run(debug=True)
