import csv
import re
from pathlib import Path
import os

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in

feed_info_file = "feed_info.txt"
stops_file = "stops.txt"
calendar_file = "calendar_dates.txt"
trips_file = "trips.txt"
routes_file = "routes.txt"
agency_file = "agency.txt"
stop_times_file = "stop_times.txt"
transfers_file = "transfers.txt"
shapes_file = "shapes.txt"


INPUT_DIR = "nlov-reduced"
# INPUT_DIR = "delfi-reduced"

OUTPUT_DIR = "gvb"
DATE = "20201215"


def AGENCY_FILTER(agency): return agency["agency_id"] == "GVB"
def ROUTE_FILTER(route): return "bus" not in route["route_url"]


def in_path(file_name):
    return os.path.join(script_dir, "data-raw", INPUT_DIR, file_name)


def out_path(file_name):
    return os.path.join(script_dir, "data", OUTPUT_DIR, file_name)


def loadCsv(file_name):
    with open(in_path(file_name), mode="r") as f:
        return list(csv.DictReader(f))


def filter_file(file_name, filter, ignore_if_not_existing = False):
    file_in_path = in_path(file_name)

    if ignore_if_not_existing and not Path(file_in_path).is_file():
        print("File {} not existing. Skip.".format(file_name))
    else:
        #input file reader
        infile = open(file_in_path, "r")
        read = csv.reader(infile)
        headers = next(read)  # header

        #output file writer
        outfile = open(out_path(file_name), "w")
        write = csv.writer(outfile)

        write.writerow(headers)  # write headers

        #for each row
        for row in read:
            parsed_row = {headers[i]: content for i, content in enumerate(row)}
            if filter(parsed_row):
                write.writerow(row)


def load_filtered_ids(file_name, csv_key):
    with open(out_path(file_name), mode="r") as f:
        return set(map(lambda x: x[csv_key], [el for el in csv.DictReader(f) if csv_key in el]))


def filter_feed_info():
    filter_file(feed_info_file, (lambda x: True), ignore_if_not_existing=True)


def filter_agencies():
    filter_file(agency_file, (lambda x: AGENCY_FILTER(x)))


def filter_calendar_dates(date):
    filter_file(calendar_file, (lambda x: date == "" or (x["date"] == date)))


def filter_routes(agency_ids):
    filter_file(routes_file, (lambda x: ROUTE_FILTER(x)
                              and x["agency_id"] in agency_ids))


def filter_trips(service_ids, route_ids):
    def is_valid_trip(trip):
        return trip["service_id"] in service_ids and trip["route_id"] in route_ids

    filter_file(trips_file, (lambda x: is_valid_trip(x)))


def filter_stop_times(trip_ids):
    filter_file(stop_times_file, (lambda st: st["trip_id"] in trip_ids))


def filter_stops(stop_ids):
    filter_file(stops_file, (lambda x: x["stop_id"] in stop_ids))


def filter_transfers(stop_ids, trip_ids):
    def is_valid_transfer(transfer):
        return ("from_stop" in transfer and "to_stop" in transfer and transfer["from_stop"] in stop_ids and transfer["to_stop"] in stop_ids) or ("from_trip" in transfer and "to_trip" in transfer and transfer["from_trip"] in trip_ids and transfer["to_trip"] in trip_ids)

    filter_file(transfers_file, (lambda x: is_valid_transfer(x)), ignore_if_not_existing=True)


def filter_shapes(shape_ids):
    filter_file(shapes_file, (lambda x: x["shape_id"] in shape_ids), ignore_if_not_existing=True)


Path(out_path("")).mkdir(parents=True, exist_ok=True)

print("Processing feed info ...")
filter_feed_info()

print("Processing agencies ...")
filter_agencies()

agency_ids = load_filtered_ids(agency_file, "agency_id")

print("Processing routes ...")
filter_routes(agency_ids)
route_ids = load_filtered_ids(routes_file, "route_id")

print("Processing calendar dates ...")
filter_calendar_dates(DATE)
service_ids = load_filtered_ids(calendar_file, "service_id")

print("Processing trips ...")
filter_trips(service_ids, route_ids)
trip_ids = load_filtered_ids(trips_file, "trip_id")
shape_ids = load_filtered_ids(trips_file, "shape_id")

print("Processing stop times ...")
filter_stop_times(trip_ids)
stop_ids = load_filtered_ids(stop_times_file, "stop_id")

print("Processing stops ...")
filter_stops(stop_ids)

print("Processing transfers ...")
filter_transfers(stop_ids, trip_ids)

print("Processing shapes ...")
filter_shapes(shape_ids)

print("Done.")
