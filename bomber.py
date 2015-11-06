#!/bin/usr/python3

try:
    import tkinter as tk
    from time import time
    from random import randint
    import sys
    import threading as th
    import socket as sk

    from labyrinthe import *
    from jokers import *
    from blowable import blowable
except ImportError as importError:
    print(importError)

RATIO_JOKER_POWER = 0.5

class Application(tk.Frame):
    """Application Bomberman"""
    def __init__(self, boss =None):
        tk.Frame.__init__(self, boss)
        self.boss = boss

        #Initialisation
        self.initialisation()


    def initialisation(self):
        self.sizemap = (75, 39)
        self.pas = 25
        self.canvas = tk.Canvas(self, width =self.sizemap[0] * self.pas,
                                height =self.sizemap[1] * self.pas, bg='light grey')
        self.canvas.pack()
        
        self.create_bomberman()
        self.laby = Labyrinthe(self.canvas, self.startingPositions[:len(self.players)])
        self.verify()
        self.pack()

    def verify(self):
        """Fonction timer pour vérifier le temps ou la fin de la partie"""
        #if Bombe.ensBomb != set():
        if Bombe.listBomb != [] and time() - Bombe.listBomb[0].start > 2:
            Bombe.listBombActiv.append(Bombe.listBomb.pop(0))
            Bombe.listBombActiv[-1].explode()
        self.after(100, self.verify)

    def create_bomberman(self):
        self.keysKeyboards = [['<Up>', '<Down>', '<Left>', '<Right>', '<space>'],
                              ['<z>', '<s>', '<q>', '<d>', '<f>'],
                              ['<o>', '<l>', '<k>', '<m>', '<j>'],
                              ['<t>', '<g>', '<f>', '<h>', '<y>']]

        self.players = ['Jean', 'Antoine', 'Dom']
        self.startingPositions = [(0, 0),
                                   (0, self.sizemap[1] - 1),
                                   (self.sizemap[0] - 1, 0),
                                   (self.sizemap[0] - 1, self.sizemap[1] - 1)]
        self.colors = ['red', 'blue', 'yellow', 'black', 'green', 'purple',
                       'pink', 'brown']

        self.listBombermans = {}

        for player, position, color, keys in zip(self.players,
            self.startingPositions, self.colors, self.keysKeyboards):
            self.listBombermans[player] = Bomberman(self.canvas, position,
                                                    color, keys, player)
            

class Labyrinthe():
    """Modelisation d'un labyrinthe"""
    def __init__(self, boss, startingPositions):
        self.startPos = set(startingPositions)
        self.boss = boss

        #Initialisation
        self.initialisation()

    def initialisation(self):
        self.sizemap = self.boss.master.sizemap
        self.pas = self.boss.master.pas
        self.draw_laby()
        self.dictJoker = dict()

    def algo_map1(self, ens):
        """Algo du labyrinthe"""
        ensCaseVide = ens
        #ensCaseVide = self.algoLaby(ensCaseVide)
        ensCaseVide = genereMap(ensCaseVide, self.sizemap)
        ensTotal = {(x, y) for x in range(self.sizemap[0])
                    for y in range(self.sizemap[1])}
        self.ensBlock = ensTotal - ensCaseVide

    def algo_map2(self, ens):
        """Algo d'une map aux blocks aléatoires"""
        RATIOBLOCK = 0.5
        nbrCaseTotal = self.sizemap[0] * self.sizemap[1]
        ensBlock = set()
        while len(ensBlock) < RATIOBLOCK * nbrCaseTotal:
            ensBlock.add((randint(0, self.sizemap[0] - 1),
                          randint(0, self.sizemap[1] - 1)))
        for position in ens:
            if position in ensBlock:
                ensBlock.remove(position)
            if (position[0] - 1, position[1]) in ensBlock:
                ensBlock.remove((position[0] - 1, position[1]))
            if (position[0] + 1, position[1]) in ensBlock:
                ensBlock.remove((position[0] + 1, position[1]))
            if (position[0], position[1] - 1) in ensBlock:
                ensBlock.remove((position[0], position[1] - 1))
            if (position[0], position[1] + 1) in ensBlock:
                ensBlock.remove((position[0], position[1] + 1))
        self.ensBlock = ensBlock

    def draw_laby(self):
        """Dessine la map"""
        #print(self.startPos)
        self.algo_map1(self.startPos)
        for block in self.ensBlock:
            (x, y) = (block[0] * self.pas, block[1] * self.pas)
            self.boss.create_rectangle(x, y, x + self.pas, y + self.pas,
                                       fill='grey')
        
