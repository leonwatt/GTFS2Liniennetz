from copy import deepcopy
import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("nl-trein")
config.stop_area_attribute = "parent_station"
config.draw_multi_lines = False
config.min_absolute_frequency = 10
config.min_relative_frequency = .2
config.boundaries = ["nl.geo.json"]


sprinter_config = deepcopy(config)
sprinter_config.colors = deepcopy(sprinter_config.colors)
sprinter_config.colors.line_colors = ["white"]
sprinter_config.line_width = .5

config.route_configs = [
    (lambda route: route["route_short_name"] != "Intercity", sprinter_config)
]

visstart.start(config)