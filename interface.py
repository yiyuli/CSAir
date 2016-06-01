import webbrowser
from graph.graph import Graph

def main():
    """Main loop of the text-based user interface.

    Main loop of the text-based user interface.
    User enters the corresponding number of the query and exits by entering 11.
    If users enters non-integer query or undefined query, pop error message.

    """
    graph = load_graph("json/test_data.json")

    while (True):
        print_menu()
        query = input()
        if not is_int(query):
            print_not_int_error()
            back = input('\nPress Enter to return to menu\n')
            continue

        query = int(query)
        print('\n')

        if query == 0:
            print_city_list(graph)
        elif query == 1:
            code = input('Enter City Code\n')
            print('\n')
            print_city_info(graph, code.upper())
        elif query == 2:
            print_longest_flight(graph)
        elif query == 3:
            print_shortest_flight(graph)
        elif query == 4:
            print_average_distance(graph)
        elif query == 5:
            print_biggest_city(graph)
        elif query == 6:
            print_smallest_city(graph)
        elif query == 7:
            print_average_city_cize(graph)
        elif query == 8:
            print_continents_and_cities(graph)
        elif query == 9:
            print_hub_cities(graph)
        elif query == 10:
            view_map(graph)
        elif query == 11:
            print('Good bye')
            break;
        else:
            print_query_number_error()

        back = input('\nPress Enter to return to menu\n')


def load_graph(addr):
    """Initialize a Graph object, and load graph info including vertices and edges into the Graph object from the specified file path.

    Args:
        addr: Specified file path containing a JSON string.

    Returns:
        A graph object with info loaded from specified file path.
    """
    graph = Graph()
    graph.load(addr)
    return graph


def print_menu():
    """Print Menu of the user interface.

	"""
    print(
        'Welcome to CSAir Query Interface\nEnter the corresponding query number \n0. list of all cities \n1. city info \n2. longest flight \n3. shortest flight \n4. average distance \n5. biggest city (by pop) \n6. smallest city (by pop) \n7. average size (by pop) \n8. continents and cities \n9. hub cities \n10. visualized map\n11. exit')


def print_city_list(graph):
    """Print a list of all cities that CSAir flies to.

    Args:
        graph: Graph object that stores map info.
    """
    print('City List:')
    for city in graph.vertices.values():
        print(city.name + ' (' + city.code + ')')


def print_city_info(graph, code):
    """Print specific information about a specific city.

    Args:
        graph: Graph object that stores map info.
        code: City code.
    """
    if not code in graph.vertices:
        print('Input code does not belong to any CSAir served Airport')
        return
    city = graph.vertices[code]
    print_city_Info_helper(city)
    print('Cities reached by single non-stop: ')
    for neighbor in city.edges.values():
        print('		', neighbor.destination.name, '(' + neighbor.destination.code + ')', 'distance: ',
              neighbor.distance)


def print_city_Info_helper(city):
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


def print_longest_flight(graph):
    """Print info of the longest flight.

    Args:
        graph: Graph object that stores map info.
    """
    longest_flight = graph.calculate_longest_edge()
    print('Longest Flight:')
    print(longest_flight.departure.code, '->', longest_flight.destination.code, ' distance: ', longest_flight.distance)


def print_shortest_flight(graph):
    """Print info of the shortest flight.

    Args:
        graph: Graph object that stores map info.
    """
    shortest_flight = graph.calculate_shortest_edge()
    print('Shortest Flight:')
    print(shortest_flight.departure.code, '->', shortest_flight.destination.code, ' distance: ', shortest_flight.distance)


def print_average_distance(graph):
    """Print average distance of all flights in the route network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Average Distance: ', graph.calculate_average_distance())


def print_biggest_city(graph):
    """Print info of the biggest city.

    Args:
        graph: Graph object that stores map info.
    """
    biggest_city = graph.calculate_biggest_vertex()
    print('Biggest City:')
    print_city_Info_helper(biggest_city)


def print_smallest_city(graph):
    """Print info of the smallest city.

    Args:
        graph: Graph object that stores map info.
    """
    smallest_city = graph.calculate_smallest_vertex()
    print('Smallest City:')
    print_city_Info_helper(smallest_city)


def print_average_city_cize(graph):
    """Print the average size of all cities in the network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Average city size: ', graph.calculate_average_vertex_size())


def print_continents_and_cities(graph):
    """Print a list of the continents and which cities in them in the route network.

    Args:
        graph: Graph object that stores map info.
    """
    continents_dict = graph.calculate_continents_info()
    for key, value in continents_dict.items():
        print('%s: ' % key)
        for city in value:
            print('		', city.name + ' (' + city.code + ')')


def print_hub_cities(graph):
    """Print hub cities (with the most direct connections) in the network.

    Args:
        graph: Graph object that stores map info.
    """
    print('Hub Cities: ')
    hub_cities = graph.calculate_hub_cities()
    for city in hub_cities:
        print(city.name + ' (' + city.code + ')')


def view_map(graph):
    """Open a window of Safari and direct to the web page that displays the whole route map.

    Args:
        graph: Graph object that stores map info.
    """
    url = graph.generate_map_url()
    safari_path = 'open -a /Applications/Safari.app %s'
    webbrowser.get(safari_path).open(url)


def print_not_int_error():
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


def print_query_number_error():
    """Print error message if a query number is not defined.

    """
    print('Query number not defined!')


if __name__ == '__main__':
    main()
