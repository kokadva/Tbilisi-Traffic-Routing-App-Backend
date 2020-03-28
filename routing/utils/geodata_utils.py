import json
import math
from geojson import MultiPoint, FeatureCollection, Feature

from routing.constants import LONGITUDE_DIVIDER, LATITUDE_DIVIDER
from ttc.api import get_bus_routes_geojson


def get_tbilisi_rectangle_coordinates():
    with open('ttc/staticdata/tbilisi_rectangle.json', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data


tbilisi_rectangle_coordinates = get_tbilisi_rectangle_coordinates()
segment_x = (tbilisi_rectangle_coordinates['rightUp']['lon'] - tbilisi_rectangle_coordinates['leftUp'][
    'lon']) / LONGITUDE_DIVIDER
segment_y = (tbilisi_rectangle_coordinates['leftUp']['lat'] - tbilisi_rectangle_coordinates['leftDown'][
    'lat']) / LATITUDE_DIVIDER


def to_segment(lon, lat, rect=tbilisi_rectangle_coordinates):
    global tbilisi_rectangle_coordinates
    x = math.ceil((lon - rect['leftUp']['lon']) / segment_x)
    y = math.ceil((rect['rightUp']['lat'] - lat) / segment_y)
    return x, y


def format_route(route):
    return list(map(lambda x: {'name': x.metadata['Name'], 'bus_num': x.bus_num}, route))


def construct_linestring(route, time):
    formated_route = format_route(route)
    feat_1 = Feature(geometry=MultiPoint(list(map(lambda x: (x.metadata['Lon'], x.metadata['Lat']), route))), properties={'time': time, 'route': formated_route})
    feat_2 = Feature(geometry=get_bus_routes_geojson(list(map(lambda x: x.bus_num, route))))
    res = FeatureCollection([feat_1,feat_2])
    return res