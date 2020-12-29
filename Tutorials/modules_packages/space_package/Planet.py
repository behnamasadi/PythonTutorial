class planet:
    shape="round"

    def printInfo(self,x=10):
        print(self.shape,x)

    def __init__(self,radius=1,name="earth",gravity=9.8,system="solar"):
        self.radius=radius
        self.name=name
        self.gravity=gravity
        self.system=system

    @classmethod
    def comment(cls):
        return f'All {cls.shape} becuase of gravity'

    @staticmethod
    def spin(speed='2000 miles per hour'):
        return f'The planet spins at {speed}'

