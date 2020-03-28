import datetime

from ttc.bus_schedule_api import get_bus_scheduled_arrival_time


class Node(object):

    def __init__(self, lon, lat, segment_x, segment_y, bus_stop_name, bus_stop_id, bus_num, neighbors, graph):
        self.lon = lon
        self.lat = lat
        self.segment_x = segment_x
        self.segment_y = segment_y
        self.bus_stop_name = bus_stop_name
        self.bus_stop_id = bus_stop_id
        self.bus_num = bus_num
        self.neighbors = neighbors
        self.graph = graph
        self.id = self.get_id() + bus_num
        self.f = 0

    def cost(self, neighbor):
        cur_date = datetime.datetime.now()
        if self.bus_num != neighbor.bus_num:
            bus_arrival_time = get_bus_scheduled_arrival_time(neighbor.bus_num, neighbor.bus_stop_id,
                                                              cur_date)
            seconds = (bus_arrival_time - cur_date).seconds
            return seconds

        return (get_bus_scheduled_arrival_time(neighbor.bus_num, neighbor.bus_stop_id, cur_date) - cur_date).seconds

    def get_id(self):
        return self.bus_stop_id

    def get_neighbours(self):
        return set(map(lambda x: self.graph[x], self.neighbors))

    def __hash__(self):
        return hash(self.id)

    def __lt__(self, other):
        return self.f < other.f

    def is_start_node(self):
        return False

    def is_end_node(self):
        return False


class StartNode(Node):

    def __init__(self, lon, lat, segment_x, segment_y, neighbors, graph):
        super().__init__(lon, lat, segment_x, segment_y, "Start Node", 'StartStop', "StartStop", neighbors, graph)

    def is_start_node(self):
        return True


class EndNode(Node):

    def __init__(self, lon, lat, segment_x, segment_y, graph):
        super().__init__(lon, lat, segment_x, segment_y, "End Node", 'EndStop', "EndStop", [], graph)

    def is_end_node(self):
        return True
