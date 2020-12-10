import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("ns-spr")
config.stop_area_attribute = "parent_station"
config.draw_multi_lines = False
config.min_absolute_frequency = 10
config.boundaries = ["nl.geo.json"]
config.document_padding = 500

visstart.start(config)