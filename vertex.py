class Vertex(object):
    
    def __init__(self, metro):
        self.name = metro['name']
        self.population = metro['population']
        self.country = metro['country']
        self.region = metro['region']
        self.code = metro['code']
        self.continent = metro['continent']
        self.timezone = metro['timezone']
        self.coordinate = metro['coordinates']
        self.edges = dict()

    def addEdges(self, edge, destination):
    	self.edges[destination] = edge
