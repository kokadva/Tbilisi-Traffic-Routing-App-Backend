from routing.astar import calculate_route
from geojson import FeatureCollection, Point, Feature


def bus_stop_to_point(bus_stop):
    return Feature(geometry=Point((bus_stop.lon, bus_stop.lat)),
                   properties={'bus_num': bus_stop.bus_num, 'bus_stop_name': bus_stop.bus_stop_name})


def to_multipoint(route, metadata):
    points = list(map(bus_stop_to_point, route))
    result = FeatureCollection(points, properties=metadata)
    return result


def get_route(coordinates_a, coordinates_b):
    route, time = calculate_route(coordinates_a[0], coordinates_a[1], coordinates_b[0], coordinates_b[1])
    multipoint_geojson = to_multipoint(route, {'time': time})
    return multipoint_geojson

