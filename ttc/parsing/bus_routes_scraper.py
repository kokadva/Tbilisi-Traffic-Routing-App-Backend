from ttc.api import *

bus_stops = get_bus_stops()
bus_numbers = set()
bus_routes = dict()

for bus_stop in bus_stops:
    try:
        print(bus_stop)
        stop_id = bus_stop['id']
        bus_numbers = bus_numbers.union(set(list(map(lambda x: x['shortName'], get_bus_numbers(stop_id)))))
    except Exception as e:
        print('error', bus_stop)

for bus_num in bus_numbers:
    try:
        bus_routes[bus_num] = dict()
        bus_routes[bus_num]['forward'] = get_bus_route(bus_num, direction='1')
        bus_routes[bus_num]['backward'] = get_bus_route(bus_num, direction='0')
        print(bus_routes[bus_num])
    except Exception as e:
        print('error', bus_num)

with open('bus_routes.json', 'w') as fp:
    json.dump(bus_routes, fp)


