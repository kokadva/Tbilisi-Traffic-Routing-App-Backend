from apscheduler.schedulers.background import BackgroundScheduler
from traffic.bus_arrival_time_scraper import scrape_bus_arrival_times


def init_bus_arrival_time_scraping():
    sched = BackgroundScheduler()
    sched.add_job(scrape_bus_arrival_times, 'interval', seconds=300)
    sched.start()
