class Fils:
    def __init__(self, boss, a, b):
        self.boss = boss
        self.x, self.y = boss.x, boss.y
        self.a, self.b = a, b
        boss.x += self.a
        self.y -= self.b

class Parent:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.t = Fils(self, 5, 8)


r = Parent(1, 2)
print(r.x, r.y)

