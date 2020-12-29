# classmethod must have a reference to a class object as the first parameter, whereas staticmethod can have no
# parameters at all.

class Date:
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


date = Date.from_string('11-09-2012')
print(date.day, date.month, date.year)


class A:
    a = 10

    def increase(self):
        self.a += 1

    @classmethod
    def class_method(cls):
        print(cls.a)

    @classmethod
    def update_a(x):
        cls.a = x

    @staticmethod
    def static_method():
        # print(self.a) #this will not work
        return


A.class_method()

a = A()

a.increase()
a.class_method()
A.class_method()
