from NetworkConfig import NetworkConfig
import math
import svgwrite
import os
import json

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

def loadJson(folder, file_name):
    with open(os.path.join(script_dir, folder, file_name), mode="r") as f:
        return json.load(f)

def draw(stops, routes, routes_per_stop_pair, stop_area_fn, config: NetworkConfig):
    min_lat = min(map(lambda stop: float(stop["stop_lat"]), stops))
    max_lat = max(map(lambda stop: float(stop["stop_lat"]), stops))
    min_lon = min(map(lambda stop: float(stop["stop_lon"]), stops))
    max_lon = max(map(lambda stop: float(stop["stop_lon"]), stops))

    lon_lat_ratio = math.cos(math.radians((max_lat + min_lat) / 2))
    pixel_width = config.document_size
    pixel_height = (max_lat - min_lat) / (max_lon - min_lon) / lon_lat_ratio * config.document_size

    def lonToX(lon):
        return config.document_padding + (float(lon) - min_lon) / (max_lon - min_lon) * pixel_width

    def latToY(lat):
        return config.document_padding + (max_lat - float(lat)) / (max_lat - min_lat) * pixel_height

    document_width = pixel_width + 2 * config.document_padding
    document_height = pixel_height + 2 * config.document_padding

    img_name = config.gtfs
    if config.art_export:
        img_name += "_art"
    dwg = svgwrite.Drawing(os.path.join("img", img_name + ".svg"), (document_width, document_height))

    dwg.add(dwg.rect((0, 0), (document_width, document_height), 0, 0, fill = config.colors.background_color))

    boundary_files = [loadJson("boundaries", file) for file in config.boundaries]
    for file in boundary_files:
        boundary_feature_geometries = [feature["geometry"] for feature in file["features"]]
        for feature_geometry in boundary_feature_geometries:
            polygons = []
            if feature_geometry["type"] == "Polygon":
                polygons = [feature_geometry["coordinates"][0]]
            elif feature_geometry["type"] == "MultiPolygon":
                polygons = feature_geometry["coordinates"][0]
            for polygon in polygons:
                boundary_path = []
                for coordinate in polygon:
                    boundary_path += (["M"] if len(boundary_path) == 0 else ["L"])
                    boundary_path += [lonToX(coordinate[0]), latToY(coordinate[1])]
                dwg.add(dwg.path(boundary_path, fill = "black" if config.colors.light_background else "white", opacity = .05))

    def route_by_id(route_id: str):
        return next((r for r in routes if r["route_id"] == route_id), None)

    def stop_by_area_id(stop_area_id: str):
        return next(obj for obj in stops if stop_area_fn(obj) == stop_area_id)

    def first_and_second_stop(stop_area_id_set):
        l = [stop_by_area_id(s_area_id) for s_area_id in list(stop_area_id_set)]
        return (l[0], l[1])

    
    for pair_string in routes_per_stop_pair:
        first, second = first_and_second_stop(eval(pair_string))
        route_ids_for_pair = routes_per_stop_pair[pair_string]

        x1 = lonToX(first["stop_lon"])
        x2 = lonToX(second["stop_lon"])
        y1 = latToY(first["stop_lat"])
        y2 = latToY(second["stop_lat"])

        if x1 != x2 or y1 != y2:

            alpha = math.asin((y2 - y1) / math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
            first_line_shift = (config.line_width + config.line_space) * (len(route_ids_for_pair) - 1) / 2
            shift_per_line = -2 * first_line_shift / (len(route_ids_for_pair) - 1) if len(route_ids_for_pair) > 1 else 0

            for route_index, route_id in enumerate(route_ids_for_pair):
                route_config: NetworkConfig = next((r_conf for (r_conf_fn, r_conf) in config.route_configs if r_conf_fn(route_by_id(route_id))), config)

                default_line_colors = route_config.colors.line_colors
                line_colors = {r["route_id"]: "#" + r["route_color"] if "route_color" in r and r["route_color"] != "" and not route_config.colors.override_route_colors else default_line_colors[i % len(default_line_colors)] for i, r in enumerate(routes)}


                shift_x = (lambda x: (math.sin(alpha) * (first_line_shift + route_index * shift_per_line) + x) if route_config.draw_multi_lines else x)
                shift_y = (lambda y: (-math.cos(alpha) * (first_line_shift + route_index * shift_per_line) + y) if route_config.draw_multi_lines else y)
                path_def = ["M", shift_x(x1), shift_y(y1), "L", shift_x(x2), shift_y(y2)]

                color = line_colors[route_id] if route_config.draw_multi_lines or len(route_ids_for_pair) == 1 or not route_config.draw_multi_lines_white else "white"

                dwg.add(dwg.path(path_def, stroke = color, fill = "none", stroke_width = route_config.line_width, class_="route-{}".format(route_id)))


    for stop in stops:
        dwg.add(
            dwg.circle((lonToX(stop["stop_lon"]), latToY(stop["stop_lat"])), config.stop_diameter / 2, fill = "white", id = stop["stop_id"])
        )


    dwg.save()
    print("Done.")