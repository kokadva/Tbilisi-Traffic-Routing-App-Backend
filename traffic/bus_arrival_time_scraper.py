import requests
from threading import Thread
from flask_app import app
from resources import db
from traffic.models import BusArrival
from ttc.api import get_bus_stops

# TODO refactor

BUS_STOP_BUS_ARRIVAL_TIMES_URL = "http://transfer.ttc.com.ge:8080/otp/routers/ttc/stopArrivalTimes?stopId={bus_stop_id}"
WORKERS_COUNT = 5


def get_bus_stop_bus_arrival_times(bus_stop_id):
    url = BUS_STOP_BUS_ARRIVAL_TIMES_URL.format(bus_stop_id=bus_stop_id)
    r = requests.get(url=url)
    return r.json()


def to_busarrival(raw_bus_stop_arrival_data, bus_stop_id):
    return BusArrival(bus_stop_id=bus_stop_id, bus_num=raw_bus_stop_arrival_data['RouteNumber'])


def remove_old_bus_arrivals(bus_arrival):
    BusArrival.query\
        .filter(BusArrival.bus_stop_id == bus_arrival.bus_stop_id)\
        .filter(BusArrival.bus_num == bus_arrival.bus_num).delete()


def bus_arrival_time_scraper_job(bus_stops, worker_index, workers_num):
    with app.app_context():
        for bus_stop_index in range(worker_index, len(bus_stops), workers_num):
            bus_stop = bus_stops[bus_stop_index]
            try:
                bus_stop_bus_arrival_times = get_bus_stop_bus_arrival_times(bus_stop['code'])['ArrivalTime']
                filtered_arrival_times = list(filter(lambda x: x['ArrivalTime'] == 0, bus_stop_bus_arrival_times))
                bus_arrivals = list(map(lambda x: to_busarrival(x, bus_stop['code']), filtered_arrival_times))
                for bus_arrival in bus_arrivals:
                    remove_old_bus_arrivals(bus_arrival)
                    db.session.add(bus_arrival)
            except Exception as e:
                # TODO handle properly
                pass
        db.session.commit()


def scrape_bus_arrival_times():
    bus_stops = get_bus_stops()
    for thread_index in range(WORKERS_COUNT):
        worker = Thread(target=bus_arrival_time_scraper_job, args=(bus_stops, thread_index, WORKERS_COUNT))
        worker.start()
