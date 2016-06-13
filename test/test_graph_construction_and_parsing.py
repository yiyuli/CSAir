import unittest
import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir) 

from graph.graph import Graph

class TestGraphConstructionAndParsing(unittest.TestCase):
	""" Tests for graph construction and parsing.

	Tests for graph construction and parsing.
	Tests include tests vertices and edges construction.

	"""
	def setUp(self):
		self.graph = Graph()
		self.graph.load("../json/test_data.json")


	def test_vertices_construction(self):
		self.assertTrue("MEX" in self.graph.vertices.keys())
		self.assertTrue("LIM" in self.graph.vertices.keys())
		self.assertTrue("SCL" in self.graph.vertices.keys())


	def test_edges_construction(self):
		edges = []
		for edge in self.graph.edges.values():
			edges.append(edge.departure.code + " -> " + edge.destination.code + ", " + str(edge.distance))
		edges.sort()
		self.assertEqual(edges, ['LIM -> MEX, 24530', 'LIM -> SCL, 2453', 'MEX -> LIM, 24530', 'MEX -> SCL, 4800', 'SCL -> LIM, 2453', 'SCL -> MEX, 4800'])


if __name__ == '__main__':
	unittest.main()
