import unittest
import json
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir) 

from graph.graph import Graph
from graph.vertex import Vertex
from graph.edge import Edge

city = json.loads('{"code" : "CMI","name" : "Champaign","country" : "US","continent" : "North America","timezone" : -6 ,"coordinates" : {"N" : 40, "W" : 88},"population" : 226000,"region" : 1}')

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
		longest_edge = sorted(self.graph.calculate_longest_edge(), key=lambda x: x.departure.code)
		self.assertEqual(longest_edge[0].departure.code, "LIM")
		self.assertEqual(longest_edge[1].departure.code, "MEX")
		self.assertEqual(longest_edge[0].distance, 24530)


	def test_shortest_edge(self):
		shortest_edge = sorted(self.graph.calculate_shortest_edge(), key=lambda x: x.departure.code)
		self.assertEqual(shortest_edge[1].departure.code, "SCL")
		self.assertEqual(shortest_edge[0].departure.code, "LIM")
		self.assertEqual(shortest_edge[0].distance, 2453)


	def test_average_distance(self):
		average_distance = self. graph.calculate_average_distance()
		self.assertEqual(int(average_distance), 10594)


	def test_biggest_vertex(self):
		biggest_vertex = self.graph.calculate_biggest_vertex()
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
		self.assertTrue("MEX-SCL" in url)
		self.assertTrue("LIM-MEX" in url)
		self.assertTrue("SCL-LIM" in url)


	def test_add_vertex(self):
		self.assertTrue(self.graph.add_vertex(city))
		self.assertTrue("CMI" in self.graph.vertices.keys())
		self.assertEqual(self.graph.vertices["CMI"].name, "Champaign")


	def test_add_edge(self):
		self.assertTrue(self.graph.add_vertex(city))
		self.assertFalse(self.graph.add_edge("CMI", "PAR", 30000))
		self.assertTrue(self.graph.add_edge("CMI", "MEX", 30000))
		edges = []
		for edge in self.graph.edges.values():
			edges.append(edge.departure.code + " -> " + edge.destination.code + ", " + str(edge.distance))
		edges.sort()
		self.assertEqual(edges, ['CMI -> MEX, 30000', 'LIM -> MEX, 24530', 'LIM -> SCL, 2453', 'MEX -> LIM, 24530', 'MEX -> SCL, 4800', 'SCL -> LIM, 2453', 'SCL -> MEX, 4800'])


	def test_remove_edge(self):
		self.assertFalse(self.graph.remove_edge("CMI", "PAR"))
		self.assertTrue(self.graph.add_vertex(city))
		self.assertTrue(self.graph.add_edge("CMI", "MEX", 30000))
		self.assertTrue(self.graph.remove_edge("CMI", "MEX"))
		edges = []
		for edge in self.graph.edges.values():
			edges.append(edge.departure.code + " -> " + edge.destination.code + ", " + str(edge.distance))
		edges.sort()
		self.assertEqual(edges, ['LIM -> MEX, 24530', 'LIM -> SCL, 2453', 'MEX -> LIM, 24530', 'MEX -> SCL, 4800', 'SCL -> LIM, 2453', 'SCL -> MEX, 4800'])


	def test_remove_vertex(self):
		self.assertFalse(self.graph.remove_vertex("PAR"))
		self.assertTrue(self.graph.add_vertex(city))
		self.assertTrue(self.graph.add_edge("CMI", "MEX", 30000))
		self.assertTrue(self.graph.remove_vertex("CMI"))
		self.assertFalse("CMI" in self.graph.vertices.keys())
		edges = []
		for edge in self.graph.edges.values():
			edges.append(edge.departure.code + " -> " + edge.destination.code + ", " + str(edge.distance))
		edges.sort()
		self.assertEqual(edges, ['LIM -> MEX, 24530', 'LIM -> SCL, 2453', 'MEX -> LIM, 24530', 'MEX -> SCL, 4800', 'SCL -> LIM, 2453', 'SCL -> MEX, 4800'])


	def test_save_to_disk(self):
		test_string = '{"metros": [{"code": "LIM", "continent": "South America", "coordinates": {"S": 12, "W": 77}, "country": "PE", "name": "Lima", "population": 9050000, "region": 1, "timezone": -5}, {"code": "MEX", "continent": "North America", "coordinates": {"N": 19, "W": 99}, "country": "MX", "name": "Mexico City", "population": 23400000, "region": 1, "timezone": -6}, {"code": "SCL", "continent": "South America", "coordinates": {"S": 33, "W": 71}, "country": "CL", "name": "Santiago", "population": 6000000, "region": 1, "timezone": -4}], "routes": [{"distance": 24530, "ports": ["LIM", "MEX"]}, {"distance": 2453, "ports": ["LIM", "SCL"]}, {"distance": 24530, "ports": ["MEX", "LIM"]}, {"distance": 4800, "ports": ["MEX", "SCL"]}, {"distance": 2453, "ports": ["SCL", "LIM"]}, {"distance": 4800, "ports": ["SCL", "MEX"]}]}'
		json_string = json.dumps(self.graph.convert_to_json(), sort_keys=True)
		self.assertEqual(json_string, test_string)


	def test_route_info(self):
		route = ['MEX', 'SCL', 'LIM']
		self.assertTrue(self.graph.is_valid_route(route))
		cost, time = self.graph.calculate_route_info(route)
		self.assertEqual(cost, 2415.90)
		self.assertEqual(time, 12.57)
		self.graph.remove_edge("MEX", "SCL")
		self.assertFalse(self.graph.is_valid_route(route))


	def test_shortest_path(self):
		shortest_path = ['MEX', 'SCL', 'LIM']
		route = self.graph.calculate_shortest_path(['MEX', 'LIM'])
		self.assertEqual(route, shortest_path)
		self.assertTrue(self.graph.add_vertex(city))
		route = self.graph.calculate_shortest_path(['MEX', 'CMI'])
		self.assertEqual(route, None)
		

if __name__ == '__main__':
	unittest.main()

