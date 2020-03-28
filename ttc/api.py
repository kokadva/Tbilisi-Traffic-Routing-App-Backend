import requests
import json
from geojson import MultiLineString


BUS_STOP_BUS_NUMBERS_URL = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/index/stops/{stop_id}/routes"
BUS_ROUTE_URL = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeStops?routeNumber={bus_id}&forward={direction}"
BUS_ROUTE_INFO_URL = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/routeInfo?routeNumber={bus_id}&type=bus&forward={direction}"

bus_stops = None
segmented_bus_stops = None
bus_routes = None
segments = None
bus_stops_map = None
bus_stop_bus_numbers = None
route_infos = None

# TODO decompose


def get_bus_stops_map():
    global bus_stops_map
    if bus_stops_map is None:
        with open('ttc/staticdata/bust_stops_map.json', encoding='utf-8') as json_file:
            bus_stops_map = json.load(json_file)
    return bus_stops_map


def get_bus_stops():
    global bus_stops
    if bus_stops is None:
        with open('ttc/staticdata/bus_stops.json', encoding='utf-8') as json_file:
            bus_stops = json.load(json_file)
    return bus_stops


def get_segmented_bus_stops():
    global segmented_bus_stops
    if segmented_bus_stops is None:
        with open('ttc/staticdata/segmented_bus_stops.json',
                  encoding='utf-8') as json_file:
            segmented_bus_stops = json.load(json_file)
    return segmented_bus_stops


def get_bus_routes():
    global bus_routes
    if bus_routes is None:
        with open('ttc/staticdata/bus_routes.json', encoding='utf-8') as json_file:
            bus_routes = json.load(json_file)
    return bus_routes


def get_bus_numbers(stop_id):
    url = BUS_STOP_BUS_NUMBERS_URL.format(stop_id=stop_id)
    r = requests.get(url=url)
    data = r.json()
    return data


def get_bus_route_info(bus_id, direction):
    url = BUS_ROUTE_INFO_URL.format(bus_id=bus_id, direction=direction)
    r = requests.get(url=url)
    data = r.json()
    return data


def get_bus_route(bus_id, direction='0'):
    url = BUS_ROUTE_URL.format(bus_id=bus_id, direction=direction)
    r = requests.get(url=url)
    data = r.json()
    return data


def get_segments():
    global segments
    if segments is None:
        with open('ttc/staticdata/segments.json',
                  encoding='utf-8') as json_file:
            segments = json.load(json_file)
    return segments


def get_bus_stop_bus_numbers():
    global bus_stop_bus_numbers
    if bus_stop_bus_numbers is None:
        with open('ttc/staticdata/bus_stop_numbers.json',
                  encoding='utf-8') as json_file:
            bus_stop_bus_numbers = json.load(json_file)
    return bus_stop_bus_numbers


def get_route_infos():
    global route_infos
    if route_infos is None:
        with open('ttc/staticdata/route_info.json',
                  encoding='utf-8') as json_file:
            route_infos = json.load(json_file)
    return route_infos


def flatten_route_info(route_info):
    res = []
    if 'forward' in route_info:
        res += route_info['forward']
    if 'backward' in route_info:
        res += route_info['backward']
    return res


def get_bus_routes_geojson(routes):
    route_infos = get_route_infos()
    res = []
    for route in routes:
        res += [flatten_route_info(route_infos[route])]
    return MultiLineString(res)
