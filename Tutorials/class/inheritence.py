# https://stackoverflow.com/questions/4015417/python-class-inherits-object
# Is there any reason for a class declaration to inherit from object?
# In Python 2: always inherit from object explicitly. Get the perks.
# In Python 3: inherit from object if you are writing code that tries to be Python agnostic, that is, it needs to
# work both in Python 2 and in Python 3. Otherwise don't, it really makes no difference since Python inserts it for you
# behind the scenes.

# Python methods are always virtual
class Base:
    value = None

    def __init__(self, value=1):
        self.value = value
        return

    def info(self):
        print(f'This is Base and value is {self.value}')
        print('This is Base and value is {}'.format(self.value))


class derived2(Base):
    def __init__(self):
        return


class derived1(Base):
    def __init__(self, base_val=2, class_val=3):
        super().__init__(base_val)
        self.class_val = 3
        return


Base_obj = Base(10)
Base_obj.info()

derived1_obj = derived1()
derived1_obj.info()
