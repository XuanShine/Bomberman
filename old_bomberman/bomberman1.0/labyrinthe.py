from random import randint

def listerCaseAutour(case, sizemap):
    """renvoie la liste les cases autour de la <case> selon un rapport de
    2 cases"""
    liste = [(case[0] + 2, case[1]), (case[0], case[1] + 2),
             (case[0] - 2, case[1]), (case[0], case[1] - 2)]
    res = liste[:]
    for case in liste:
        if (case[0] < 0 or case[1] < 0 or
            case[0] >= sizemap[0] or case[1] >= sizemap[1]):
            res.remove(case)
    return res

def cherchePossibilite(ens, oldEns, sizemap):
    """renvoie l'ensemble des cases où il est possible de supprimer
    parmis <ens>"""
    res = set()
    for case in ens - oldEns:
        if case[0] % 2 == 0 and case[1] % 2 == 0:
            caseAutour = listerCaseAutour(case, sizemap)
            addTo_oldEns = True
            for case2 in caseAutour:
                if case2 not in ens:
                    res.add(case2)
                    addTo_oldEns = False
            if addTo_oldEns:
                oldEns.add(case)
    return res, oldEns

def random(ens):
    """retourne un element au hasard parmis <ens>"""
    liste = [e for e in ens]
    return liste[randint(0, len(ens) - 1)]

def possibiliteDepart(delCase, ensDepart, sizemap):
    """retourne la case de depart (dans <ensDepart>) pour arriver à la case
    à supprimer <delCase>"""
    caseAutour = listerCaseAutour(delCase, sizemap)
    ensPossibleAutour = set()
    for case in caseAutour:
        if case in ensDepart:
            ensPossibleAutour.add(case)
    return random(ensPossibleAutour)

def genereMap(ensDepart, SIZEMAP):
    oldEns = set()
    ensPossibilite, oldEns = cherchePossibilite(ensDepart, oldEns, SIZEMAP)
    while ensPossibilite != set():
        delCase = random(ensPossibilite)
        depCase = possibiliteDepart(delCase, ensDepart, SIZEMAP)
        ensDepart.add(delCase)
        delCase2 = ((delCase[0] - depCase[0]) / 2 + depCase[0],
                    (delCase[1] - depCase[1]) / 2 + depCase[1])
        ensDepart.add(delCase2)
        ensPossibilite, oldEns = cherchePossibilite(ensDepart, oldEns, SIZEMAP)
    return ensDepart

if __name__ == '__main__':
    import tkinter as tk
    from time import time

    
    SIZEMAP = (51, 23)
    PAS = 20
    ensCaseVide = {(0, 0)}
    start = time()
    ensCaseVide = genereMap(ensCaseVide, SIZEMAP)
    end = time()
    print(end - start)
    #=> 6.54 / 6.50
    #=> 2.99 / 2.99
    #=> 0.73 / 0.68 / 0.72
    #=> 0.74 / 0.76 / 0.69 / 0.74

    winRoot = tk.Tk()

    canvasMap = tk.Canvas(winRoot, width=SIZEMAP[0] * PAS, height=SIZEMAP[1] * PAS,
                      bg='blue')
    canvasMap.pack()
    for case in ensCaseVide:
        canvasMap.create_rectangle(case[0] * PAS, case[1] * PAS,
                               case[0] * PAS + PAS, case[1] * PAS + PAS,
                               fill='dark grey', outline='dark grey')
    winRoot.mainloop()
