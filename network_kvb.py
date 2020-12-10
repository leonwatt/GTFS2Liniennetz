from ColorScheme import springColors, winterColors
import visstart
from NetworkConfig import NetworkConfig

config = NetworkConfig("kvb")
config.stop_area_attribute = "stop_id"
config.min_relative_frequency = .1


visstart.start(config)