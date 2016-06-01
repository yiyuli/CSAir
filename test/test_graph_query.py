import unittest
import json
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 

from graph.graph import Graph

class TestGraphQuery(unittest.TestCase):
	""" Tests for graph queries.

	Tests for graph queries.
	Tests include testsing longest edge, shortest edge, average edge distance, biggest vertex,
	smallest vertex, average vertex size, continents info, hub cities, and map url.

	"""
	def setUp(self):
		self.graph = Graph()
		self.graph.load("../json/test_data.json")


	def test_longest_edge(self):
		longest_edge = self.graph.calculate_longest_edge()
		self.assertEqual(longest_edge.departure.code, "MEX")
		self.assertEqual(longest_edge.destination.code, "LIM")
		self.assertEqual(longest_edge.distance, 24530)


	def test_shortest_edge(self):
		shortest_edge = self.graph.calculate_shortest_edge()
		self.assertEqual(shortest_edge.departure.code, "SCL")
		self.assertEqual(shortest_edge.destination.code, "LIM")
		self.assertEqual(shortest_edge.distance, 2453)


	def test_average_distance(self):
		average_distance = self. graph.calculate_average_distance()
		self.assertEqual(average_distance, 17171)


	def test_biggest_vertex(self):
		biggest_vertex =self.graph.calculate_biggest_vertex()
		self.assertEqual(biggest_vertex.code, "MEX")


	def test_smallest_vertex(self):
		smallest_vertex =self.graph.calculate_smallest_vertex()
		self.assertEqual(smallest_vertex.code, "SCL")


	def test_average_size(self):
		average_size = self. graph.calculate_average_vertex_size()
		self.assertEqual(int(average_size), 12816666)


	def test_continents_info(self):
		continents_dict = self.graph.calculate_continents_info()
		self.assertTrue("South America" in continents_dict.keys())
		self.assertTrue("North America" in continents_dict.keys())
		cities = []
		for value in continents_dict.values():
			for city in value:
				cities.append(city.code)
		self.assertTrue("MEX" in cities)
		self.assertTrue("SCL" in cities)
		self.assertTrue("LIM" in cities)


	def test_hub_cities(self):
		hub_cities = self.graph.calculate_hub_cities()
		hub_cities = [hub_cities[0].code, hub_cities[1].code, hub_cities[2].code]
		self.assertTrue("MEX" in hub_cities)
		self.assertTrue("SCL" in hub_cities)
		self.assertTrue("MEX" in hub_cities)


	def test_map_url(self):
		url = self.graph.generate_map_url()
		self.assertEqual(url, 'http://www.gcmap.com/mapui?P=SCL-LIM, MEX-LIM, LIM-MEX, ')


if __name__ == '__main__':
	unittest.main()

