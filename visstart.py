import visprep
import visdraw
from NetworkConfig import NetworkConfig

import os
import csv

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

parameters = {}

feed_info_file = "feed_info.txt"
stops_file = "stops.txt"
calendar_file = "calendar_dates.txt"
trips_file = "trips.txt"
routes_file = "routes.txt"
agency_file = "agency.txt"
stop_times_file = "stop_times.txt"
transfers_file = "transfers.txt"
shapes_file = "shapes.txt"



def loadCsv(file_name):
    with open(os.path.join(script_dir, "data", parameters["gtfs_dir"], file_name), mode="r") as f:
        return list(csv.DictReader(f))

def start(network_config: NetworkConfig):
    parameters["gtfs_dir"] = network_config.gtfs

    routes = loadCsv(routes_file)
    stops = loadCsv(stops_file)
    trips = loadCsv(trips_file)
    stop_times = loadCsv(stop_times_file)

    stop_area_fn = network_config.stop_area_fn if (network_config.stop_area_fn is not None) else lambda s: (s[network_config.stop_area_attribute] if (network_config.stop_area_attribute) in s else s["stop_id"])

    routes_per_stop_pair, filtered_stops = visprep.prepare(routes, stops, trips, stop_times, stop_area_fn, network_config)

    visdraw.draw(filtered_stops, routes, routes_per_stop_pair, stop_area_fn, network_config)
