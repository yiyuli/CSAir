import json
import sys

from vertex import Vertex
from edge import Edge

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
        data = self.loadJSON(addr)
        self.loadMetros(data)
        self.loadRoutes(data)


    @staticmethod
    def loadJSON(addr):
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


    def loadMetros(self, data):
        """Load city info from JSON object.

        Args:
            data: JSON object.
        """
        for city in data['metros']:
            self.numOfVertices += 1
            self.vertices[city['code']] = Vertex(city)  


    def loadRoutes(self, data):
        for route in data['routes']:
            self.numOfEdges += 1
            self.edges[self.numOfEdges] = self.buildEdge(self.vertices, route)


    @staticmethod
    def buildEdge(vertices, route):
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
        departure.addEdges(edge, destination)

        return edge


    def calculateLongestEdge(self):
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


    def calculateShortestEdge(self):
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


    def calculateAverageDistance(self):
        """Calculate the average edge distance.

        Returns:
            Average edge distance.
        """
        averageDistance = 0
        for flight in self.edges.values():
            averageDistance += flight.distance

        return averageDistance / self.numOfEdges


    def calculateBiggestVertex(self):
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


    def calculateSmallestVertex(self):
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


    def calculateAverageCitySize(self):
        """Calculate average vertex size.

        Returns:
            Average vertex size.
        """
        averageCitySize = 0
        for city in self.vertices.values():
            averageCitySize += city.population

        return averageCitySize / self.numOfVertices


    def calculateContinentsInfo(self):
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


    def calculateHubCities(self):
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


    def generateMapUrl(self):
        """Get url that contains the graph info to generate map in www.gcmap.com.

        Returns:
            An url that is used to generate map.
        """
        url = 'http://www.gcmap.com/mapui?P='
        for route in self.edges.values():
            url += route.departure.code + '-' + route.destination.code + ', '

        return url


