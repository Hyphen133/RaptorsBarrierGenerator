from src.api.barrier_generation_controller import BarrierGenerationFacade
from src.map_processing.map_loading import FilePathMapLoader
from src.visualization.polygons_visualization import show_polygons
from tests.resource_loader import ResourceLoader
import matplotlib.pyplot as plt
config = [
    ('apartment.pgm',10, (75,250)),
    ('factory_map.pgm', ),
    ('demoGeniale.pgm', ),
    ('hefei_arenaA.pgm', ),
    ('hefei_version1.pgm', ),
    ('map042013.pgm', ),
    ('masterpiece.pgm', ),
    ('wm2013.pgm', )]

resource_loader = ResourceLoader()
barrier_generator = BarrierGenerationFacade()


map_name, robot_diamater, robot_starting_position = config[0]
map_filepath = resource_loader.get_test_map_filepath(map_name)
map_image = FilePathMapLoader(map_filepath).load_image()

impassable_polygons = barrier_generator.generate_barriers(map_image)

plt.title("Impassable regions")
show_polygons(impassable_polygons)