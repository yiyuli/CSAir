import json

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
        for metro in data['metros']:
            self.vertices[metro['code']] = Vertex(metro)  
            self.numOfVertices += 1

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

g = Graph()
g.load("json/map_data.json")

