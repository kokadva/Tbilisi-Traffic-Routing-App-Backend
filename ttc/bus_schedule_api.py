import json
import datetime

WEEK_DAYS = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
bus_schedule = None


def get_bus_schedules():
    global bus_schedule
    if bus_schedule is None:
        with open('ttc/staticdata/bus_schedules.json', encoding='utf-8') as json_file:
            bus_schedule = json.load(json_file)
    return bus_schedule


def get_bus_stops_schedule(cur_day, schedule_data):
    weekday_schedules = schedule_data['WeekdaySchedules']
    for weekdaySchedule in weekday_schedules:
        from_day = WEEK_DAYS[weekdaySchedule['FromDay'].lower()]
        to_day = WEEK_DAYS[weekdaySchedule['ToDay'].lower()]
        if from_day <= cur_day <= to_day:
            return weekdaySchedule['Stops']
    return []


def get_bus_stop_arrival_times(stops, stop_id):
    for stop in stops:
        if stop['StopId'] == str(stop_id):
            return stop['ArriveTimes']
    return None


def to_datetime(arrival_time, date_from):
    return datetime.datetime(date_from.year, date_from.month, date_from.day,
                             hour=int(arrival_time.split(':')[0]) % 24,
                             minute=int(arrival_time.split(':')[1]) % 60
                             )


def get_closest_arrival_time(arrival_times_string, date_from):
    arrival_times = list(reversed((arrival_times_string.split(','))))
    closest_date = to_datetime(arrival_times[0], date_from)
    for arrival_time in arrival_times:
        arrival_time = to_datetime(arrival_time, date_from)
        if date_from >= arrival_time:
            return arrival_time
        closest_date = arrival_time
    return closest_date


def get_bus_scheduled_arrival_time(bus_id, bust_stop_id, date_from, bus_schedules=get_bus_schedules()):
    bus_schedule = bus_schedules[str(bus_id)]
    target_weekday = date_from.weekday()
    bus_stop_schedules = get_bus_stops_schedule(target_weekday, bus_schedule['forward']) + \
                         get_bus_stops_schedule(target_weekday, bus_schedule['backward'])
    arrival_times = get_bus_stop_arrival_times(bus_stop_schedules, bust_stop_id)
    return get_closest_arrival_time(arrival_times, date_from)
