import visstart
from NetworkConfig import NetworkConfig
from ColorScheme import ColorScheme, lightColors, winterColors
from copy import deepcopy

config = NetworkConfig("gvb")
config.boundaries = ["amsterdam.geo.json"]
config.stop_area_attribute = "parent_station"
config.line_width = 2

tram_config = deepcopy(config)
tram_config.line_width = 1.5

veer_config = deepcopy(config)
veer_config.line_width = .5
veer_config.colors.line_colors = ["#5895c7"]
veer_config.draw_multi_lines = False

config.route_configs = [
    (lambda route: "tram" in route["route_url"], tram_config),
    (lambda route: "veer" in route["route_url"], veer_config)
]

visstart.start(config)