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
        self.numOfVertices = 0
        self.numOfEdges = 0


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
            self.numOfVertices += 1
            self.vertices[city['code']] = Vertex(city)  


    def load_edges(self, data):
        for route in data['routes']:
            self.numOfEdges += 1
            self.edges[self.numOfEdges] = self.build_edge(self.vertices, route)


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
        longestFlight = None
        largestDistance = 0
        for flight in self.edges.values():
            if flight.distance > largestDistance:
                largestDistance = flight.distance
                longestFlight = flight

        return longestFlight


    def calculate_shortest_edge(self):
        """Calculate the shortest edge.

        Returns:
            Edge with smallest distance.
        """
        shortestFlight = None
        smallestDistance = sys.maxsize
        for flight in self.edges.values():
            if flight.distance < smallestDistance:
                smallestDistance = flight.distance
                shortestFlight = flight

        return shortestFlight


    def calculate_average_distance(self):
        """Calculate the average edge distance.

        Returns:
            Average edge distance.
        """
        averageDistance = 0
        for flight in self.edges.values():
            averageDistance += flight.distance

        return averageDistance / self.numOfEdges


    def calculate_biggest_vertex(self):
        """Calculate the biggest vertex (by population).

        Returns:
            Vertex with most population.
        """
        biggestCity = None
        largestPop = 0
        for city in self.vertices.values():
            if city.population > largestPop:
                largestPop = city.population
                biggestCity = city

        return biggestCity


    def calculate_smallest_vertex(self):
        """Calculate the smallest vertex (by population).

        Returns:
            Vertex with least population.
        """
        smallestCity = None
        smallestPop = sys.maxsize
        for city in self.vertices.values():
            if city.population < smallestPop:
                smallestPop = city.population
                smallestCity = city

        return smallestCity


    def calculate_average_city_size(self):
        """Calculate average vertex size.

        Returns:
            Average vertex size.
        """
        averageCitySize = 0
        for city in self.vertices.values():
            averageCitySize += city.population

        return averageCitySize / self.numOfVertices


    def calculate_continents_info(self):
        """Calculate continent info and its corresponding cities info.

        Returns:
            A dict with keys are continent info and values are cities info in the corresponding continent.
        """
        continentsDict = dict()
        for city in self.vertices.values():
            if not city.continent in continentsDict:
                continentsDict[city.continent] = []
            continentsDict[city.continent].append(city)

        return continentsDict


    def calculate_hub_cities(self):
        """Calculate hub cities (most direct connections) in the map.

        Returns:
            An array of cities with most direct connections.
        """
        hubCities = []
        max_connections = 0
        for city in self.vertices.values():
            if len(city.edges) > max_connections:
                max_connections = len(city.edges)
                hubCities = [city]
            elif len(city.edges) == max_connections:
                hubCities.append(city)

        return hubCities


    def generate_map_url(self):
        """Get url that contains the graph info to generate map in www.gcmap.com.

        Returns:
            An url that is used to generate map.
        """
        url = 'http://www.gcmap.com/mapui?P='
        for route in self.edges.values():
            url += route.departure.code + '-' + route.destination.code + ', '

        return url


