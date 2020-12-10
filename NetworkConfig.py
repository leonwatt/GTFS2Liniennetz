from ColorScheme import ColorScheme

class NetworkConfig:
    # General properties
    gtfs = ""
    min_relative_frequency = .3
    min_absolute_frequency = 1

    # Document dimensions
    document_size = 1000
    document_aspect_ratio = 0
    document_padding = 100

    # Feature dimensions
    line_width = 3
    line_space = 1
    stop_diameter = 3

    # Feature properties
    draw_multi_lines = True
    draw_multi_lines_white = False

    # Geometrical objects
    boundaries = []

    # Normalizing paramters
    stop_area_fn = None
    stop_area_attribute = None

    # Art parameters
    art_export = False
    art_shuffle_route = False

    # Colors
    colors = ColorScheme()

    # Custom route configs, set in __init__
    route_configs = []

    def __init__(self, gtfs):
        self.gtfs = gtfs