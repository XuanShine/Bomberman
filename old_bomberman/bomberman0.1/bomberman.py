import tkinter as tk

from random import randint
from time import time


SIZEMAP = (40, 30) #Taile de la map (en carreau)

name = 'Xuan'

#Paramètres du jeux
RATIOBLOCK = 0.5 #le ratio de block/case_dispo

PAS = 30 #Taille de chaque carreau (en pixel)
power = 3 #Puissance de la bombe
position = (0, 0) #position de départ
end_game = 0
#Variables utiles au programme
bombeRestant = True
superPower = True
error = True
start = 0
positionBombe = 0
bombe = 0
bomberMan = 0

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

def listeCase(position, power, superPower):
    """Renvoie la liste des coordonnées des blocks touché par la bombe en
fonction de la case inititale de la bombe (position), de la puissance (power),
de la possibilité du superPower"""
    if superPower:
        L1 = [(x, position[1]) for x in
              range(position[0] - power, position[0] + power + 1)]
        L2 = [(position[0], y) for y in
              range(position[1] - power, position[1] + power + 1)]
    return L1 + L2

def genereMap(SIZEMAP, RATIOBLOCK):
    """Renvoie un ensemble qui contient les coordonnées des blocks pour
pouvoir dessiner une map aléatoire en fonction de la taille de la map
et du ratio block/case_dispo EN ENLEVANT les positions du bomberMan
et des cases autour"""
    nbrCaseTotal = SIZEMAP[0] * SIZEMAP[1]
    ensBlock = set()
    while len(ensBlock) < RATIOBLOCK * nbrCaseTotal:
        ensBlock.add((randint(0, SIZEMAP[0] - 1), randint(0, SIZEMAP[1] - 1)))
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
    return ensBlock

ensBlock = genereMap(SIZEMAP, RATIOBLOCK)

#----Commandes Actions------
def up(event=None):
    global position
    position = avance(position, 'N', ensBlock, SIZEMAP)
    canvasMap.coords(bomberMan, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def down(event=None):
    global position
    position = avance(position, 'S', ensBlock, SIZEMAP)
    canvasMap.coords(bomberMan, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def left(event=None):
    global position
    position = avance(position, 'W', ensBlock, SIZEMAP)
    canvasMap.coords(bomberMan, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

def right(event=None):
    global position
    position = avance(position, 'E', ensBlock, SIZEMAP)
    canvasMap.coords(bomberMan, position[0] * PAS + 5,
                     position[1] * PAS + 5,
                     position[0] * PAS + PAS - 5,
                     position[1] * PAS + PAS - 5)

#----Actualisation/Refreshing--------
def createMap():
    global bomberMan
    canvasMap.delete('all')
    for x in range(0, SIZEMAP[0] * PAS + PAS, PAS):
        canvasMap.create_line(x, 0, x, SIZEMAP[1] * PAS + PAS)
    for y in range(0, SIZEMAP[1] * PAS + PAS, PAS):
        canvasMap.create_line(0, y, SIZEMAP[0] * PAS + PAS, y)
    for case in ensBlock:
        canvasMap.create_rectangle(case[0] * PAS, case[1] * PAS,
                               case[0] * PAS + PAS, case[1] * PAS + PAS,
                               fill='yellow')
    bomberMan = canvasMap.create_oval(position[0] * PAS + 5,
                                  position[1] * PAS + 5,
                                  position[0] * PAS + PAS - 5,
                                  position[1] * PAS + PAS - 5, fill='black')
    canvasMap.create_oval((SIZEMAP[0] - 1) * PAS, (SIZEMAP[1] - 1) * PAS,
                       (SIZEMAP[0] - 1) * PAS + PAS,
                       (SIZEMAP[1] - 1) * PAS + PAS, fill='green')

#-----Ce qui se passe lorsqu'on place une bombe (la touche <space>)
def putBomb(event=None):
    global ensBlock, bombeRestant, start, positionBombe, bombe
    if bombeRestant:
        #On ajoute la position de la bombe dans 'ensBlock' pour ne pas
        #pouvoir marcher dessus
        start = time()
        bombeRestant = False
        positionBombe = position
        ensBlock.add(positionBombe)
        #Afficher la bombe
        bombe = canvasMap.create_oval(positionBombe[0] * PAS + 7,
                                    positionBombe[1] * PAS + 7,
                                    positionBombe[0] * PAS + PAS - 7,
                                    positionBombe[1] * PAS + PAS - 7,
                                    fill='red')

def gameOver():
    over = tk.Toplevel()
    canvasMap.delete('all')

    msg = tk.Label(over, text='GAME OVER !')
    msg.pack()

    tk.Button(over, text='Quitter', command=winRoot.destroy).pack()
    print('GAME OVER !')

def boom():
    """Ce qui se passe lors de l'explosion"""
    global ensBlock
    #Déterminer la liste des cases 'abimées' par l'explosion et les détruire
    listDestroy = listeCase(positionBombe, power, superPower)
    if position in listDestroy: #Si on est présent dans la zone de l'explosion
        gameOver()
        #winRoot.destroy()
    else:
        for case in listDestroy:
            try:
                ensBlock.remove(case)
            except:
                pass
        createMap()

def verify():
    """Losqu'une bombe est posée, cette fonction permet de la faire
exploser !"""
    global start, positionBombe, bombeRestant, ensBlock, error, end_game
    if time() > start + 1.5 and start != 0:
        bombeRestant = True
        boom()
        start = 0
        
        #ensBlock.remove(positionBombe)
        canvasMap.delete(bombe)
    if position == (SIZEMAP[0] - 1, SIZEMAP[1] - 1) and error:
        error = False
        over = tk.Toplevel()
        end_game = time()
        canvasMap.delete('all')

        
        msg = tk.Label(over, text='YOU WIN ! T\'as mis {} secondes'.format(int(end_game - start_game)))
        msg.pack()

        tk.Button(over, text='Quitter', command=winRoot.destroy).pack()
    winRoot.after(100, verify) #Un timer


#-----Jeux--------
#name = input('Quel est ton nom ?\n')

winRoot = tk.Tk()

canvasMap = tk.Canvas(winRoot, width=SIZEMAP[0] * PAS, height=SIZEMAP[1] * PAS,
                      bg='dark grey')
canvasMap.pack()

createMap()

winRoot.bind_all('<z>', up)
winRoot.bind_all('<s>', down)
winRoot.bind_all('<q>', left)
winRoot.bind_all('<d>', right)
winRoot.bind_all('<space>', putBomb)

'''
winRoot.bind_all('<Up>', up)
winRoot.bind_all('<Down>', down)
winRoot.bind_all('<Left>', left)
winRoot.bind_all('<Right>', right)
winRoot.bind_all('<space>', putBomb)
'''

verify()
start_game = time()
end_game = 0
winRoot.mainloop()
try:
    winRoot.destroy()
except:
    pass

try:
    f_out = open('score.txt', 'a', encoding='utf-8')
except:
    f_out = open('score.txt', 'w', encoding='utf-8')
f_out.write(name + ':' + str(int(end_game - start_game)) + ':' + str(SIZEMAP) + '\n')
f_out.close()
