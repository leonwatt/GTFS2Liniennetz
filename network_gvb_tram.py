import visstart
from NetworkConfig import NetworkConfig
from ColorScheme import ColorScheme, lightColors, winterColors

config = NetworkConfig("gvb-tram")
config.boundaries = ["amsterdam.geo.json"]
config.stop_area_attribute = "parent_station"

# colors = lightColors()
# colors.override_route_colors = True

# config.colors = colors

# config.art_export = True
# config.art_shuffle_route = True
# config.min_frequency_threshold = 0
# config.line_width = .5
# config.stop_diameter = 2

visstart.start(config)