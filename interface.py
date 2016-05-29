import webbrowser

from graph import Graph


def main():
    """Main loop of the text-based user interface.

    Main loop of the text-based user interface.
    User enters the corresponding number of the query and exits by entering 11.
    If users enters non-integer query or undefined query, pop error message.

    """
    graph = loadGraph("json/map_data.json")

    while (True):
        printMenu()
        query = input()
        if not is_int(query):
            printNotIntError()
            back = input('\nPress Enter to return to menu\n')
            continue
        query = int(query)
        print('\n')

        if query == 0:
            printCityList(graph)
        elif query == 1:
            code = input('Enter City Code\n')
            print('\n')
            printCityInfo(graph, code.upper())
        elif query == 2:
            printLongestFlight(graph)
        elif query == 3:
            printShortestFlight(graph)
        elif query == 4:
            printAverageDistance(graph)
        elif query == 5:
            printBiggestCity(graph)
        elif query == 6:
            printSmallestCity(graph)
        elif query == 7:
            printAverageCitySize(graph)
        elif query == 8:
            printContinentsAndCities(graph)
        elif query == 9:
            printHubCities(graph)
        elif query == 10:
            viewMap(graph)
        elif query == 11:
            print('Good bye')
            break;
        else:
            printQueryNumberError()

        back = input('\nPress Enter to return to menu\n')


def loadGraph(addr):
    """Initialize a Graph object, and load graph info including vertices and edges into the Graph object from the specified file path.

    Args:
        addr: Specified file path containing a JSON string.

    Returns:
        A graph object with info loaded from specified file path.
    """
    graph = Graph()
    graph.load(addr)
    return graph


def printMenu():
    """Print Menu of the user interface.

	"""
    print(
        'Welcome to CSAir Query Interface\nEnter the corresponding query number \n0. list of all cities \n1. city info \n2. longest flight \n3. shortest flight \n4. average distance \n5. biggest city (by pop) \n6. smallest city (by pop) \n7. average size (by pop) \n8. continents and cities \n9. hub cities \n10. visualized map\n11. exit')


def printCityList(graph):
    """Print a list of all cities that CSAir flies to.

    Args:
        graph: Graph object that stores map info.
    """
    print('City List:')
    for city in graph.vertices.values():
        print(city.name + ' (' + city.code + ')')


def printCityInfo(graph, code):
    """Print specific information about a specific city.

    Args:
        graph: Graph object that stores map info.
        code: City code.
    """
    if not code in graph.vertices:
        print('Input code does not belong to any CSAir served Airport')
        return
    city = graph.vertices[code]
    printCityInfoHelper(city)
    print('Cities reached by single non-stop: ')
    for neighbor in city.edges.values():
        print('		', neighbor.destination.name, '(' + neighbor.destination.code + ')', 'distance: ',
              neighbor.distance)


def printCityInfoHelper(city):
    """Print info of a specific city given its corresonding Vertex object.

    Args:
        city: Vertex object corresponding to the city.
    """
    print(city.name)
    print('code: ', city.code)
    print('population: ', city.population)
    print('country: ', city.country)
    print('region: ', city.region)
    print('continent: ', city.continent)
    print('timezone: ', city.timezone)
    print('coordinates: ', str(city.coordinates))


def printLongestFlight(graph):
    """Print info of the longest flight.

    Args:
        graph: Graph object that stores map info.
    """
    longestFlight = graph.calculateLongestEdge()
    print('Longest Flight:')
    print(longestFlight.departure.code, '->', longestFlight.destination.code, ' distance: ', longestFlight.distance)


def printShortestFlight(graph):
    """Print info of the shortest flight.

    Args:
        graph: Graph object that stores map info.
    """
    shortestFlight = graph.calculateShortestEdge()
    print('Shortest Flight:')
    print(shortestFlight.departure.code, '->', shortestFlight.destination.code, ' distance: ', shortestFlight.distance)


def printAverageDistance(graph):
    """Print average distance of all flights in the route network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Average Distance: ', graph.calculateAverageDistance())


def printBiggestCity(graph):
    """Print info of the biggest city.

    Args:
        graph: Graph object that stores map info.
    """
    biggestCity = graph.calculateBiggestVertex()
    print('Biggest City:')
    printCityInfoHelper(biggestCity)


def printSmallestCity(graph):
    """Print info of the smallest city.

    Args:
        graph: Graph object that stores map info.
    """
    smallestCity = graph.calculateSmallestVertex()
    print('Smallest City:')
    printCityInfoHelper(smallestCity)


def printAverageCitySize(graph):
    """Print the average size of all cities in the network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Average city size: ', graph.calculateAverageCitySize())


def printContinentsAndCities(graph):
    """Print a list of the continents and which cities in them in the route network.

    Args:
        graph: Graph object that stores map info.
    """
    continentsDict = graph.calculateContinentsInfo()
    for key, value in continentsDict.items():
        print('%s: ' % key)
        for city in value:
            print('		', city.name + ' (' + city.code + ')')


def printHubCities(graph):
    """Print hub cities (with the most direct connections) in the network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Hub Cities: ')
    hubCities = graph.calculateHubCities()
    for city in hubCities:
        print(city.name + ' (' + city.code + ')')


def viewMap(graph):
    """Open a window of Safari and direct to the web page that displays the whole route map.

    Args:
        graph: Graph object that stores map info.
    """
    url = graph.generateMapUrl()
    safari_path = 'open -a /Applications/Safari.app %s'
    webbrowser.get(safari_path).open(url)


def printNotIntError():
    """Print error message if a query is not an int.

    """
    print("\nPlease enter an integer\n")


def is_int(query):
    """Check input query is an integer

    Args:
        query: Input query

    Returns:
        True if query is an integer. False if not.
    """
    try:
        num = int(query)
    except ValueError:
        return False
    return True


def printQueryNumberError():
    """Print error message if a query number is not defined.

    """
    print('Query number not defined!')


if __name__ == '__main__':
    main()
