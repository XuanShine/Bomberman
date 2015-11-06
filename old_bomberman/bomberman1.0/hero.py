from tkinter import *
from random import randint

from labyrinthe import *

#Paramètres du jeux

SIZEMAP = (67, 35) #Taile de la map (en carreau) (IMPAIRE !)
PAS = 20 #Taille de chaque carreau (en pixel)
position = (0, 0) #position de départ

win = False
hero = None #Dessin du hero

ensembleTotal = set()
ensembleCaseVide = set()

for x in range(SIZEMAP[0]):
    for y in range(SIZEMAP[1]):
        ensembleTotal.add((x, y))

ensembleCaseVide.add((0, 0))
ensembleCaseVide = genereMap(ensembleCaseVide, SIZEMAP)

ensBlock = ensembleTotal - ensembleCaseVide

def avance(position, direction, listBlock, SIZEMAP):
    """Renvoie les coordonnées du tuple 'position' dans la 'direction'
('N', 'S', 'W', 'E') sans le déplacer sur la liste des Block ni en dehors de
la SIZEMAP"""
    (x, y) = (position[0], position[1]) #On garde les coordonnées en mémoire
    if direction == 'N': y -= 1
    if direction == 'S': y += 1
    if direction == 'W': x -= 1
    if direction == 'E': x += 1
    if (x, y) in listBlock: #Si elle se déplace sur un block
        (x, y) = position
    #Si elle sort du cadre
    elif 0 > x or x > SIZEMAP[0] - 1 or 0 > y or y > SIZEMAP[1] - 1:
        (x, y) = position
    return (x, y)


#----Commandes Actions------
def up(event):
    global position
    position = avance(position, 'N', ensBlock, SIZEMAP)
    canvasMap.coords(hero, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def down(event):
    global position
    position = avance(position, 'S', ensBlock, SIZEMAP)
    canvasMap.coords(hero, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def left(event):
    global position
    position = avance(position, 'W', ensBlock, SIZEMAP)
    canvasMap.coords(hero, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def right(event):
    global position
    position = avance(position, 'E', ensBlock, SIZEMAP)
    canvasMap.coords(hero, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def createMap():
    global hero
    for case in ensBlock:
        canvasMap.create_rectangle(case[0] * PAS, case[1] * PAS,
                               case[0] * PAS + PAS, case[1] * PAS + PAS,
                               fill='blue', outline='blue')
    hero = canvasMap.create_oval(position[0] * PAS + 5,
                                  position[1] * PAS + 5,
                                  position[0] * PAS + PAS - 5,
                                  position[1] * PAS + PAS - 5, fill='black')
    canvasMap.create_oval((SIZEMAP[0] - 1) * PAS, (SIZEMAP[1] - 1) * PAS,
                        (SIZEMAP[0] - 1) * PAS + PAS,
                       (SIZEMAP[1] - 1) * PAS + PAS, fill='green')

def verify():
    """Verifie si le hero est sur le ptArrive"""
    global win
    if position == (SIZEMAP[0] - 1, SIZEMAP[1] - 1) and not win:
        win = True
        over = Toplevel()
        canvasMap.delete('all')

        msg = Label(over, text='YOU WIN !')
        msg.pack()

        Button(over, text='Quitter', command=winRoot.destroy).pack()
    winRoot.after(400, verify) #Verifie tous les 400ms si win ou pas

#-----Jeux--------
winRoot = Tk()

canvasMap = Canvas(winRoot, width=SIZEMAP[0] * PAS, height=SIZEMAP[1] * PAS,
                      bg='dark grey')
canvasMap.pack()

createMap()

winRoot.bind('<Up>', up)
winRoot.bind('<Down>', down)
winRoot.bind('<Left>', left)
winRoot.bind('<Right>', right)

verify()
winRoot.mainloop()

