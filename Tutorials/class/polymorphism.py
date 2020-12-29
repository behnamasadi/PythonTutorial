# Polymorphism
####################### A simple Python function to demonstrate #######################


def add(x, y, z=0):
    return x + y + z


# Driver code
print(add(2, 3))
print(add(2, 3, 4))


######################## Polymorphism with class methods ########################
class Dog:
    def say(self):
        print("hau")


class Cat:
    def say(self):
        print("meow")


pet = Dog()
pet.say()  # prints "hau"
another_pet = Cat()
another_pet.say()  # prints "meow"

my_pets = [pet, another_pet]
for a_pet in my_pets:
    a_pet.say()


####################Polymorphism with Inheritance####################
class Bird:
    def intro(self):
        print("There are many types of birds.")

    def flight(self):
        print("Most of the birds can fly but some cannot.")


class sparrow(Bird):
    def flight(self):
        print("Sparrows can fly.")


class ostrich(Bird):
    def flight(self):
        print("Ostriches cannot fly.")


obj_bird = Bird()
obj_spr = sparrow()
obj_ost = ostrich()

obj_bird.intro()
obj_bird.flight()

obj_spr.intro()
obj_spr.flight()

obj_ost.intro()
obj_ost.flight()
