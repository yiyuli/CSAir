import json
import sys
import math
from .vertex import Vertex
from .edge import Edge
from .priority_queue import PriorityQueue

class Graph(object):
    """Graph object.

    Graph object that includes vertices and edges info.
    It also includes several query functions to support special information retrieval.

    """
    def __init__(self):
        """Constructor of Graph object.

        """
        self.vertices = dict()
        self.edges = dict()


    def load(self, addr):
        """Load data to update Graph object from specified file containing JSON object.

        Args:
            addr: Loaded file address.
        """
        data = self.load_json(addr)
        self.load_vertices(data)
        self.load_edges(data)


    @staticmethod
    def load_json(addr):
        """Load JSON object from the specified address.

        Args:
            addr: Loaded file address.

        Returns:
            the JSON object.
        """
        with open(addr, 'r') as file:
            data = file.read()
            data = json.loads(data)
    
        return data


    def load_vertices(self, data):
        """Load graph vertices info from JSON object.

        Args:
            data: JSON object.
        """
        for city in data['metros']:
            self.vertices[city['code']] = Vertex(city)  


    def load_edges(self, data):
        """Load graph edges info from JSON object.

        Args:
            data: JSON object.
        """
        for route in data['routes']:
            self.edges[route['ports'][0] + "," + route['ports'][1]] = self.build_edge(route['ports'][0], route['ports'][1], route['distance'])
            self.edges[route['ports'][1] + "," + route['ports'][0]] = self.build_edge(route['ports'][1], route['ports'][0], route['distance'])


    def build_edge(self, departure, destination, distance):
        """Build edge according to edge information.

        Args:
            departure: Departure vertex code.
            destination: Destination vertex code.
            distance: Distance of the edge.

        Returns:
            Added edge.
        """
        departure = self.vertices[departure]
        destination = self.vertices[destination]
        edge = Edge(departure, destination, distance)
        departure.add_edge(edge, destination)

        return edge


    def remove_vertex(self, code):
        """Remove a vertex from the Graph object and its connected edges. Return true if succeed. If code does not exist, return False.

        Args:
            code: code of vertex to be removed.

        Returns:
            True if removal is ok. Otherwise False.
        """
        if not code in self.vertices:
            return False
        else:
            edges_to_be_removed = []
            for key, edge in self.edges.items():
                if edge.departure.code == code or edge.destination.code == code:
                    edges_to_be_removed.append(key)
                    if edge.destination.code == code:
                        edge.departure.remove_edge(edge.destination)
            for edge in edges_to_be_removed:
                del self.edges[edge]
            del self.vertices[code]
            return True


    def remove_edge(self, departure, destination):
        """Remove an edge from the Graph object. Return true if succeed. Return false if connected city is missed.

        Args:
            departure: Code of departure vertex.
            destination: Code of destination vertex.

        Returns:
            True if removal is ok. Otherwise False.
        """
        if departure in self.vertices and destination in self.vertices and departure + "," + destination in self.edges:
            self.vertices[departure].remove_edge(self.vertices[destination])
            del self.edges[departure + "," + destination]
            return True
        else:
            return False


    def add_vertex(self, vertex):
        """Add a vertex from the Graph object. If the code of the vertex is already existed, return False. Otherwise True.

        Args:
            vertex: JSON object holding vertex info.

        Returns:
            True if addition is ok. Otherwise Fasle.
        """
        if not vertex['code'] in self.vertices:
            vertex_to_be_added = Vertex(vertex)
            self.vertices[vertex_to_be_added.code] = vertex_to_be_added
            return True
        else:
            return False


    def add_edge(self, departure, destination, distance):
        """Add an edge from the Graph object. If connected city is missed, return false. Otherwise true.

        Args:
            departure: Code of departure vertex.
            destination: Code of destination vertex.
            distance: Distance of the vertex.

        Returns:
            True if addition is ok. Otherwise False.
        """
        if departure in self.vertices and destination in self.vertices:
            edge = Edge(self.vertices[departure], self.vertices[destination], distance)
            self.edges[departure + "," + destination] = edge
            self.vertices[departure].add_edge(edge, self.vertices[destination])
            return True
        else:
            return False



    def edit_vertex(self, vertex):
        """Edit a vertex info. Return true if succeed.

        Args:
            vertex: JSON object holding vertex info.

        Returns:
            True if edit is ok. Otherwise Fasle.
        """
        if vertex['code'] in self.vertices:
            self.vertices[vertex['code']].edit(vertex)
            return True
        else:
            return False


    def calculate_longest_edge(self):
        """Calculate the longest edges.

        Returns:
            Edge list with largest distance.
        """
        longest_flight = []
        largest_distance = 0
        for flight in self.edges.values():
            if flight.distance > largest_distance:
                largest_distance = flight.distance
                longest_flight = [flight]
            elif flight.distance == largest_distance:
                longest_flight.append(flight)

        return longest_flight


    def calculate_shortest_edge(self):
        """Calculate the shortest edges.

        Returns:
            Edge list with smallest distance.
        """
        shortest_flight = []
        smallest_distance = sys.maxsize
        for flight in self.edges.values():
            if flight.distance < smallest_distance:
                smallest_distance = flight.distance
                shortest_flight = [flight]
            elif flight.distance == smallest_distance:
                shortest_flight.append(flight)

        return shortest_flight


    def calculate_average_distance(self):
        """Calculate the average edge distance.

        Returns:
            Average edge distance.
        """
        average_distance = 0
        for flight in self.edges.values():
            average_distance += flight.distance

        return average_distance / len(self.edges)


    def calculate_biggest_vertex(self):
        """Calculate the biggest vertex (by population).

        Returns:
            Vertex with most population.
        """
        biggest_city = None
        largest_pop = 0
        for city in self.vertices.values():
            if city.population > largest_pop:
                largest_pop = city.population
                biggest_city = city

        return biggest_city


    def calculate_smallest_vertex(self):
        """Calculate the smallest vertex (by population).

        Returns:
            Vertex with least population.
        """
        smallest_city = None
        smallest_pop = sys.maxsize
        for city in self.vertices.values():
            if city.population < smallest_pop:
                smallest_pop = city.population
                smallest_city = city

        return smallest_city


    def calculate_average_vertex_size(self):
        """Calculate average vertex size.

        Returns:
            Average vertex size.
        """
        average_city_size = 0
        for city in self.vertices.values():
            average_city_size += city.population

        return average_city_size / len(self.vertices)


    def calculate_continents_info(self):
        """Calculate continent info and its corresponding cities info.

        Returns:
            A dict with keys are continent info and values are cities info in the corresponding continent.
        """
        continents_dict = dict()
        for city in self.vertices.values():
            if not city.continent in continents_dict:
                continents_dict[city.continent] = []
            continents_dict[city.continent].append(city)

        return continents_dict


    def calculate_hub_cities(self):
        """Calculate hub cities (most direct connections) in the map.

        Returns:
            An array of cities with most direct connections.
        """
        hub_cities = []
        max_connections = 0
        for city in self.vertices.values():
            if len(city.edges) > max_connections:
                max_connections = len(city.edges)
                hub_cities = [city]
            elif len(city.edges) == max_connections:
                hub_cities.append(city)

        return hub_cities


    def generate_map_url(self):
        """Get url that contains the graph info to generate map in www.gcmap.com.

        Returns:
            An url that is used to generate map.
        """
        url = 'http://www.gcmap.com/mapui?P='
        for route in self.edges.values():
            url += route.departure.code + '-' + route.destination.code + ', '

        return url


    def is_valid_route(self, route):
        """Check route is valid. For successive cities in the route, cities must exist and there are edges between them.

        Args:
            route: List of cities' code.

        Returns:
            True if route is valid. Otherwise False.
        """
        for i in range(len(route) - 1):
            if not self.vertices[route[i + 1]] in self.vertices[route[i]].edges:
                return False

        return True


    def calculate_route_info(self, route):
        """Calculate the cost and time of a given valid route.

        Args:
            route: List of cities' code.

        Returns:
            Cost and time of the route.
        """
        cost = 0
        time = 0
        for i in range(len(route) - 1):
            departure = self.vertices[route[i]]
            destination = self.vertices[route[i + 1]]
            distance = self.edges[departure.code + "," + destination.code].distance
            # calculate cost
            if 0.35 - 0.05 * i >= 0:
                cost += distance * (0.35 - 0.05 * i)
            # caculate flight time
            if distance < 400:
                a = 1406.25 # accleration
                time += math.sqrt(2 * distance / a)
            else:
                time += 400 / 375 + (distance - 400) / 750
            #calculate layover time
            if i != len(route) - 2:
                if 2 - (len(destination.edges) - 1) * 10 / 60 > 0:
                    time += 2 - (len(destination.edges) - 1) * 10 / 60

        return float("%.2f" % cost), float("%.2f" % time)


    def convert_to_json(self):
        """Convert Graph object to json object.

        Returns:
            A json object holding current Graph object's info.
        """
        graph_json = dict()
        graph_json['metros'] = []
        graph_json['routes'] = []

        for key in sorted(self.vertices):
            metro = dict()
            metro['code'] = self.vertices[key].code
            metro['name'] = self.vertices[key].name
            metro['country'] = self.vertices[key].country
            metro['continent'] = self.vertices[key].continent
            metro['timezone'] = self.vertices[key].timezone
            metro['coordinates'] = json.loads(self.vertices[key].coordinates.replace("\'", "\""))
            metro['population'] = self.vertices[key].population
            metro['region'] = self.vertices[key].region
            graph_json['metros'].append(metro)

        for key in sorted(self.edges):
            route = dict()
            route['ports'] = [self.edges[key].departure.code, self.edges[key].destination.code]
            route['distance'] = self.edges[key].distance
            graph_json['routes'].append(route)

        return graph_json


    def calculate_shortest_path(self, cities):
        """Calculate shortest path using dijkstra's algorithm given departure vertex and destination vertex.

        Args:
            cities: List holding code of departure vertex and destination vertex.

        Returns:
            List of code of shortest_path.
        """
        departure = self.vertices[cities[0]]
        destination = self.vertices[cities[1]]

        pq = PriorityQueue()
        pq[departure] = 0

        smallest_distance = dict()
        previous = dict()
        unvisited_vertices = set()
        for vertex in self.vertices.values():
            previous[vertex] = None
            unvisited_vertices.add(vertex)
            if vertex != departure:
                smallest_distance[vertex] = sys.maxsize
            else:
                smallest_distance[vertex] = 0
            pq[vertex] = smallest_distance[vertex]
        
        while pq:
            v = pq.pop_smallest()
            for neighbor in v.edges.keys():
                if neighbor in unvisited_vertices:
                    distance = self.edges[v.code + ',' + neighbor.code].distance
                    if distance + smallest_distance[v] < smallest_distance[neighbor]:
                        smallest_distance[neighbor] = distance + smallest_distance[v]
                        pq[neighbor] = smallest_distance[neighbor]
                        previous[neighbor] = v

            unvisited_vertices.remove(v)

        shortest_path = [destination.code]
        vertex = destination
        while vertex != departure:
            if previous[vertex] == None:
                shortest_path = None
                break
            else:
                shortest_path = [previous[vertex].code] + shortest_path
                vertex = previous[vertex]

        return shortest_path
