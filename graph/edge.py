class Edge(object):
    """Edge class.

    Directed edge object that stores departure vertex, destination vertex, and distance.

    """
    def __init__(self, departure, destination, distance):
        """Constructor of edge object

        Args:
            departure: Departure vertex.
            destination: Destination vertex.
            distance: Distance.
        """
        self.departure = departure
        self.destination = destination
        self.distance = distance

