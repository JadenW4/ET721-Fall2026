"""
Jaden Wiltshire
lab 5: review of class, object, methods, and attributes
Sep 16, 2026
"""

print("\n---- Example 1: class Circle ------")


class Circle():
    # values that need to pass to the object of class Circle
    def __init__(self, radius, color):
        self.r = radius
        self.c = color

    # attributes
    pi = 3.14157

    # method
    def circumference(self):
        return 2 * self.pi * self.r


# create instance object of the class
c1 = Circle(2, "red")
print(c1.c)
print(c1.circumference())


print("\n---- Example 2: class Rectangle ------")


class Rectangle():
    def __init__(self, height, width, color):
        self.h = height
        self.w = width
        self.c = color

    # method to calculate the area
    def area(self):
        return self.w * self.h

    # method to calculate the perimeter
    def perimeter(self):
        return 2 * self.w + 2 * self.h

    # method to draw the rectangle
    """
    def drawRectangle(self):
        plt.gca().add_patch(plt.Rectangle((0,0), self.w, self.h, fc=self.c))
        plt.axis('scaled')
        plt.show()
    """


# create instance object of the class
r1 = Rectangle(2, 3, "olive")
print(f"The perimeter of rectangle with height = {r1.h} "
      f"and width = {r1.w} is {r1.perimeter()}")


print("\n---- Example 3: Car Dealership Inventory ----")


# Task 1 & 2: Create a class to represent each vehicle
class Car():
    # Default color for all vehicles
    color = "white"

    def __init__(self, max_speed, mileage):
        self.max_speed = max_speed
        self.mileage = mileage
        self.seats = 0

    # Task 3: Method to assign seating capacity
    def seating_capacity(self, seats):
        self.seats = seats

    # Task 4: Method to display all properties
    def display_properties(self):
        print(f"The {self.color} car has {self.seats} seats, "
              f"with {self.mileage} miles and a maximum speed of "
              f"{self.max_speed}")


# Task 5: Create two instance objects of the car

# First car
car1 = Car(200, 50000)
car1.seating_capacity(5)

# Second car
car2 = Car(180, 75000)
car2.seating_capacity(4)


# Display properties of both cars
print("\n---- Car 1 ----")
car1.display_properties()

print("\n---- Car 2 ----")
car2.display_properties()