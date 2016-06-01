import json
import sys
from .vertex import Vertex
from .edge import Edge

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
        self.num_vertices = 0
        self.num_edges = 0


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
        """Load city info from JSON object.

        Args:
            data: JSON object.
        """
        for city in data['metros']:
            self.num_vertices += 1
            self.vertices[city['code']] = Vertex(city)  


    def load_edges(self, data):
        for route in data['routes']:
            self.num_edges += 1
            self.edges[self.num_edges] = self.build_edge(self.vertices, route)


    @staticmethod
    def build_edge(vertices, route):
        """Build edge according to route information.

        Args:
            vertices: Vertex dictionary of the graph.
            route: Route info to build a edge.

        Returns:
            Added edge.
        """
        departure = vertices[route['ports'][0]]
        destination = vertices[route['ports'][1]]
        distance  = route['distance']
        edge = Edge(departure, destination, distance)
        departure.add_edge(edge, destination)

        return edge


    def calculate_longest_edge(self):
        """Calculate the longest edge.

        Returns:
            Edge with largest distance.
        """
        longest_flight = None
        largest_distance = 0
        for flight in self.edges.values():
            if flight.distance > largest_distance:
                largest_distance = flight.distance
                longest_flight = flight

        return longest_flight


    def calculate_shortest_edge(self):
        """Calculate the shortest edge.

        Returns:
            Edge with smallest distance.
        """
        shortest_flight = None
        smallest_distance = sys.maxsize
        for flight in self.edges.values():
            if flight.distance < smallest_distance:
                smallest_distance = flight.distance
                shortest_flight = flight

        return shortest_flight


    def calculate_average_distance(self):
        """Calculate the average edge distance.

        Returns:
            Average edge distance.
        """
        average_distance = 0
        for flight in self.edges.values():
            average_distance += flight.distance

        return average_distance / self.num_edges


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

        return average_city_size / self.num_vertices


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


