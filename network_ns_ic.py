import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("ns-ic")
config.stop_area_attribute = "parent_station"
config.draw_multi_lines = False
config.min_absolute_frequency = 10

visstart.start(config)