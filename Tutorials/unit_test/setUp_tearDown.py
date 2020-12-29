#test fixture test case test suite test runner




import unittest


#When a setUp() method is defined, the test runner will run that method prior to each test. Likewise, if a tearDown() method is defined, the test runner will invoke that method after each test.

#Suppose you have a suite with 10 tests. 8 of the tests share the same setup/teardown code. The other 2 don't.

#setup and teardown give you a nice way to refactor those 8 tests. Now what do you do with the other 2 tests? You'd move them to another testcase/suite. So using setup and teardown also helps give a natural way to break the tests into cases/suites

class SomeTest(unittest.TestCase):
	def setUp(self):
		super(SomeTest, self).setUp()
		self.mock_data = [1,2,3,4,5]
		print("setUp")

	def test_len(self):
		self.assertEqual(len(self.mock_data), 5)

	def test_equal(self):
		self.assertEqual(self.mock_data,[1,2,3,4,5] )

	def tearDown(self):
		super(SomeTest, self).tearDown()
		self.mock_data = []
		print("tearDown")


if __name__ == '__main__':
    unittest.main()
