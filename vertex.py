class Vertex(object):
    """Vertex object.

    Vertex object that stores name, population, country, region, code, continent, timezone, coordinates info and edges starting from it.
    It also includes a function that stores an edge which starts from it.

    """
    def __init__(self, metro):
        """Constructor of Vertex object.

        Args:
            metro: JSON object that stores Vertex info.
        """
        self.name = metro['name']
        self.population = metro['population']
        self.country = metro['country']
        self.region = metro['region']
        self.code = metro['code']
        self.continent = metro['continent']
        self.timezone = metro['timezone']
        self.coordinates = metro['coordinates']
        self.edges = dict()


    def addEdges(self, edge, destination):
        """Store an edge to the edge dictionart of the current Vertex object.

        Args:
            edge: Edge to be added.
            destination: Vertex that is at the destination side of the edge
        """
        self.edges[destination] = edge
