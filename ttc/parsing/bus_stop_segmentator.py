from ttc.api import *
import json

bus_routes = get_bus_stops()
result = dict()


def save_bus_num_for_bus_stop(bus_num, route_stops):
    route_stops = route_stops['Stops']
    global result
    for stop in route_stops:
        if stop['StopId'] not in result:
            result[stop['StopId']] = set()
        result[stop['StopId']].add(bus_num)


for bus_num in bus_routes:
    bus_route = bus_routes[bus_num]
    if 'forward' in bus_route:
        save_bus_num_for_bus_stop(bus_num, bus_route['forward'])
    if 'backward' in bus_route:
        save_bus_num_for_bus_stop(bus_num, bus_route['backward'])



class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


with open('bus_stop_numbers.json', 'w', encoding='utf-8') as fp:
    json.dump(result, fp, cls=SetEncoder)
