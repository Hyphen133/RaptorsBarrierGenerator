from PIL import Image
from flask import Flask
import urllib.request
import timeit
import os
from src.api.barrier_generation_controller import BarrierGenerationFacade
from tests.resource_loader import ResourceLoader

app = Flask(__name__)

URL = 'http://s000.tinyupload.com/download.php?file_id=59102213236179943709&t=5910221323617994370949353'

@app.route('/')
def index():
    start = timeit.default_timer()

    # map_pgm = get_files(URL)
    path =  ResourceLoader().get_test_map_filepath('apartment.pgm')
    print(path)
    print()
    map_pgm = Image.open(path, 'r')
    bgf = BarrierGenerationFacade()
    barriers = bgf.generate_barriers(map_pgm,30,(0,0))

    print(barriers)

    stop = timeit.default_timer()

    return 'Time to fetch all 3 map related files: {}'.format(stop - start)

def get_files(path):
    # response_png = urllib.request.urlopen(path + '.png')
    # map_png = response_png.read()
    response_pgm = urllib.request.urlopen(path)
    map_pgm = response_pgm.read()
    # response_yaml = urllib.request.urlopen(path + '.yaml')
    # map_yaml = response_yaml.read()
    return map_pgm

if __name__ == '__main__':
    app.run(debug=True)
