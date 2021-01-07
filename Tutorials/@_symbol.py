# An @ symbol at the beginning of a line is used for 
# 1) class
# 2) function 
# 3) method 
# 4) decorators


print('####################### @property #######################')
class student(object):
    def __init__(self,firstname, lastname):
        self._firstname=firstname
        self._lastname=lastname
    @property
    def firstname(self):
        return self._firstname
    @firstname.setter
    def firstname(self,firstname):
        self._firstname = firstname
std=student('john','smith')
print(std.firstname)
std.firstname='new first name'
print(std.firstname)


print('####################### @classmethod, @staticmethod #######################')
# https://docs.python.org/3/library/functions.html#classmethod

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

print('####################### @decorators #######################')
