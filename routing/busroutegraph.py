from routing.graphnode import Node
from routing.utils.geodata_utils import to_segment
from ttc.api import get_bus_routes, get_segments, get_bus_stop_bus_numbers


def get_segment_nearby_bus_stops(segment, bus_number=None, segments=get_segments(),
                                 bus_stop_bus_numbers=get_bus_stop_bus_numbers()):
    x, y = segment
    result = set()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            n_x = x + dx
            n_y = y + dy
            n_segment_id = str(n_x) + ':' + str(n_y)
            if n_segment_id not in segments:
                continue
            for bus_stop in segments[n_segment_id]['bus_stops']:
                if bus_stop not in bus_stop_bus_numbers:
                    continue
                for bus_num in bus_stop_bus_numbers[bus_stop]:
                    if bus_num == bus_number:
                        continue
                    result.add((bus_stop, bus_num))
    return result


def to_nodes(bus_number, stops, bus_routes_graph):
    result = dict()
    for i in range(len(stops)):
        stop = stops[i]
        neighbors = set()
        if i < len(stops) - 1:
            neighbors.add((stops[i + 1]['StopId'], bus_number))
        segment = to_segment(stop['Lon'], stop['Lat'])
        nearby_bus_stops = get_segment_nearby_bus_stops(segment, bus_number)
        neighbors = neighbors.union(nearby_bus_stops)
        node = Node(stop['Lon'], stop['Lat'], segment[0], segment[1], stop['Name'], stop['StopId'], bus_number,
                    neighbors, bus_routes_graph)
        result[(node.get_id(), bus_number)] = node
    return result


def build_graph():
    result = dict()
    bus_routes = get_bus_routes()
    for bus_number in bus_routes:
        bus_route = bus_routes[bus_number]
        if "forward" in bus_route:
            nodes = to_nodes(bus_number, bus_route["forward"]['Stops'], result)
            for node in nodes:
                result[node] = nodes[node]
        if "backward" in bus_route:
            nodes = to_nodes(bus_number, bus_route["backward"]['Stops'], result)
            for node in nodes:
                result[node] = nodes[node]
    return result


bus_routes_graph = build_graph()


def get_bus_routes_graph():
    global bus_routes_graph
    return bus_routes_graph
