try:
    from blowable import blowable
except ImportError as importEror:
    print(importError)

class Joker(blowable):
    """class parent des Jokers"""
    def __init__(self, boss, position):
        self.boss = boss
        self.pas = self.boss.master.pas
        self.position = position

        #initialisation
        #self.initialisation()

    def delete(self):
        self.boss.delete(self.id)
        self.position = (-10, -10)

class Joker_Power(Joker):
    def __init__(self, boss, position, state):
        Joker.__init__(boss, position)
        self.state = state

        #initiaisation
        self.initialisation()

    def initialisation(self):
        (x, y) = (self.position[0] * self.pas, self.position[1] * self.pas)
        if self.state == 1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='green')
        elif self.state == -1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='red')
        else:
            print('erreur d\'entrée du Joker Power')

    def action(self, bomberman):
        """Si un bomberman l'active"""
        bomberman.power += self.state
        self.delete()

class Joker_Bomb(Joker):
    def __init__(self, boss, position, state):
        Joker.__init__(boss, position)
        self.state = state

        #initiaisation
        self.initialisation()

    def initialisation(self):
        (x, y) = (self.position[0] * self.pas, self.position[1] * self.pas)
        if self.state == 1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='green')
        elif self.state == -1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='red')
        else:
            print('erreur d\'entrée du Joker Bomb')

    def action(self, bomberman):
        """Si un bomberman l'active"""
        if bomberman.numberBomb == 1 and self.state == -1:
            pass
        else:
            bomberman.numberBomb += self.state
        self.delete()

class Joker_SuperBomb(Joker):
    def __init__(self, boss, position):
        Joker.__init__(boss, position)

        #initiaisation
        self.initialisation()

    def initialisation(self):
        (x, y) = (self.position[0] * self.pas, self.position[1] * self.pas)
        if self.state == 1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='green')
        elif self.state == -1:
            self.id = self.boss.create.create_oval(x, y, x + 5 + self.pas,
                                            y + 5 + self.pas, fill ='red')
        else:
            print('erreur d\'entrée du Joker SuperBomb')

    def action(self, bomberman):
        """Si un bomberman l'active"""
        bomberman.superBomb = True
        self.delete()

