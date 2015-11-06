#!/bin/usr/python3

try:
    import tkinter as tk
    from time import time

    from labyrinthe import *
except ImportError as e:
    print(e)

class Application(tk.Frame):
    def __init__(self, boss =None):
        tk.Frame.__init__(self, boss)
        self.SIZEMAP = (31, 21)
        self.PAS = 20

        self.CANVAS = tk.Canvas(self, width=self.SIZEMAP[0] * self.PAS,
                                height=self.SIZEMAP[1] * self.PAS)
        self.CANVAS.pack()
        self.laby = Labyrinthe(self.CANVAS)
        self.commandes()
        self.verify()
        self.pack()
        
    def commandes(self):
        self.bind('<Up>', lambda sel=self.laby, cmd='N': self.laby.action(sel, cmd))
        self.bind('<Down>', lambda sel=self, cmd='S': self.laby.action(sel, cmd))
        self.bind('<Left>', lambda sel=self, cmd='W': self.laby.action(sel, cmd))
        self.bind('<Right>', lambda sel=self, cmd='E': self.laby.action(sel, cmd))
        self.bind('<space>', lambda sel=self, cmd='Put Bomb': self.laby.action(sel, cmd))

    def verify(self):
        """Fonction timer pour vérifier le temps ou la fin de la partie"""
        if self.laby.timerBomb + 3 < time() and self.laby.timerBomb != 0:
            self.laby.b1.numberBomb += 1
            self.laby.timerBomb = 0
            self.laby.boom(self.laby.bomb1.POSITION)
            
        self.after(100, self.verify)

class Labyrinthe():
    def __init__(self, boss):
        self.SIZEMAP = boss.master.SIZEMAP
        self.PAS = boss.master.PAS
        self.CAN = boss
        self.dessinLaby()
        self.createBomberman()
        self.timerBomb = 0

    def action(self, event, cmd):
        #print(self, event, cmd)
        if cmd == 'N':
            self.b1.action('N', self.ensBlock)
        elif cmd == 'S':
            self.b1.action('S', self.ensBlock)
        elif cmd == 'W':
            self.b1.action('W', self.ensBlock)
        elif cmd == 'E':
            self.b1.action('E', self.ensBlock)
        elif cmd == 'Put Bomb':
            if self.b1.numberBomb:
                self.b1.numberBomb -= 1
                self.ensBlock.add(self.b1.pos)
                self.bomb1 = Bombe(self.CAN, self.b1.pos, self.PAS)
                self.timerBomb = time()
            

    def algoLaby(self, ens):
        return

    def boom(self, *position):
        print(position)
        for coord in position:
            (x, y) = (coord[0] * self.PAS, coord[1] * self.PAS)
            self.CAN.create_rectangle(x, y, x + self.PAS, y + self.PAS, fill='blue')

    def createBomberman(self):
        self.b1 = Bomberman(self.CAN, (0, 0), 'blue', self.SIZEMAP, self.PAS) 

    def dessinLaby(self):
        ensCaseVide = {(0, 0)}
        #ensCaseVide = self.algoLaby(ensCaseVide)
        ensCaseVide = genereMap(ensCaseVide, self.SIZEMAP)
        ensTotal = {(x, y) for x in range(self.SIZEMAP[0]) for y in range(self.SIZEMAP[1])}
        self.ensBlock = ensTotal - ensCaseVide
        
        for block in self.ensBlock:
            (x, y) = (block[0] * self.PAS, block[1] * self.PAS)
            self.CAN.create_rectangle(x, y, x + self.PAS, y + self.PAS, fill='grey')
        
class Bomberman():
    def __init__(self, canvas, positionDepart, color, sizemap, pas):
        self.CAN = canvas
        self.pos = positionDepart
        self.COLOR = color
        self.SIZEMAP = sizemap
        self.PAS = pas
        (x, y) = self.pos[0] * pas, self.pos[1] * pas
        self.ID = self.CAN.create_oval(x + 5, y + 5, x + self.PAS - 5,
                                       y + self.PAS - 5)
        self.numberBomb = 1

    def action(self, cmd, block):
        (x, y) = self.pos
        #print(cmd)
        if cmd == 'N':
            y -= 1
        elif cmd == 'S':
            y += 1
        elif cmd == 'W':
            x -= 1
        elif cmd == 'E':
            x += 1
        #print((x, y) in block)
        if (x, y) in block or x < 0 or x >= self.SIZEMAP[0] \
           or y < 0 or y >= self.SIZEMAP[1]:
            pass
        else:
            self.pos = (x, y)
            #print(self.pos)
            self.CAN.coords(self.ID, x * self.PAS + 5, y * self.PAS + 5,
                            x * self.PAS + self.PAS - 5,
                            y * self.PAS + self.PAS - 5)

class Bombe():
    #1/ Afficher Bombe
    #2/ Ajout dans un ensemble
    #3/ Lancer un Timer
    def __init__(self, canvas, position, pas):
        self.PAS = pas
        self.CAN = canvas
        self.POSITION = position
        (x, y) = self.POSITION[0] * pas, self.POSITION[1] * pas
        self.CAN.create_oval(x + 6, y + 6, x + self.PAS - 6,
                                       y + self.PAS - 6, fill='red')


if __name__ == '__main__':
    Application().mainloop()

