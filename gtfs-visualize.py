import csv
from math import dist, sqrt
import os
import svgwrite
import math

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

feed_info_file = "feed_info.txt"
stops_file = "stops.txt"
calendar_file = "calendar_dates.txt"
trips_file = "trips.txt"
routes_file = "routes.txt"
agency_file = "agency.txt"
stop_times_file = "stop_times.txt"
transfers_file = "transfers.txt"
shapes_file = "shapes.txt"

### PARAMETERS ###
GTFS_DIR = "gvb-tram"
SVG_OUT_FILE = os.path.join("old_img", GTFS_DIR + ".svg")
PADDING = 100
WIDTH = 500
LINE_COLORS = ["#BB3636", "#FF5B1A", "#EEF608", "#A9C539", "#0CC261", "#39C5C3", "#2D80D3", "#8478F4", "#D66ECD"]
BACKGROUND_COLOR = "#222B38"

def find(fn, arr):
    return next(obj for obj in arr if fn(obj))

def loadCsv(file_name):
    with open(os.path.join(script_dir, "data", GTFS_DIR, file_name), mode="r") as f:
        return list(csv.DictReader(f))

def loadFilteredCsv(file_name, filterFn):
    with open(os.path.join(script_dir, "data", GTFS_DIR, file_name), mode="r") as f:
        return list(filter(filterFn, csv.DictReader(f)))

routes = loadCsv(routes_file)
stops = loadCsv(stops_file)
trips = loadCsv(trips_file)
    

for i, stop in enumerate(stops):
    parent_station = stop["parent_station"]
    if (parent_station != ""):
        first_occurence = [s for s in stops if s["parent_station"] == parent_station][0]
        stops[i]["stop_lat"] = first_occurence["stop_lat"]
        stops[i]["stop_lon"] = first_occurence["stop_lon"]

def stopById(stop_id):
    return find(lambda stop: stop["stop_id"] == stop_id, stops)

def firstTripForRoute(route_id):
    return [t for t in trips if t["route_id"] == route_id][0]
    # return find(lambda trip: trip["route_id"] == route_id, trips)

def stop_sequence_for_trip(trip_id):
    unsorted_stop_times = loadFilteredCsv(stop_times_file, lambda row: row["trip_id"] == trip_id)
    stop_times = sorted(unsorted_stop_times, key = lambda st: float(st["stop_sequence"]))
    return list(map(lambda s: stopById(s["stop_id"]), stop_times))

routes = [r for r in routes if len([t for t in trips if t["route_id"] == r["route_id"]]) > 0]
route_ids = [r["route_id"] for r in routes]
route_trips = [firstTripForRoute(r) for r in route_ids]
stop_sequences = [stop_sequence_for_trip(t_id) for t_id in [t["trip_id"] for t in route_trips]]
# stop_sequences = list(map(stop_sequence_for_trip, list(map(lambda t: t["trip_id"],route_trips))))
print(len(stop_sequences))


def visualize():
    border_line = loadCsv("borders.csv")

    min_lat = min(map(lambda stop: float(stop["stop_lat"]), stops))
    max_lat = max(map(lambda stop: float(stop["stop_lat"]), stops))
    min_lon = min(map(lambda stop: float(stop["stop_lon"]), stops))
    max_lon = max(map(lambda stop: float(stop["stop_lon"]), stops))

    lon_lat_ratio = math.cos(math.radians((max_lat + min_lat) / 2))
    pixel_width = WIDTH
    pixel_height = (max_lat - min_lat) / (max_lon - min_lon) / lon_lat_ratio * WIDTH

    def lonToX(lon):
        return PADDING + (float(lon) - min_lon) / (max_lon - min_lon) * pixel_width

    def latToY(lat):
        return PADDING + (max_lat - float(lat)) / (max_lat - min_lat) * pixel_height

    document_width = pixel_width + 2 * PADDING
    document_height = pixel_height + 2 * PADDING

    dwg = svgwrite.Drawing(SVG_OUT_FILE, (document_width, document_height))

    dwg.add(dwg.rect((0, 0), (document_width, document_height), 0, 0, fill = BACKGROUND_COLOR))

    border_path = [["M" if i == 0 else "L", lonToX(s["lon"]), latToY(s["lat"])] for i, s in enumerate(border_line)]
    dwg.add(dwg.path(border_path, stroke = "none", fill = "#2E3B4C", stroke_width = 2))

    def place_stop_label(route, stop):
        route_name = route["route_short_name"]
        dwg.add(dwg.text(route_name + " " + stop["stop_name"], (lonToX(stop["stop_lon"]), latToY(stop["stop_lat"])), style="font-size: 4pt; font-family: 'Roboto Slab'", fill="white"))

    for route_index, stop_sequence in enumerate(stop_sequences):
        route = routes[route_index]

        path_def = [["M" if i == 0 else "L", lonToX(s["stop_lon"]), latToY(s["stop_lat"])] for i, s in enumerate(stop_sequence)]
        color = "#" + route["route_color"] if route["route_color"] != "" else LINE_COLORS[route_index % len(LINE_COLORS)]
        path = dwg.path(path_def, stroke = color, fill = "none", stroke_width = 3)
        dwg.add(path)

    # for route_index, stop_sequence in enumerate(stop_sequences):
    #     route = routes[route_index]
    #     place_stop_label(route, stop_sequence[0])
    #     place_stop_label(route, stop_sequence[-1])


    for stop in stops:
        dwg.add(
            dwg.circle((lonToX(stop["stop_lon"]), latToY(stop["stop_lat"])), 1.5, fill = "white")
        )


    dwg.save()


visualize()