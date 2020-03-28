# print(LineString(list(map(lambda x: (float(x.split(':')[0]), float(x.split(':')[1])), get_route_infos()["Shape"].split(',')))))
# print(list(map(lambda x: (float(x.split(':')[0]), float(x.split(':')[1])), get_route_infos()["Shape"].split(','))))

from ttc.api import *

bus_stops = get_bus_routes()
result = dict()


def process_route(route_info):
    return list(map(lambda x: (float(x.split(':')[0]), float(x.split(':')[1])), route_info["Shape"].split(',')))


for bus_id in bus_stops:

    result[bus_id] = dict()
    if bus_id == 'I ხაზი (ახმეტელი/ვარკეთილი)':
        continue
    try:
        result[bus_id]['forward'] = process_route(get_bus_route_info(bus_id, '0'))
    except:
        print('error')
    try:
        result[bus_id]['backward'] = process_route(get_bus_route_info(bus_id, '1'))
    except:
        print("error")


with open('route_info.json', 'w') as fp:
    json.dump(result, fp)


