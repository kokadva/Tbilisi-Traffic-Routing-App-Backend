from routing.busroutegraph import get_segment_nearby_bus_stops, get_bus_routes_graph
from routing.graphnode import StartNode, EndNode
from routing.priorityqueue import PriorityQueue
from routing.utils.geodata_utils import *


def heuristic(a, b):
    return math.sqrt(math.pow(a.segment_x - b.segment_x, 2) + math.pow(a.segment_y - b.segment_y, 2)) * 7 * 36 / 5


def weight(current, neighbour):
    if current.bus_num != neighbour.bus_num:
        return 5
    return 1


def found_goal(current, goal):
    if not current.is_start_node():
        cur_x = current.segment_x
        cur_y = current.segment_y
        goal_x = goal.segment_x
        goal_y = goal.segment_y
        return abs(goal_x - cur_x) <= 2 and abs(goal_y - cur_y) <= 2
    return False


def a_star_search(start, goal):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()

        if found_goal(current, goal):
            came_from[goal] = current
            cost_so_far[goal] = cost_so_far[current]
            break

        for neighbour in current.get_neighbours():
            new_cost = cost_so_far[current] + current.cost(neighbour)
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + heuristic(goal, neighbour) * weight(current, neighbour)
                frontier.put(neighbour, priority)
                came_from[neighbour] = current

    return came_from, cost_so_far


def to_route(came_from, start_node, end_node):
    cur = end_node
    route = []
    while cur != start_node:
        route.append(cur)
        cur = came_from[cur]
    return list(reversed(route[1:]))


def calculate_route(lon_a, lat_a, lon_b, lat_b, bus_routes_graph=get_bus_routes_graph()):
    x_1, y_1 = to_segment(lon_a, lat_a, get_tbilisi_rectangle_coordinates())
    x_2, y_2 = to_segment(lon_b, lat_b, get_tbilisi_rectangle_coordinates())
    nearby_bus_stops = get_segment_nearby_bus_stops((x_1, y_1))
    start_node = StartNode(lon_a, lat_a, x_1, y_1, nearby_bus_stops, bus_routes_graph)
    end_node = EndNode(lon_b, lat_b, x_2, y_2, bus_routes_graph)
    came_from, cost_so_far = a_star_search(start_node, end_node)
    route = to_route(came_from, start_node, end_node)
    return route, cost_so_far[end_node]
