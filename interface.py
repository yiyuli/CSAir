import webbrowser

from graph import Graph

def main():
	g = loadGraph("json/map_data.json")

	while (True):
		printMenu()
		query = int(input())
		print('\n')

		if query == 0:
			printCityList(g)
		elif query == 1:
			code = input('Enter City Code\n')
			print('\n')
			printCityInfo(g, code)
		elif query == 2:
			printLongestFlight(g)
		elif query == 3:
			printShortestFlight(g)
		elif query == 4:
			printAverageDistance(g)
		elif query == 5:
			printBiggestCity(g)
		elif query == 6:
			printSmallestCity(g)
		elif query == 7:
			printAverageCitySize(g)
		elif query == 8:
			printContinentsAndCities(g)
		elif query == 9:
			printHubCities(g)
		elif query == 10:
			viewMap(g)
		elif query == 11:
			print('Good bye')
			break;
		else:
			printError()

		back = input('\nPress Enter to return to menu\n')

def loadGraph(addr):
	g = Graph()
	g.load(addr)

	return g

def printMenu():
	print('Welcome to CSAir Query Interface\nEnter the corresponding query number \n0. list of all cities \n1. city info \n2. longest flight \n3. shortest flight \n4. average distance \n5. biggest city (by pop) \n6. smallest city (by pop) \n7. average size (by pop) \n8. continents and cities \n9. hub cities \n10. visualized map\n11. exit')

def printCityList(g):
	print('City List:')
	for city in g.vertices.values():
		print(city.name + ' (' + city.code + ')')

def printCityInfo(g, code):
	if not code in g.vertices:
		print('Input code does not belong to any CSAir served Airport')
		return
	city = g.vertices[code]
	printCityInfoHelper(city)
	print('Cities reached by single non-stop: ')
	for neighbor in city.edges.values():
		print('		', neighbor.destination.name, '(' + neighbor.destination.code + ')', 'distance: ', neighbor.distance)


def printCityInfoHelper(city):
	print(city.name)
	print('code: ', city.code)
	print('population: ', city.population)
	print('country: ', city.country)
	print('region: ', city.region)
	print('continent: ', city.continent)
	print('timezone: ', city.timezone)
	print('coordinates: ', str(city.coordinates))

def printLongestFlight(g):
	longestFlight = g.calculateLongestFlight()
	print('Longest Flight:')
	print(longestFlight.departure.code, '->', longestFlight.destination.code, ' distance: ', longestFlight.distance)

def printShortestFlight(g):
	shortestFlight = g.calculateShortestFlight()
	print('Shortest Flight:')
	print(shortestFlight.departure.code, '->', shortestFlight.destination.code, ' distance: ', shortestFlight.distance)

def printAverageDistance(g):
	print('Average Distance: ', g.calculateAverageDistance())

def printBiggestCity(g):
	biggestCity = g.calculateBiggestCity()
	print('Biggest City:')
	printCityInfoHelper(biggestCity)

def printSmallestCity(g):
	smallestCity = g.calculateSmallestCity()
	print('Smallest City:')
	printCityInfoHelper(smallestCity)

def printAverageCitySize(g):
	print('Average city size: ', g.calculateAverageCitySize())

def printContinentsAndCities(g):
	continentsDict = g.calculateContinentsInfo()
	for key, value in continentsDict.items():
		print('%s: ' % key)
		for city in value:
			print('		', city.name + ' (' + city.code + ')')

def printHubCities(g):
	print('Hub Cities: ')
	hubCities = g.calculateHubCities()
	for city in hubCities:
		print(city.name + ' (' + city.code + ')')

def viewMap(g):
	url = g.generateMapUrl()
	safari_path = 'open -a /Applications/Safari.app %s'
	webbrowser.get(safari_path).open(url)

def printError():
	print('Query number not defined!')

if __name__ == '__main__':
	main()