import json
import sys

from vertex import Vertex
from edge import Edge

class Graph(object):
    
    def __init__(self):
        self.vertices = dict()
        self.edges = dict()
        self.numOfVertices = 0
        self.numOfEdges = 0

    def load(self, addr):
        data = self.loadJSON(addr)
        self.loadMetros(data)
        self.loadRoutes(data)

    @staticmethod
    def loadJSON(addr):
        with open(addr, 'r') as file:
            data = file.read()
            data = json.loads(data)
    
        return data

    def loadMetros(self, data):
        for city in data['metros']:
            self.numOfVertices += 1
            self.vertices[city['code']] = Vertex(city)  

    def loadRoutes(self, data):
        for route in data['routes']:
            self.numOfEdges += 1
            self.edges[self.numOfEdges] = self.buildEdge(self.vertices, route)

    @staticmethod
    def buildEdge(vertices, route):
        departure = vertices[route['ports'][0]]
        destination = vertices[route['ports'][1]]
        distance  = route['distance']
        edge = Edge(departure, destination, distance)
        departure.addEdges(edge, destination)

        return edge

    def calculateLongestFlight(self):
        longestFlight = None
        largestDistance = 0
        for flight in self.edges.values():
            if flight.distance > largestDistance:
                largestDistance = flight.distance
                longestFlight = flight

        return longestFlight

    def calculateShortestFlight(self):
        shortestFlight = None
        smallestDistance = sys.maxsize
        for flight in self.edges.values():
            if flight.distance < smallestDistance:
                smallestDistance = flight.distance
                shortestFlight = flight

        return shortestFlight

    def calculateAverageDistance(self):
        averageDistance = 0
        for flight in self.edges.values():
            averageDistance += flight.distance

        return averageDistance / self.numOfEdges

    def calculateBiggestCity(self):
        biggestCity = None
        largestPop = 0
        for city in self.vertices.values():
            if city.population > largestPop:
                largestPop = city.population
                biggestCity = city

        return biggestCity

    def calculateSmallestCity(self):
        smallestCity = None
        smallestPop = sys.maxsize
        for city in self.vertices.values():
            if city.population < smallestPop:
                smallestPop = city.population
                smallestCity = city

        return city

    def calculateAverageCitySize(self):
        averageCitySize = 0
        for city in self.vertices.values():
            averageCitySize += city.population

        return averageCitySize / self.numOfVertices

    def calculateContinentsInfo(self):
        continentsDict = dict()
        for city in self.vertices.values():
            if not city.continent in continentsDict:
                continentsDict[city.continent] = []
            continentsDict[city.continent].append(city)

        return continentsDict

    def calculateHubCities(self):
        hubCities = []
        max_connections = 0
        for city in self.vertices.values():
            if len(city.edges) > max_connections:
                hubCities = [city]
            elif len(city.edges) == max_connections:
                hubCities.append(city)

        return hubCities

    def generateMapUrl(self):
        url = 'http://www.gcmap.com/mapui?P='
        for route in self.edges.values():
            url += route.departure.code + '-' + route.destination.code + ', '

        return url


