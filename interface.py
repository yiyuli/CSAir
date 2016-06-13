import webbrowser
import json
from graph.graph import Graph

def main():
    """Main loop of the text-based user interface.

    Main loop of the text-based user interface.
    User enters the corresponding number of the query and exits by entering 19.
    If users enters non-integer query or undefined query, pop error message.

    """
    graph = load_graph("json/map_data.json", "json/cmi_hub.json")    # "json/map_data.json", "json/cmi_hub.json"    "json/save_data.json"

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
            city = input('Enter City Info (format: "code, name, country, countinent, timezone, coordinates (e.g. {"N" : 40, "W" : 88}), population, region")\n')
            print('\n')
            add_city(graph, city)
        elif query == 12:
            flight = input('Enter Flight Info (format: "departure_code, destination_code, distance")\n')
            print('\n')
            add_flight(graph, flight)
        elif query == 13:
            city = input('Enter City code (format: "city_code")\n')
            print('\n')
            remove_city(graph, city.upper())
        elif query == 14:
            flight = input('Enter Flight Info (format: "departure_code, destination_code")\n')
            print('\n')
            remove_flight(graph, flight)
        elif query == 15:
            city = input('Enter City Info (format: "code, name, country, countinent, timezone, coordinates (e.g. {"N" : 40, "W" : 88}), population, region")\n')
            print('\n')
            edit_city(graph, city)
        elif query == 16:
            save_network_to_disk(graph)
        elif query == 17:
            route = input('Enter Route Info (e.g. "LON, PAR, IST")\n')
            print('\n')
            print_route_info(graph, route)
        elif query == 18:
            cities = input('Enter Departure and Destination city (formate: "departure_code, destination_code")\n')
            print('\n')
            print_shortest_path(graph, cities)
        elif query == 19:
            print('Good bye')
            break;
        else:
            print_query_number_error()

        back = input('\nPress Enter to return to menu\n')


def load_graph(*file_addr):
    """Initialize a Graph object, and load graph info including vertices and edges into the Graph object from the specified file paths.

    Args:
        file_addr: Specified file paths containing a JSON string.

    Returns:
        A graph object with info loaded from specified file path.
    """
    graph = Graph()
    for addr in file_addr:
        graph.load(addr)
    return graph


def print_menu():
    """Print Menu of the user interface.

	"""
    print(
        'Welcome to CSAir Query Interface\nEnter the corresponding query number \n0. list of all cities \n1. city info \n2. longest flight \n3. shortest flight \n4. average distance \n5. biggest city (by pop) \n6. smallest city (by pop) \n7. average size (by pop) \n8. continents and cities \n9. hub cities \n10. visualized map\n11. add a city\n12. add a flight\n13. remove a city\n14. remove a flight\n15. edit a city\n16. save network\n17. get route info\n18. get shortest path\n19. exit')


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
    print('coordinates: ', city.coordinates)


def print_longest_flight(graph):
    """Print info of the longest flight.

    Args:
        graph: Graph object that stores map info.
    """
    longest_flight = graph.calculate_longest_edge()
    print('Longest Flight:')
    for flight in longest_flight:
        print(flight.departure.code, '->', flight.destination.code, ' distance: ', flight.distance)


def print_shortest_flight(graph):
    """Print info of the shortest flight.

    Args:
        graph: Graph object that stores map info.
    """
    shortest_flight = graph.calculate_shortest_edge()
    print('Shortest Flight:')
    for flight in shortest_flight:
        print(flight.departure.code, '->', flight.destination.code, ' distance: ', flight.distance)


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


def add_city(graph, city):
    """Add a city to the network.

    Args:
        graph: Graph object that stores map info.
        city: String containing input city info sperated by comma.
    """
    city = list(map(str.strip, city.split(",")))
    if len(city) != 9 or not is_int(city[4]) or not is_int(city[7]) or not is_int(city[8]) or int(city[7]) < 0:
        print("Wrong input!\n")
    else:
        vertex = create_city_json(city)
        if graph.add_vertex(vertex):
            print("success!\n")
        else:
            print("Failed!\n")


