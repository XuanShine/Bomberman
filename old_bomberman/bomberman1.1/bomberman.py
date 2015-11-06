#!/bin/usr/python3

import tkinter as tk

from labyrinthe import *

class App(tk.Canvas):
    def __init__(self, boss=None, width=1000, height=700):
        tk.Canvas.__init__(self, boss, width=width, height=height)
        self.laby = Labyrinthe(self)

        

class Labyrinthe():
    def __init__(self, canvas, sizemap=(41, 21), pas=25):
        self.SIZEMAP = sizemap
        self.PAS = pas
        self.CAN = canvas
        self.dessinLaby()
        self.createBomberman()

    def algoLaby(self, ens):
        return

    def boom(self, *position):
        for coord in position:
            (x, y) = (coord[0] * self.pas, coord[1] * self.pas)
            self.CAN.create_rectangle(x, y, x + self.pas, y + self.pas)

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
        self.ID = self.CAN.create_oval(x + 5, y + 5, x + self.PAS - 5, y + self.PAS - 5)

    def action(e, cmd, block):
        (x, y) = self.pos
        print(cmd)
        if cmd == 'N':
            y -= 1
        elif cmd == 'S':
            y += 1
        elif cmd == 'W':
            x -= 1
        elif cmd == 'E':
            print('E')
            x += 1
        elif cmd == 'Put Bomb':
            self.bomb1 = Bombe()
        #print((x, y) in block)
        if (x, y) in block:
            pass
        else:
            self.pos = (x, y)
            print(self.pos)
            self.CAN.coords(self.ID, x * self.PAS + 5, y * self.PAS + 5,
                            x * self.PAS + self.PAS - 5,
                            y * self.PAS + self.PAS - 5)

class Bombe():
    #1/ Afficher Bombe
    #2/ Ajout dans un ensemble
    #3/ Lancer un Timer
    pass

winRoot = tk.Tk()
y = App(winRoot)
y.pack()
winRoot.bind('<Up>', lambda cmde='N', ens=y.laby.ensBlock: y.laby.b1.action(cmde, ens))
winRoot.bind('<Down>', lambda cmde='S', ens=y.laby.ensBlock: y.laby.b1.action(cmde, ens))
winRoot.bind('<Left>', lambda cmde='W', ens=y.laby.ensBlock: y.laby.b1.action(cmde, ens))
winRoot.bind('<Right>', lambda cmde='E', ens=y.laby.ensBlock: y.laby.b1.action(cmde, ens))
winRoot.bind('<space>', lambda cmde='Put Bombe', ens=y.laby.ensBlock: y.laby.b1.action(cmde, ens))
winRoot.mainloop()
