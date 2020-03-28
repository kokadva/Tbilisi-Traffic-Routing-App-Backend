import os

from flask import Response
from flask_cors import cross_origin
from flask_app import app
from resources import db, cors
from services.routing_service import get_route
from services.traffic_service import get_bus_route_traffic
from settings import settings_object
from traffic.scheduler import init_bus_arrival_time_scraping


# Call if connected to fresh new DB
def init_database_scheme():
    with app.app_context():
        db.create_all()


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def init_resources():
    cors.init_app(app)
    db.init_app(app)


def init_config():
    app.config.from_object(settings_object)


def init_app():
    init_config()
    app.after_request(add_cors_headers)
    init_resources()
    init_bus_arrival_time_scraping()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@cross_origin()
@app.route('/', methods=['GET'])
def home():
    return "Tbilisi Traffic Routing App! (tbilisitrafficrouting@gmail.com)"


@cross_origin()
@app.route('/route/<float:lon_a>/<float:lat_a>/<float:lon_b>/<float:lat_b>', methods=['GET'])
def retrieve_route(lon_a, lat_a, lon_b, lat_b):
    try:
        route = str(get_route((lon_a, lat_a), (lon_b, lat_b)))
        response = Response(
            route,
            200,
            direct_passthrough=True,
        )
        return response
    except Exception as e:
        pass
    return "", 404


@cross_origin()
@app.route('/traffic/busroute/<string:bus_num>')
def retrieve_bus_route_traffic(bus_num):
    return str(get_bus_route_traffic(bus_num))


if __name__ == '__main__':
    init_app()
    init_database_scheme()
    app.run(port=app.config.get('PORT'), host=app.config.get('HOST'))