def add_flight(graph, flight):
    """Add a flight to the network.

    Args:
        graph: Graph object that stores map info.
        flight: String containing flight info sperated by comma.
    """
    flight = flight.replace(" ", "").split(",")
    if len(flight) != 3 or not is_int(flight[2]) or int(flight[2]) < 0:
        print("Wrong input!\n")
    else:
        if graph.add_edge(flight[0], flight[1], int(flight[2])):
            print("Success!\n")
        else:
            print("Failed!\n")


def remove_city(graph, city):
    """Remove a city to the network.

    Args:
        city: Code of city to be removed.
    """
    if graph.remove_vertex(city):
        print("Success!\n")
    else:
        print("Failed!\n")


def remove_flight(graph, flight):
    """Add a flight to the network.

    Args:
        graph: Graph object that stores map info.
        flight: String containing departure and destination code sperated by comma.
    """
    flight = flight.replace(" ", "").split(",")
    if len(flight) != 2:
        print("Wrong input!\n")
    else:
        if graph.remove_edge(flight[0], flight[1]):
            print("Success!\n")
        else:
            print("Failed!\n")


def edit_city(graph, city):
    """Edit a city to the network.

    Args:
        graph: Graph object that stores map info.
        city: String containing input city info seperated by comma.
    """
    city = list(map(str.strip, city.split(",")))
    if len(city) != 9 or not is_int(city[4]) or not is_int(city[7]) or not is_int(city[8]) or int(city[7]) < 0:
        print("Wrong input!\n")
    else:
        vertex = create_city_json(city)
        if graph.edit_vertex(vertex):
            print("Success!\n")
        else:
            print("Failed!\n")


def save_network_to_disk(graph):
    """Convert network graph to a json object and stores it into a file.

    Args:
        graph: Graph object that stores map info.
    """
    graph_json = graph.convert_to_json()
    with open("json/save_data.json", 'wt') as out:
        res = json.dump(graph_json, out, sort_keys=True, indent=4, separators=(',', ': '))


def print_route_info(graph, route):
    """Print route info given a route. If a route is invalid, print corresponding error message.

    Args:
        graph: Graph object that stores map info.
        route: String containing cities code in the route seperated by comma.
    """
    route = route.replace(" ", "").split(",")
    
    for city in route:
        if not city in graph.vertices:
            print("City Code Not Found!\n")

    if graph.is_valid_route(route):
        cost, time = graph.calculate_route_info(route)
        for i in range(len(route) - 1):
            print(route[i], end="->")
        print(route[-1])
        print("Cost:", cost , "Time: ", time)
    else:
        print("Invalid Route!\n")


def print_shortest_path(graph, cities):
    """Print shortest path given a list containing departure and destination city code. If route is invalid or no shortest path, print corresponding error message.

    Args:
        graph: Graph object that stores map info.
        cities: String containing departure and destination city code sperated by comma.
    """
    cities = cities.replace(" ", "").split(",")
    if len(cities) != 2:
        print("Wrong input!\n")
    elif not cities[0] in graph.vertices or not cities[1] in graph.vertices:
        print("City Code Not Found!\n")
    else:
        route = graph.calculate_shortest_path(cities)
        if route == None:
            print("No path between", cities[0], "and", cities[1])
        else:
            print("Shortest Path between %s and %s: " % (cities[0], cities[1]))
            for i in range(len(route) - 1):
                print(route[i], end="->")
            print(route[-1])


def print_not_int_error():
    """Print error message if a query is not an int.

    """
    print("\nPlease enter an integer\n")


def is_int(query):
    """Check input query is an integer.

    Args:
        query: Input query.

    Returns:
        True if query is an integer. False if not.
    """
    try:
        num = int(query)
    except ValueError:
        return False
    return True


def create_city_json(city):
    """Create json object given a string containing city info.

    Args:
        city: String containing input city info sperated by comma.

    Returns:
        A json object containing city info.
    """
    json = dict()
    json['code'] = city[0]
    json['name'] = city[1]
    json['country'] = city[2]
    json['continent'] = city[3]
    json['timezone'] = int(city[4])
    json['coordinates'] = city[5] + ", " + city[6]
    json['population'] = int(city[7])
    json['region'] = int(city[8])
    return json


def print_query_number_error():
    """Print error message if a query number is not defined.

    """
    print('Query number not defined!\n')


if __name__ == '__main__':
    main()
