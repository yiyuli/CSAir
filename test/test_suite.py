import unittest
from test_graph_query import TestGraphQuery
from test_graph_construction_and_parsing import TestGraphConstructionAndParsing

def suite():
	test_suite = unittest.TestSuite()
	test_suite.addTest(unittest.makeSuite(TestGraphConstructionAndParsing))
	test_suite.addTest(unittest.makeSuite(TestGraphQuery))
	return test_suite

if __name__ == '__main__':
	test_suite = suite()
	runner = unittest.TextTestRunner()
	runner.run(test_suite)