class Bomberman(blowable):
    """Modélisation d'un personnage le <Bomberman<"""
    def __init__(self, boss, positionDepart, color, keys, name):
        self.boss = boss
        self.name = name
        self.position = positionDepart
        self.color = color
        self.keys = keys

        self.sizemap = boss.master.sizemap
        self.pas = boss.master.pas
        (x, y) = self.position[0] * self.pas, self.position[1] * self.pas
        self.id = self.boss.create_oval(x + 5, y + 5, x + self.pas - 5,
                                       y + self.pas - 5, fill =color)
        self.numberBomb = 2
        self.power = 75
        self.move()

    def move(self):
        possible = ['N', 'S', 'W', 'E', 'Put Bomb']
        for i in range(5):
            self.boss.master.boss.bind(self.keys[i], lambda event =0,
                                       cmd =possible[i]:
                                       self.action(event, cmd))
                
    def action(self, event, cmd):
        (x, y) = self.position
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
        ensBlock = self.boss.master.laby.ensBlock
        if (x, y) in ensBlock or x < 0 or x >= self.sizemap[0] \
           or y < 0 or y >= self.sizemap[1]:
            pass
        else:
            self.position = (x, y)
            #print(self.pos)
            self.boss.coords(self.id, x * self.pas + 5, y * self.pas + 5,
                            x * self.pas + self.pas - 5,
                            y * self.pas + self.pas - 5)
            self.boss.tag_raise(self.id)
        if cmd == 'Put Bomb' and self.numberBomb:
            self.numberBomb -= 1
            Bombe.listBomb.append(Bombe(self.boss, self.position, self.power,
                                     self.name))

    def game_over(self):
        for i in range(5):
            self.boss.master.boss.bind(self.keys[i], self.none_action)
        self.boss.coords(self.id, -10, -10, -10, -10)

    def none_action(self, event):
        pass

class Bombe(blowable):
    """Modélisation d'une bombe"""
    listBomb = []
    listBombActiv = []
    def __init__(self, boss, position, power, name):
        self.pas = boss.master.laby.pas
        self.boss = boss
        self.position = position
        self.power = power
        self.name = name
        self.start = time()
        (x, y) = self.position[0] * self.pas, self.position[1] * self.pas
        self.boss.create_oval(x + 7, y + 7, x + self.pas - 7,
                                       y + self.pas - 7, fill='black')
        self.boss.master.laby.ensBlock.add(self.position)

    def listExplode(self):

        ensBlock = self.boss.master.laby.ensBlock - {self.position}
        self.ensTotal = set()
        self.ensBreakBlock = set()

        for i in range(self.power + 1):
            add = (self.position[0], self.position[1] + i)
            self.ensTotal.add(add)
            if add in ensBlock:
                self.ensBreakBlock.add(add)
                break
        for i in range(self.power + 1):
            add = (self.position[0], self.position[1] - i)
            self.ensTotal.add(add)
            if add in ensBlock:
                self.ensBreakBlock.add(add)
                break
        for i in range(self.power + 1):
            add = (self.position[0] + i, self.position[1])
            self.ensTotal.add(add)
            if add in ensBlock:
                self.ensBreakBlock.add(add)
                break
        for i in range(self.power + 1):
            add = (self.position[0] - i, self.position[1])
            self.ensTotal.add(add)
            if add in ensBlock:
                self.ensBreakBlock.add(add)
                break
        #print(self.ensTotal)
        '''
        L1 = [(x, self.position[1]) for x in
              range(self.position[0] - self.power,
                    self.position[0] + self.power + 1)]
        L2 = [(self.position[0], y) for y in
              range(self.position[1] - self.power,
                    self.position[1] + self.power + 1)]
        self.ensTotal = set(L1 + L2)
        '''
    
    def explode(self):
        self.listExplode()
        self.listExplosion = []
        for block in self.ensTotal:
            (x, y) = block[0] * self.pas, block[1] * self.pas
            self.listExplosion.append(self.boss.create_rectangle(x, y,
                                      x + self.pas, y + self.pas, fill='red'))
            try:
                self.boss.master.laby.ensBlock.remove(block)
            except:
                pass
        for bomberman in self.boss.master.listBombermans.values():
            if bomberman.position in self.ensTotal:
                bomberman.game_over()
        self.boss.master.listBombermans[self.name].numberBomb += 1
        self.boss.master.after(150, self.end_explode)

    def end_explode(self):
        for block in self.ensTotal:
            #self.boss.delete(block)
            #print(block)
            (x, y) = block[0] * self.pas, block[1] * self.pas
            self.boss.create_rectangle(x, y,
                                      x + self.pas, y + self.pas, fill='light grey', outline = 'light grey')
        for block in self.ensBreakBlock:
            self.boss.master.laby.dictJoker[block] = Joker_Power(boss, block)



        
            
if __name__ == '__main__':
    winRoot = tk.Tk()
    Application(winRoot).mainloop()
    #i = input()

