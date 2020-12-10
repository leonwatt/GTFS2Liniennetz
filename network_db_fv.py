import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("db-fv")
config.stop_area_attribute = "stop_id"
config.draw_multi_lines = False
config.min_relative_frequency = .2
config.min_absolute_frequency = 4
# config.boundaries = ["germany.geo.json"]


# config.art_export = True
# config.art_shuffle_route = True
# config.min_frequency_threshold = 0
# config.line_width = .5
# config.stop_diameter = 2

visstart.start(config)