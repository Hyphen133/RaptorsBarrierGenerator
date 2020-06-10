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
    # Get parameters
    map_folder_name = request.args.get('map_folder_name')
    map_file_name = request.args.get('map_file_name')
    robot_diameter = int(request.args.get('robot_diameter'))

    # Combine database-url, folder name and map name to get full file url
    file_url = urljoin(os.environ.get('database-url'), ''.join([map_folder_name,'/', map_file_name]))

    # Using file url fetch pgm and yaml files files 
    map_pgm = get_pgm_from_path(''.join([file_url, '.pgm']))
    map_yaml = get_yaml_from_path(''.join([file_url, '.yaml']))

    # Calculate robot starting position using map size, resolution and starting position
    dimentions = np.array(map_pgm).shape
    resolution = map_yaml['resolution']
    robot_starting_position = (dimentions[0] + map_yaml['origin'][0] * resolution, dimentions[1] + map_yaml['origin'][1] * resolution)
    
    # Generate barrier polygons for selected map
    bgf = BarrierGenerationFacade()
    barriers = bgf.generate_barriers(map_pgm, robot_diameter, robot_starting_position)

    # Parse polygons to string and return
    return polygons_to_string(barriers)

@app.route('/dummy_map')
def index2():
    robot_diameter = int(request.args.get('robot_diameter'))
    robot_starting_x = int(request.args.get('robot_starting_x'))
    robot_starting_y = int(request.args.get('robot_starting_y'))

    robot_starting_position = (robot_starting_x, robot_starting_y)

    start = timeit.default_timer()

    map_pgm = Image.open('test_resources/maps/apartment.pgm', 'r')
    
    bgf = BarrierGenerationFacade()
    barriers = bgf.generate_barriers(map_pgm, robot_diameter, robot_starting_position)

    stop = timeit.default_timer()

    dummpy_map_test_result = {'map': 'apartment.pgm', 'polygons': polygons_to_string(barriers), 'time': stop-start}
    return jsonify(dummpy_map_test_result)


@app.route('/performance_test')
def performance_test():
    robot_starting_position = (75, 250)

    start = timeit.default_timer()

    path = 'test_resources/maps/apartment.pgm'

    map_pgm = Image.open(path, 'r')
    bgf = BarrierGenerationFacade()

    barriers = bgf.generate_barriers(map_pgm, 10, robot_starting_position)
    stop = timeit.default_timer()

    performance_test_result = {'map': 'apartment.pgm', 'passed': True, 'time': stop-start}
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

# HELPERS

def get_files(path):
    response = urllib.request.urlopen(path)
    return response.read()

def get_pgm_from_path(path):
    response = urllib.request.urlopen(path)
    pgm_file =  response.read()
    return Image.open(BytesIO(pgm_file))

def get_yaml_from_path(path):
    response = urllib.request.urlopen(path)
    yaml_file = response.read()
    return yaml.load(yaml_file, Loader=yaml.FullLoader)

def polygons_to_string(polygons):
    all_polygons = []
    for polygon in polygons:
        polygon_s = []
        for vertex in list(polygon.exterior.coords):
            polygon_s.append('({},{})'.format(int(round(vertex[0])), int(round(vertex[1]))))
        all_polygons.append('[{}]'.format(','.join(polygon_s)))
    all_polygons = '[{}]'.format(','.join(all_polygons))
    return all_polygons



if __name__ == '__main__':
    app.run(debug=True)
