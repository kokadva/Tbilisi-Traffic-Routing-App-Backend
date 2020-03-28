from ttc.api import *
import json

segmented_bus_stops = get_segmented_bus_stops()
result = dict()


for stop_id in segmented_bus_stops:
    bus_stop_segment = segmented_bus_stops[stop_id]['segment']
    if bus_stop_segment['id'] not in result:
        result[bus_stop_segment['id']] = dict()
        result[bus_stop_segment['id']]['x'] = bus_stop_segment['x']
        result[bus_stop_segment['id']]['y'] = bus_stop_segment['y']
        result[bus_stop_segment['id']]['bus_stops'] = set()
    result[bus_stop_segment['id']]['bus_stops'].add(stop_id)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


with open('segments.json', 'w', encoding='utf-8') as fp:
    json.dump(result, fp, cls=SetEncoder)
