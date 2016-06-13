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
        self.edit(metro)
        self.edges = dict()


    def __lt__(self, other):
        """Compare function of Vertex object. 

        """
        return self.code < other.code


    def add_edge(self, edge, destination):
        """Store an edge to the edge dictionart of the current Vertex object.

        Args:
            edge: Edge to be added.
            destination: Vertex that is at the destination side of the edge.
        """
        self.edges[destination] = edge


    def remove_edge(self, destination):
        """Remove an edge from the edge dictionart of the current Vertex object.

        Args:
            destination: Vertex that is at the destination side of the edge.
        """
        if destination in self.edges:
            del self.edges[destination]


    def edit(self, metro):
        """Edit the information of the Vertex object.
        
        """
        self.name = metro['name']
        self.population = metro['population']
        self.country = metro['country']
        self.region = metro['region']
        self.code = metro['code']
        self.continent = metro['continent']
        self.timezone = metro['timezone']
        self.coordinates = str(metro['coordinates'])


