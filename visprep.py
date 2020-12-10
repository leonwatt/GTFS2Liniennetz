from NetworkConfig import NetworkConfig
from typing import Dict
import random


def prepare(routes, stops, trips, stop_times, stop_area_fn, config: NetworkConfig):
    stop_area_per_stop_point: Dict[str, str] = {}
    stop_times_per_trip: Dict[str, list[Dict]] = {}
    routes_per_stop_pair: Dict[str, set[str]] = {}

    for i, stop in enumerate(stops):
        stop_area_id = stop_area_fn(stop)
        stop_area_per_stop_point[stop["stop_id"]] = stop_area_id
        if (stop_area_id != ""):
            first_occurence = [s for s in stops if stop_area_fn(s) == stop_area_id][0]
            stops[i]["stop_lat"] = first_occurence["stop_lat"]
            stops[i]["stop_lon"] = first_occurence["stop_lon"]

    
    for st in stop_times:
        trip_id = st["trip_id"]
        if (trip_id in stop_times_per_trip):
            stop_times_per_trip[trip_id] += [st]
        else:
            stop_times_per_trip[trip_id] = [st]

    for trip_id in stop_times_per_trip:
        stop_times_per_trip[trip_id] = sorted(stop_times_per_trip[trip_id], key = lambda st: float(st["stop_sequence"]))

        if config.art_shuffle_route:
            random.shuffle(stop_times_per_trip[trip_id])

    for rou in routes:
        r_id = rou["route_id"]
        route_trips = [t for t in trips if t["route_id"] == r_id]
        pair_frequency: Dict[str, int] = {}
        for tr in route_trips:
            trip_stop_times = stop_times_per_trip[tr["trip_id"]]
            for first_st_index, first_st in enumerate(trip_stop_times[:-1]):
                second_st = trip_stop_times[first_st_index + 1]
                key_set = set(map(lambda st: stop_area_per_stop_point[st["stop_id"]], [first_st, second_st]))
                if len(key_set) == 2:
                    key = repr(key_set)
                    if (key in pair_frequency):
                        pair_frequency[key] += 1
                    else:
                        pair_frequency[key] = 1
        
        for pair in pair_frequency:
            if (pair_frequency[pair] / len(route_trips)) >= config.min_relative_frequency and len(route_trips) >= config.min_absolute_frequency:
                if pair in routes_per_stop_pair:
                    routes_per_stop_pair[pair].add(r_id)
                else:
                    routes_per_stop_pair[pair] = set([r_id])


    pairs = [eval(pair) for pair in routes_per_stop_pair]
    filtered_stops = [stop for stop in stops if len([p for p in pairs if (stop_area_fn(stop) in p)]) > 0]

    return routes_per_stop_pair, filtered_stops