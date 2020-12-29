#setUpClass and tearDownClass are run once for the whole class; setUp and tearDown are run before and after each test method.
class Example(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    def setUp(self):
        print("setUp")

    def test1(self):
        print("test1")

    def test2(self):
        print("test2")

    def tearDown(self):
        print("tearDown")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")
