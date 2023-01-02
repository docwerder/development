from __future__ import annotations

class meineKlasse():
    def __init__(self, inittext='Wert0'):
        self.instatt = inittext
        print(self.instatt)

    def __del__(self):
        print('Klasse wird gelöscht!')

    def __str__(self):
        str = "New instance of {0}".format(self.instatt)
        return str


x = meineKlasse('text1')
y = meineKlasse()
print(y)
#del(x)


class Car:
    def __init__(self):
        print("Building the Car")
        self.name = "Lamborghini"
        self.max_speed = "220 mph"

    def display(self):
        print(f"Name: {self.name}")
        print(f"Max Speed: {self.max_speed}")

    def __del__(self):
        print("Destroying the Car")


# creating object of the class
# myCar = Car()

# calling the display function of the myCar object
# myCar.display()

# manually deleting the object using the del keyword
# del myCar
# myCar.display()

# ====================================================

class Point:
    def __init__(self, x, y, srs):
        self.x = x
        self.y = y
        self.srs = srs

    def __str__(self):
        str = "Point({0}, {1}) ".format(self.x, self.y)
        str += "EPSG code: {0}".format(self.srs)
        return str

ptn1 = Point(3, 12, 4555)
ptn2 = Point(6, 16, 4555)

print(ptn1)
# class Point3D(Point):

