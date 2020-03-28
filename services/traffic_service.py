from geojson import FeatureCollection, Point, Feature
from traffic.models import BusArrival
from ttc.api import get_bus_routes
from sqlalchemy import func

from ttc.bus_schedule_api import get_bus_scheduled_arrival_time


def bus_stop_to_point(bus_stop_data):
    return Feature(geometry=Point((bus_stop_data['lon'], bus_stop_data['lat'])),
                   properties=bus_stop_data)


def get_bus_route_bus_stops(bus_num):
    bus_routes = get_bus_routes()
    bus_route = bus_routes[bus_num]
    bus_route_stops = []
    if 'forward' in bus_route:
        bus_route_stops += bus_route['forward']['Stops']
    if 'backward' in bus_route:
        bus_route_stops += bus_route['backward']['Stops']
    return bus_route_stops


def get_bus_route_stops_live_arrival_times(bus_num):
    return BusArrival.query.with_entities(BusArrival.bus_stop_id,
                                          func.max(BusArrival.arrival_time)).filter(
        BusArrival.bus_num == bus_num).group_by(
        BusArrival.bus_stop_id).all()


def get_bus_route_stops_shceduled_arrival_times(bus_num, bus_stop_live_arrival_times):
    return list(map(lambda x: get_bus_scheduled_arrival_time(bus_num, x[0], x[1]), bus_stop_live_arrival_times))


def to_bus_stops_dict(bus_route_stops):
    bus_stops_dict = dict()
    for bus_stop in bus_route_stops:
        bus_stops_dict[bus_stop['StopId']] = bus_stop
    return bus_stops_dict


def to_traffic(bus_num, bus_stop_live_arrival_times, bus_stop_scheduled_arrival_times, bus_stops_dict):
    res = []
    for i in range(len(bus_stop_live_arrival_times)):
        bus_arrival_time = bus_stop_live_arrival_times[i]
        by_schedule = bus_stop_scheduled_arrival_times[i]
        by_realtime = bus_arrival_time[1]
        res.append(
            {'id': bus_arrival_time[0],
             'bus_num': bus_num,
             'lon': bus_stops_dict[bus_arrival_time[0]]['Lon'],
             'lat': bus_stops_dict[bus_arrival_time[0]]['Lat'],
             'name': bus_stops_dict[bus_arrival_time[0]]['Name'],
             'traffic': (by_realtime - by_schedule).total_seconds()
             })
    return res


def bus_route_traffic_to_feature_collection(bus_route_traffic):
    bus_stop_points = list(map(bus_stop_to_point, bus_route_traffic))
    return FeatureCollection(bus_stop_points)


def get_bus_route_traffic(bus_num):
    bus_route_stops = get_bus_route_bus_stops(bus_num)
    bus_stop_live_arrival_times = get_bus_route_stops_live_arrival_times(bus_num)
    bus_stop_scheduled_arrival_times = get_bus_route_stops_shceduled_arrival_times(bus_num, bus_stop_live_arrival_times)
    bus_stops_dict = to_bus_stops_dict(bus_route_stops)
    bus_route_traffic = to_traffic(bus_num, bus_stop_live_arrival_times, bus_stop_scheduled_arrival_times,
                                   bus_stops_dict)
    return bus_route_traffic_to_feature_collection(bus_route_traffic)

