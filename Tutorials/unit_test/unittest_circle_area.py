#naming convention: <Modulename_test.py>
#To run type python -m unittest <name_of_test_module.py> -v 
#Passing the -v option to your test script will instruct unittest.main() to enable a higher level of verbosity.
#In this case unittest is the pkgname and <name_of_test_module.py> is the args





#A testcase is created by subclassing unittest.TestCase. The individual tests are defined with methods whose names start with the letters test. This naming convention informs the test runner about which methods represent tests.


#assertEqual() to check for an expected result; 
#assertTrue() or assertFalse() to verify a condition;
#assertRaises() to verify that a specific exception gets raised, i.e. TypeError, ValueError
#assertAlmostEqual()


#The setUp() and tearDown() methods allow you to define instructions that will be executed before and after each test method.



from circles import *

import unittest

class TestCircleArea(unittest.TestCase):

	def test_area(self): #each method should start with the word test
		#Test areas when radius >=0
		self.assertAlmostEqual(circle_area(1),pi)
		self.assertAlmostEqual(circle_area(0),0)
		self.assertAlmostEqual(circle_area(2.1),2.1**2*pi)
	
	def test_values(self):
	#Make sure value errors are aised when necessary
		self.assertRaises(ValueError, circle_area,-2)
	
	def test_types(self):
	#
		self.assertRaises(TypeError, circle_area,3+5j)
		self.assertRaises(TypeError, circle_area,True)
		self.assertRaises(TypeError, circle_area,"radius")
	
#help(unittest.TestCase.assertSetEqual)
if __name__=="__main__":
	unittest.main()
