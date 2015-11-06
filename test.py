

class Parent:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.initialisation()

    def initialisation(self):
        self.a = 123456789

class Fils(Parent):
    def __init__(self, x, y):
        Parent.__init__(self, x, y)
        #self.initialisation2()

    def initialisation(self):
        self.b = 1234678
        


r = Fils(1, 2)
print(r.b)
print(r.a)


