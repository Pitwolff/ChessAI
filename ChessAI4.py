import copy
import time
import numpy as np
import matplotlib.pyplot as plt

class Noeud:
    def __init__(self, noeud):
        self.noeud = noeud
        self.branches = []
        self.valeur = ""

    def fils(self, noeud):
        self.branches.append(Noeud(noeud))

class Piece:
    def __init__(self, x, y, couleur):
        self.x = x
        self.y = y
        self.coups_piece = []
        self.couleur = couleur
        self.defenseur = []
        self.attaquant = []
        self.attaque = []
        self.defendu = []
        self.coups_potentiels = []
        self.injouables = []
        self.mur = []
        self.valeur_piece = 0

class Pion(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)

    def valeur(self):
        if self.couleur == 0:
            self.valeur_piece = 0.5 + self.y ** 3 / 256 + (len(self.coups_piece) - len(self.injouables) - 1) / 16 + len(self.defenseur + self.attaquant * 2) / 64
            if len(self.defendu) != len(self.attaque):
                self.valeur_piece += ((len(self.defendu) - len(self.attaque)) / abs((len(self.defendu) - len(self.attaque)))) / (8 * (7 - self.y))
            if self.mur != [] and self.mur[0][0] == self.y - 1 and self.x != 3 and self.x != 4 and self.y == 1:
                self.valeur_piece += 0.375
        else:
            self.valeur_piece = 0.5 + (7 - self.y) ** 3 / 256 + (len(self.coups_piece) - len(self.injouables) - 1) / 16 + len(self.defenseur + self.attaquant * 2) / 64
            if len(self.defendu) != len(self.attaque):
                self.valeur_piece += ((len(self.defendu) - len(self.attaque)) / abs((len(self.defendu) - len(self.attaque)))) / (8 * self.y)
            if self.mur != [] and self.mur[0][0] == self.y + 1 and self.x != 3 and self.x != 4 and self.y == 6:
                self.valeur_piece += 0.375

    def coups(self, echequier):
        coups = []
        coups_potentiels = []
        attaquant = []
        defenseur = []
        if self.couleur == 0:
            if isinstance(echequier[self.x + (self.y + 1) * 8], list):
                coups.append((self.y + 1, self.x))
                if self.y == 1:
                    if isinstance(echequier[self.x + (self.y + 2) * 8], list):
                        coups.append((self.y + 2, self.x))
                    else:
                        coups_potentiels.append((self.y + 2, self.x))
            else:
                coups_potentiels.append((self.y + 1, self.x))
                if self.y == 1 and isinstance(echequier[self.x + (self.y + 2) * 8], list):
                    coups_potentiels.append((self.y + 2, self.x))
            if self.x > 0:
                if not isinstance(echequier[self.x - 1 + (self.y + 1) * 8], list) and echequier[self.x - 1 + (self.y + 1) * 8].couleur != self.couleur:
                    coups.append((self.y + 1, self.x - 1))
                    attaquant.append((self.y + 1, self.x - 1))
                    echequier[self.x - 1 + (self.y + 1) * 8].attaque.append((self.y, self.x))
                elif isinstance(echequier[self.x - 1 + (self.y + 1) * 8], list):
                    echequier[self.x - 1 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
                    coups_potentiels.append((self.y + 1, self.x - 1))
                else:
                    defenseur.append((self.y + 1, self.x - 1))
                    echequier[self.x - 1 + (self.y + 1) * 8].defendu.append((self.y, self.x))
            if self.x < 7:
                if not isinstance(echequier[self.x + 1 + (self.y + 1) * 8], list) and echequier[self.x + 1 + (self.y + 1) * 8].couleur != self.couleur:
                    coups.append((self.y + 1, self.x + 1))
                    attaquant.append((self.y + 1, self.x + 1))
                    echequier[self.x + 1 + (self.y + 1) * 8].attaque.append((self.y, self.x))
                elif isinstance(echequier[self.x + 1 + (self.y + 1) * 8], list):
                    echequier[self.x + 1 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
                    coups_potentiels.append((self.y + 1, self.x + 1))
                else:
                    defenseur.append((self.y + 1, self.x + 1))
                    echequier[self.x + 1 + (self.y + 1) * 8].defendu.append((self.y, self.x))
        else:
            if isinstance(echequier[self.x + (self.y - 1) * 8], list):
                coups.append((self.y - 1, self.x))
                if self.y == 6:
                    if type(echequier[self.x + (self.y - 2) * 8]) == list:
                        coups.append((self.y - 2, self.x))
                    else:
                        coups_potentiels.append((self.y - 2, self.x))
            else:
                coups_potentiels.append((self.y - 1, self.x))
                if self.y == 6 and isinstance(echequier[self.x + (self.y - 2) * 8], list):
                    coups_potentiels.append((self.y - 2, self.x))
            if self.x > 0:
                if not isinstance(echequier[self.x - 1 + (self.y - 1) * 8], list) and echequier[self.x - 1 + (self.y - 1) * 8].couleur != self.couleur:
                    coups.append((self.y - 1, self.x - 1))
                    attaquant.append((self.y - 1, self.x - 1))
                    echequier[self.x - 1 + (self.y - 1) * 8].attaque.append((self.y, self.x))
                elif isinstance(echequier[self.x - 1 + (self.y - 1) * 8], list):
                    echequier[self.x - 1 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
                    coups_potentiels.append((self.y - 1, self.x - 1))
                else:
                    defenseur.append((self.y - 1, self.x - 1))
                    echequier[self.x - 1 + (self.y - 1) * 8].defendu.append((self.y, self.x))
            if self.x < 7:
                if not isinstance(echequier[self.x + 1 + (self.y - 1) * 8], list) and echequier[self.x + 1 + (self.y - 1) * 8].couleur != self.couleur:
                    coups.append((self.y - 1, self.x + 1))
                    attaquant.append((self.y - 1, self.x + 1))
                    echequier[self.x + 1 + (self.y - 1) * 8].attaque.append((self.y, self.x))
                elif isinstance(echequier[self.x + 1 + (self.y - 1) * 8], list):
                    echequier[self.x + 1 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
                    coups_potentiels.append((self.y - 1, self.x + 1))
                else:
                    defenseur.append((self.y - 1, self.x + 1))
                    echequier[self.x + 1 + (self.y - 1) * 8].defendu.append((self.y, self.x))
        self.coups_piece = coups
        self.coups_potentiels = coups_potentiels
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        self.injouables = []
        coups_bonus = [0, 0, 0, 0]
        if self.mur != []:
            if self.couleur == 0 and self.y == 4:
                if self.x > 0 and informations[self.x - 1] == 1:
                    self.coups_piece.append((self, self.y + 1, self.x - 1, self.y, self.x))
                    coups_bonus[0] = 1
                if self.x < 7 and informations[self.x + 1] == 1:
                    self.coups_piece.append((self, self.y + 1, self.x + 1, self.y, self.x))
                    coups_bonus[1] = 1
            elif self.couleur == 1 and self.y == 3:
                if self.x > 0 and informations[8 + self.x - 1] == 1:
                    self.coups_piece.append((self, self.y - 1, self.x - 1, self.y, self.x))
                    coups_bonus[2] = 1
                if self.x < 7 and informations[8 + self.x + 1] == 1:
                    self.coups_piece.append((self, self.y - 1, self.x + 1, self.y, self.x))
                    coups_bonus[3] = 1
            for elt in self.attaque:
                if isinstance(echequier[elt[1] + elt[0] * 8], Fou):
                    if self.mur[0][1] - self.x != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.x - elt2[1]) == 0 or (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Tour):
                    if self.mur[0][1] == self.x == elt[1]:
                        self.injouables = self.coups_piece
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Dame):
                    if self.mur[0][1] == self.x == elt[1]:
                        self.injouables = self.coups_piece
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt)
                        break
                    elif self.mur[0][1] - self.x != 0 and self.x - elt[1] != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.x - elt2[1]) == 0 or (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break
            if coups_bonus[0] == 1:
                self.coups_piece.remove((self, self.y + 1, self.x - 1, self.y, self.x))
            elif coups_bonus[1] == 1:
                self.coups_piece.remove((self, self.y + 1, self.x + 1, self.y, self.x))
            elif coups_bonus[2] == 1:
                self.coups_piece.remove((self, self.y - 1, self.x - 1, self.y, self.x))
            elif coups_bonus[3] == 1:
                self.coups_piece.remove((self, self.y - 1, self.x + 1, self.y, self.x))


class Cavalier(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)

    def valeur(self):
        self.valeur_piece = (2.5 + (len(self.coups_piece) - len(self.injouables)) / 64) * (1 + (len(self.defenseur + self.attaquant * 8 + self.defendu) / 64 - len(self.attaque) / 8))

    def coups(self, echequier):
        coups = []
        attaquant = []
        defenseur = []
        injouable = []
        if self.y > 1 and self.x > 0:
            if isinstance(echequier[self.x - 1 + (self.y - 2) * 8], list):
                coups.append((self.y - 2, self.x - 1))
                echequier[self.x - 1 + (self.y - 2) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x - 1 + (self.y - 2) * 8].couleur != self.couleur:
                coups.append((self.y - 2, self.x - 1))
                attaquant.append((self.y - 2, self.x - 1))
                echequier[self.x - 1 + (self.y - 2) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y - 2, self.x - 1))
                echequier[self.x - 1 + (self.y - 2) * 8].defendu.append((self.y, self.x))
        if self.y > 1 and self.x < 7:
            if isinstance(echequier[self.x + 1 + (self.y - 2) * 8], list):
                coups.append((self.y - 2, self.x + 1))
                echequier[self.x + 1 + (self.y - 2) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x + 1 + (self.y - 2) * 8].couleur != self.couleur:
                coups.append((self.y - 2, self.x + 1))
                attaquant.append((self.y - 2, self.x + 1))
                echequier[self.x + 1 + (self.y - 2) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y - 2, self.x + 1))
                echequier[self.x + 1 + (self.y - 2) * 8].defendu.append((self.y, self.x))
        if self.y > 0 and self.x > 1:
            if isinstance(echequier[self.x - 2 + (self.y - 1) * 8], list):
                coups.append((self.y - 1, self.x - 2))
                echequier[self.x - 2 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x - 2 + (self.y - 1) * 8].couleur != self.couleur:
                coups.append((self.y - 1, self.x - 2))
                attaquant.append((self.y - 1, self.x - 2))
                echequier[self.x - 2 + (self.y - 1) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y - 1, self.x - 2))
                echequier[self.x - 2 + (self.y - 1) * 8].defendu.append((self.y, self.x))
        if self.y > 0 and self.x < 6:
            if isinstance(echequier[self.x + 2 + (self.y - 1) * 8], list):
                coups.append((self.y - 1, self.x + 2))
                echequier[self.x + 2 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x + 2 + (self.y - 1) * 8].couleur != self.couleur:
                coups.append((self.y - 1, self.x + 2))
                attaquant.append((self.y - 1, self.x + 2))
                echequier[self.x + 2 + (self.y - 1) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y - 1, self.x + 2))
                echequier[self.x + 2 + (self.y - 1) * 8].defendu.append((self.y, self.x))
        if self.y < 7 and self.x > 1:
            if isinstance(echequier[self.x - 2 + (self.y + 1) * 8], list):
                coups.append((self.y + 1, self.x - 2))
                echequier[self.x - 2 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x - 2 + (self.y + 1) * 8].couleur != self.couleur:
                coups.append((self.y + 1, self.x - 2))
                attaquant.append((self.y + 1, self.x - 2))
                echequier[self.x - 2 + (self.y + 1) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y + 1, self.x - 2))
                echequier[self.x - 2 + (self.y + 1) * 8].defendu.append((self.y, self.x))
        if self.y < 7 and self.x < 6:
            if isinstance(echequier[self.x + 2 + (self.y + 1) * 8], list):
                coups.append((self.y + 1, self.x + 2))
                echequier[self.x + 2 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x + 2 + (self.y + 1) * 8].couleur != self.couleur:
                coups.append((self.y + 1, self.x + 2))
                attaquant.append((self.y + 1, self.x + 2))
                echequier[self.x + 2 + (self.y + 1) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y + 1, self.x + 2))
                echequier[self.x + 2 + (self.y + 1) * 8].defendu.append((self.y, self.x))
        if self.y < 6 and self.x > 0:
            if isinstance(echequier[self.x - 1 + (self.y + 2) * 8], list):
                coups.append((self.y + 2, self.x - 1))
                echequier[self.x - 1 + (self.y + 2) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x - 1 + (self.y + 2) * 8].couleur != self.couleur:
                coups.append((self.y + 2, self.x - 1))
                attaquant.append((self.y + 2, self.x - 1))
                echequier[self.x - 1 + (self.y + 2) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y + 2, self.x - 1))
                echequier[self.x - 1 + (self.y + 2) * 8].defendu.append((self.y, self.x))
        if self.y < 6 and self.x < 7:
            if isinstance(echequier[self.x + 1 + (self.y + 2) * 8], list):
                coups.append((self.y + 2, self.x + 1))
                echequier[self.x + 1 + (self.y + 2) * 8][self.couleur].append((self.y, self.x))
            elif echequier[self.x + 1 + (self.y + 2) * 8].couleur != self.couleur:
                coups.append((self.y + 2, self.x + 1))
                attaquant.append((self.y + 2, self.x + 1))
                echequier[self.x + 1 + (self.y + 2) * 8].attaque.append((self.y, self.x))
            else:
                defenseur.append((self.y + 2, self.x + 1))
                echequier[self.x + 1 + (self.y + 2) * 8].defendu.append((self.y, self.x))
        self.coups_piece = coups
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        self.injouables = []
        if self.mur != []:
            for elt in self.attaque:
                if isinstance(echequier[elt[1] + elt[0] * 8], Fou):
                    if self.mur[0][1] - self.x != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        self.injouables = self.coups_piece
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Tour):
                    if self.mur[0][1] == self.x == elt[1] or self.mur[0][0] == self.y == elt[0]:
                        self.injouables = self.coups_piece
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Dame):
                    if self.mur[0][1] == self.x == elt[1] or self.mur[0][0] == self.y == elt[0]:
                        self.injouables = self.coups_piece
                        break
                    elif self.mur[0][1] - self.x != 0 and (self.x - elt[1]) != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        self.injouables = self.coups_piece
                        break

class Fou(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)
        self.coups1 = []
        self.coups2 = []
        self.coups3 = []
        self.coups4 = []

    def valeur(self):
        self.valeur_piece = 2 + (len(self.coups_piece) - len(self.injouables)) / 16 + len(self.defenseur + self.attaquant + self.defendu) / 16 - len(self.attaque) / 8

    def coups(self, echequier):
        coups1 = []
        coups2 = []
        coups3 = []
        coups4 = []
        attaquant = []
        defenseur = []
        n = 1
        while self.y - n >= 0 and self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y - n) * 8], list) or echequier[self.x - n + (self.y - n) * 8].couleur != self.couleur):
            coups1.append((self.y - n, self.x - n))
            if isinstance(echequier[self.x - n + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x - n))
                echequier[self.x - n + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x - n + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0 and self.x - n >= 0:
            defenseur.append((self.y - n, self.x - n))
            echequier[self.x - n + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7 and self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y + n) * 8], list) or echequier[self.x - n + (self.y + n) * 8].couleur != self.couleur):
            coups2.append((self.y + n, self.x - n))
            if isinstance(echequier[self.x - n + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x - n))
                echequier[self.x - n + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x - n + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7 and self.x - n >= 0:
            defenseur.append((self.y + n, self.x - n))
            echequier[self.x - n + (self.y + n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y - n >= 0 and self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y - n) * 8], list) or echequier[self.x + n + (self.y - n) * 8].couleur != self.couleur):
            coups3.append((self.y - n, self.x + n))
            if isinstance(echequier[self.x + n + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x + n))
                echequier[self.x + n + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x + n + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0 and self.x + n <= 7:
            defenseur.append((self.y - n, self.x + n))
            echequier[self.x + n + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7 and self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y + n) * 8], list) or echequier[self.x + n + (self.y + n) * 8].couleur != self.couleur):
            coups4.append((self.y + n, self.x + n))
            if isinstance(echequier[self.x + n + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x + n))
                echequier[self.x + n + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x + n + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7 and self.x + n <= 7:
            defenseur.append((self.y + n, self.x + n))
            echequier[self.x + n + (self.y + n) * 8].defendu.append((self.y, self.x))
        self.coups1 = coups1
        self.coups2 = coups2
        self.coups3 = coups3
        self.coups4 = coups4
        self.coups_piece = coups1 + coups2 + coups3 + coups4
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        self.injouables = []
        if self.mur != []:
            for elt in self.attaque:
                if isinstance(echequier[elt[1] + elt[0] * 8], Fou):
                    if self.mur[0][1] - self.x != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Tour):
                    if self.mur[0][1] == self.x == elt[1] or self.mur[0][0] == self.y == elt[0]:
                        self.injouables = self.coups_piece
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Dame):
                    if self.mur[0][1] == self.x == elt[1] or self.mur[0][0] == self.y == elt[0]:
                        self.injouables = self.coups_piece
                        break
                    elif self.mur[0][1] - self.x != 0 and (self.x - elt[1]) != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break



class Tour(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)
        self.coups5 = []
        self.coups6 = []
        self.coups7 = []
        self.coups8 = []
    def valeur(self):
        self.valeur_piece = 4 + (len(self.coups_piece) - len(self.injouables)) / 16 + len(self.defenseur + self.attaquant + self.defendu) / 16 - len(self.attaque) / 8

    def coups(self, echequier):
        coups5 = []
        coups6 = []
        coups7 = []
        coups8 = []
        attaquant = []
        defenseur = []
        n = 1
        while self.y - n >= 0  and (isinstance(echequier[self.x + (self.y - n) * 8], list) or echequier[self.x + (self.y - n) * 8].couleur != self.couleur):
            coups5.append((self.y - n, self.x))
            if isinstance(echequier[self.x + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x))
                echequier[self.x + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0:
            defenseur.append((self.y - n, self.x))
            echequier[self.x + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7  and (isinstance(echequier[self.x + (self.y + n) * 8], list) or echequier[self.x + (self.y + n) * 8].couleur != self.couleur):
            coups6.append((self.y + n, self.x))
            if isinstance(echequier[self.x + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x))
                echequier[self.x + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7:
            defenseur.append((self.y + n, self.x))
            echequier[self.x + (self.y + n) * 8].defendu.append((self.y, self.x))
        n = 1
        while  self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y) * 8], list) or echequier[self.x - n + (self.y) * 8].couleur != self.couleur):
            coups7.append((self.y, self.x - n))
            if isinstance(echequier[self.x - n + (self.y) * 8], Piece):
                attaquant.append((self.y, self.x - n))
                echequier[self.x - n + (self.y) * 8].attaque.append((self.y, self.x))
                n = self.x + 1
            else:
                echequier[self.x - n + (self.y) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.x - n >= 0:
            defenseur.append((self.y, self.x - n))
            echequier[self.x - n + (self.y) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y) * 8], list) or echequier[self.x + n + (self.y) * 8].couleur != self.couleur):
            coups8.append((self.y, self.x + n))
            if isinstance(echequier[self.x + n + (self.y) * 8], Piece):
                attaquant.append((self.y, self.x + n))
                echequier[self.x + n + (self.y) * 8].attaque.append((self.y, self.x))
                n = 8 - self.x
            else:
                echequier[self.x + n + (self.y) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.x + n <= 7:
            defenseur.append((self.y, self.x + n))
            echequier[self.x + n + (self.y) * 8].defendu.append((self.y, self.x))
        self.coups5 = coups5
        self.coups6 = coups6
        self.coups7 = coups7
        self.coups8 = coups8
        self.coups_piece = coups5 + coups6 + coups7 + coups8
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        self.injouables = []
        if self.mur != []:
            for elt in self.attaque:
                if isinstance(echequier[elt[1] + elt[0] * 8], Fou):
                    if self.mur[0][1] - self.x != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        self.injouables = self.coups_piece
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Tour):
                    if self.mur[0][1] == self.x == elt[1]:
                        for elt2 in self.coups_piece:
                            if elt2[1] != self.x:
                                self.injouables.append(elt2)
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Dame):
                    if self.mur[0][1] - self.x != 0 and (self.x - elt[1]) != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        self.injouables = self.coups_piece
                        break
                    elif self.mur[0][1] == self.x == elt[1]:
                        for elt2 in self.coups_piece:
                            if elt2[1] != self.x:
                                self.injouables.append(elt2)
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt2)
                        break

class Dame(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)
        self.coups1 = []
        self.coups2 = []
        self.coups3 = []
        self.coups4 = []
        self.coups5 = []
        self.coups6 = []
        self.coups7 = []
        self.coups8 = []

    def valeur(self):
        self.valeur_piece = 8.5 + (len(self.coups_piece) - len(self.injouables)) / 64 + len(self.defenseur + self.attaquant + self.defendu) / 128 - len(self.attaque) / 16

    def coups(self, echequier):
        coups1 = []
        coups2 = []
        coups3 = []
        coups4 = []
        coups5 = []
        coups6 = []
        coups7 = []
        coups8 = []
        attaquant = []
        defenseur = []
        n = 1
        while self.y - n >= 0 and self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y - n) * 8], list) or echequier[self.x - n + (self.y - n) * 8].couleur != self.couleur):
            coups1.append((self.y - n, self.x - n))
            if isinstance(echequier[self.x - n + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x - n))
                echequier[self.x - n + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x - n + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0 and self.x - n >= 0:
            defenseur.append((self.y - n, self.x - n))
            echequier[self.x - n + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7 and self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y + n) * 8], list) or echequier[self.x - n + (self.y + n) * 8].couleur != self.couleur):
            coups2.append((self.y + n, self.x - n))
            if isinstance(echequier[self.x - n + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x - n))
                echequier[self.x - n + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x - n + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7 and self.x - n >= 0:
            defenseur.append((self.y + n, self.x - n))
            echequier[self.x - n + (self.y + n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y - n >= 0 and self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y - n) * 8], list) or echequier[self.x + n + (self.y - n) * 8].couleur != self.couleur):
            coups3.append((self.y - n, self.x + n))
            if isinstance(echequier[self.x + n + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x + n))
                echequier[self.x + n + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x + n + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0 and self.x + n <= 7:
            defenseur.append((self.y - n, self.x + n))
            echequier[self.x + n + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7 and self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y + n) * 8], list) or echequier[self.x + n + (self.y + n) * 8].couleur != self.couleur):
            coups4.append((self.y + n, self.x + n))
            if isinstance(echequier[self.x + n + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x + n))
                echequier[self.x + n + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x + n + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7 and self.x + n <= 7:
            defenseur.append((self.y + n, self.x + n))
            echequier[self.x + n + (self.y + n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y - n >= 0  and (isinstance(echequier[self.x + (self.y - n) * 8], list) or echequier[self.x + (self.y - n) * 8].couleur != self.couleur):
            coups5.append((self.y - n, self.x))
            if isinstance(echequier[self.x + (self.y - n) * 8], Piece):
                attaquant.append((self.y - n, self.x))
                echequier[self.x + (self.y - n) * 8].attaque.append((self.y, self.x))
                n = self.y + 1
            else:
                echequier[self.x + (self.y - n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y - n >= 0:
            defenseur.append((self.y - n, self.x))
            echequier[self.x + (self.y - n) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.y + n <= 7  and (isinstance(echequier[self.x + (self.y + n) * 8], list) or echequier[self.x + (self.y + n) * 8].couleur != self.couleur):
            coups6.append((self.y + n, self.x))
            if isinstance(echequier[self.x + (self.y + n) * 8], Piece):
                attaquant.append((self.y + n, self.x))
                echequier[self.x + (self.y + n) * 8].attaque.append((self.y, self.x))
                n = 8 - self.y
            else:
                echequier[self.x + (self.y + n) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.y + n <= 7:
            defenseur.append((self.y + n, self.x))
            echequier[self.x + (self.y + n) * 8].defendu.append((self.y, self.x))
        n = 1
        while  self.x - n >= 0 and (isinstance(echequier[self.x - n + (self.y) * 8], list) or echequier[self.x - n + (self.y) * 8].couleur != self.couleur):
            coups7.append((self.y, self.x - n))
            if isinstance(echequier[self.x - n + (self.y) * 8], Piece):
                attaquant.append((self.y, self.x - n))
                echequier[self.x - n + (self.y) * 8].attaque.append((self.y, self.x))
                n = self.x + 1
            else:
                echequier[self.x - n + (self.y) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.x - n >= 0:
            defenseur.append((self.y, self.x - n))
            echequier[self.x - n + (self.y) * 8].defendu.append((self.y, self.x))
        n = 1
        while self.x + n <= 7 and (isinstance(echequier[self.x + n + (self.y) * 8], list) or echequier[self.x + n + (self.y) * 8].couleur != self.couleur):
            coups8.append((self.y, self.x + n))
            if isinstance(echequier[self.x + n + (self.y) * 8], Piece):
                attaquant.append((self.y, self.x + n))
                echequier[self.x + n + (self.y) * 8].attaque.append((self.y, self.x))
                n = 8 - self.x
            else:
                echequier[self.x + n + (self.y) * 8][self.couleur].append((self.y, self.x))
            n += 1
        if self.x + n <= 7:
            defenseur.append((self.y, self.x + n))
            echequier[self.x + n + (self.y) * 8].defendu.append((self.y, self.x))
        self.coups1 = coups1
        self.coups2 = coups2
        self.coups3 = coups3
        self.coups4 = coups4
        self.coups5 = coups5
        self.coups6 = coups6
        self.coups7 = coups7
        self.coups8 = coups8
        self.coups_piece = coups1 + coups2 + coups3 + coups4 + coups5 + coups6 + coups7 + coups8
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        self.injouables = []
        if self.mur != []:
            for elt in self.attaque:
                if isinstance(echequier[elt[1] + elt[0] * 8], Fou):
                    if self.mur[0][1] - self.x != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.x - elt2[1]) == 0 or (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Tour):
                    if self.mur[0][1] == self.x == elt[1]:
                        for elt2 in self.coups_piece:
                            if elt2[1] != self.x:
                                self.injouables.append(elt2)
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt2)
                        break
                elif isinstance(echequier[elt[1] + elt[0] * 8], Dame):
                    if self.mur[0][1] - self.x != 0 and self.x - elt[1] != 0 and (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) == (self.y - elt[0]) / (self.x - elt[1]):
                        for elt2 in self.coups_piece:
                            if (self.x - elt2[1]) == 0 or (self.mur[0][0] - self.y) / (self.mur[0][1] - self.x) != (self.y - elt2[0]) / (self.x - elt2[1]):
                                self.injouables.append(elt2)
                        break
                    elif self.mur[0][1] == self.x == elt[1]:
                        for elt2 in self.coups_piece:
                            if elt2[1] != self.x:
                                self.injouables.append(elt2)
                        break
                    elif self.mur[0][0] == self.y == elt[0]:
                        for elt2 in self.coups_piece:
                            if elt2[0] != self.y:
                                self.injouables.append(elt2)
                        break

class Roi(Piece):
    def __init__(self, x, y, couleur):
        Piece.__init__(self, x, y, couleur)

    def valeur(self):
        self.valeur_piece = 1 - len(self.injouables) / 16 + len(self.defenseur + self.attaquant) / 32 - len(self.attaque) / 4 + 100

    def coups(self, echequier):
        coups = []
        attaquant = []
        defenseur = []
        if self.y > 0 and self.x > 0:
            if isinstance(echequier[self.x - 1 + (self.y - 1) * 8], list):
                echequier[self.x - 1 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y - 1, self.x - 1))
            else:
                if echequier[self.x - 1 + (self.y - 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y - 1, self.x - 1))
                    echequier[self.x - 1 + (self.y - 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y - 1, self.x - 1))
                else:
                    defenseur.append((self.y - 1, self.x - 1))
                    echequier[self.x - 1 + (self.y - 1) * 8].defendu.append((self.y, self.x))
        if self.x > 0:
            if isinstance(echequier[self.x - 1 + (self.y) * 8], list):
                echequier[self.x - 1 + (self.y) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y, self.x - 1))
            else:
                if echequier[self.x - 1 + (self.y) * 8].couleur != self.couleur:
                    attaquant.append((self.y, self.x - 1))
                    echequier[self.x - 1 + (self.y) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y, self.x - 1))
                else:
                    defenseur.append((self.y, self.x - 1))
                    echequier[self.x - 1 + (self.y) * 8].defendu.append((self.y, self.x))
        if self.y < 7 and self.x > 0:
            if isinstance(echequier[self.x - 1 + (self.y + 1) * 8], list):
                echequier[self.x - 1 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y + 1, self.x - 1))
            else:
                if echequier[self.x - 1 + (self.y + 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y + 1, self.x - 1))
                    echequier[self.x - 1 + (self.y + 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y + 1, self.x - 1))
                else:
                    defenseur.append((self.y + 1, self.x - 1))
                    echequier[self.x - 1 + (self.y + 1) * 8].defendu.append((self.y, self.x))
        if self.y < 7:
            if isinstance(echequier[self.x + (self.y + 1) * 8], list):
                echequier[self.x + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y + 1, self.x))
            else:
                if echequier[self.x + (self.y + 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y + 1, self.x))
                    echequier[self.x + (self.y + 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y + 1, self.x))
                else:
                    defenseur.append((self.y + 1, self.x))
                    echequier[self.x + (self.y + 1) * 8].defendu.append((self.y, self.x))
        if self.y < 7 and self.x < 7:
            if isinstance(echequier[self.x + 1 + (self.y + 1) * 8], list):
                echequier[self.x + 1 + (self.y + 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y + 1, self.x + 1))
            else:
                if echequier[self.x + 1 + (self.y + 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y + 1, self.x + 1))
                    echequier[self.x + 1 + (self.y + 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y + 1, self.x + 1))
                else:
                    defenseur.append((self.y + 1, self.x + 1))
                    echequier[self.x + 1 + (self.y + 1) * 8].defendu.append((self.y, self.x))
        if self.x < 7:
            if isinstance(echequier[self.x + 1 + (self.y) * 8], list):
                echequier[self.x + 1 + (self.y) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y, self.x + 1))
            else:
                if echequier[self.x + 1 + (self.y) * 8].couleur != self.couleur:
                    attaquant.append((self.y, self.x + 1))
                    echequier[self.x + 1 + (self.y) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y, self.x + 1))
                else:
                    defenseur.append((self.y, self.x + 1))
                    echequier[self.x + 1 + (self.y) * 8].defendu.append((self.y, self.x))
        if self.y > 0 and self.x < 7:
            if isinstance(echequier[self.x + 1 + (self.y - 1) * 8], list):
                echequier[self.x + 1 + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y - 1, self.x + 1))
            else:
                if echequier[self.x + 1 + (self.y - 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y - 1, self.x + 1))
                    echequier[self.x + 1 + (self.y - 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y - 1, self.x + 1))
                else:
                    defenseur.append((self.y - 1, self.x + 1))
                    echequier[self.x + 1 + (self.y - 1) * 8].defendu.append((self.y, self.x))
        if self.y > 0:
            if isinstance(echequier[self.x + (self.y - 1) * 8], list):
                echequier[self.x + (self.y - 1) * 8][self.couleur].append((self.y, self.x))
                coups.append((self.y - 1, self.x))
            else:
                if echequier[self.x + (self.y - 1) * 8].couleur != self.couleur:
                    attaquant.append((self.y - 1, self.x))
                    echequier[self.x + (self.y - 1) * 8].attaque.append((self.y, self.x))
                    coups.append((self.y - 1, self.x))
                else:
                    defenseur.append((self.y - 1, self.x))
                    echequier[self.x + (self.y - 1) * 8].defendu.append((self.y, self.x))
        self.coups_piece = coups
        self.attaquant = attaquant
        self.defenseur = defenseur

    def injouable(self, echequier, informations):
        injouables = []
        for elt in self.coups_piece:
            match elt:
                case elt if isinstance(echequier[elt[1] + elt[0] * 8], list):
                    if echequier[elt[1] + elt[0] * 8][abs(self.couleur - 1)] != []:
                        injouables.append(elt)
                case _:
                    if echequier[elt[1] + elt[0] * 8].couleur != self.couleur and echequier[elt[1] + elt[0] * 8].defendu != []:
                        injouables.append(elt)
        self.injouables = injouables

    def muraille(self, echequier, informations):
        mur = []
        n = 1
        while self.y - n > 0 and self.x - n > 0:
            if isinstance(echequier[self.x - n + (self.y - n) * 8], Piece):
                if echequier[self.x - n + (self.y - n) * 8].couleur == self.couleur:
                    mur.append((self.y - n, self.x - n))
                    echequier[self.x - n + (self.y - n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.x - n > 0:
            if isinstance(echequier[self.x - n + (self.y) * 8], Piece):
                if echequier[self.x - n + (self.y) * 8].couleur == self.couleur:
                    mur.append((self.y, self.x - n))
                    echequier[self.x - n + (self.y) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.y + n < 7 and self.x - n > 0:
            if isinstance(echequier[self.x - n + (self.y + n) * 8], Piece):
                if echequier[self.x - n + (self.y + n) * 8].couleur == self.couleur:
                    mur.append((self.y + n, self.x - n))
                    echequier[self.x - n + (self.y + n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.y + n < 7:
            if isinstance(echequier[self.x + (self.y + n) * 8], Piece):
                if echequier[self.x + (self.y + n) * 8].couleur == self.couleur:
                    mur.append((self.y + n, self.x))
                    echequier[self.x + (self.y + n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.y + n < 7 and self.x + n < 7:
            if isinstance(echequier[self.x + n + (self.y + n) * 8], Piece):
                if echequier[self.x + n + (self.y + n) * 8].couleur == self.couleur:
                    mur.append((self.y + n, self.x + n))
                    echequier[self.x + n + (self.y + n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.x + n < 7:
            if isinstance(echequier[self.x + n + (self.y) * 8], Piece):
                if echequier[self.x + n + (self.y) * 8].couleur == self.couleur:
                    mur.append((self.y, self.x + n))
                    echequier[self.x + n + (self.y) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.y - n > 0 and self.x + n < 7:
            if isinstance(echequier[self.x + n + (self.y - n) * 8], Piece):
                if echequier[self.x + n + (self.y - n) * 8].couleur == self.couleur:
                    mur.append((self.y - n, self.x + n))
                    echequier[self.x + n + (self.y - n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        n = 1
        while self.y - n > 0:
            if isinstance(echequier[self.x + (self.y - n) * 8], Piece):
                if echequier[self.x + (self.y - n) * 8].couleur == self.couleur:
                    mur.append((self.y - n, self.x))
                    echequier[self.x + (self.y - n) * 8].mur.append((self.y, self.x))
                break
            n += 1
        self.mur = mur
        for elt in self.mur:
            echequier[elt[1] + elt[0] * 8].injouable(echequier, informations)

def coups_b(echequier, informations, vitesse):
    coups_bl = []
    for elt in echequier:
        if isinstance(elt, Piece):
            if elt.couleur == 0:
                if isinstance(elt, Roi):
                    roi = elt
                    if elt.attaque != []:
                        echec = 1
                    else:
                        echec = 0
                        if informations[16] == 1:
                            if (isinstance(echequier[elt.x - 1 + (elt.y) * 8], list) and echequier[elt.x - 1 + (elt.y) * 8][1] == []) and (isinstance(echequier[elt.x - 2 + (elt.y) * 8], list) and echequier[elt.x - 2 + (elt.y) * 8][1] == []) and (isinstance(echequier[elt.x - 3 + (elt.y) * 8], list) and echequier[elt.x - 3 + (elt.y) * 8][1] == []):
                                coups_bl.append(((elt, 0, 2, 0, 4), (echequier[0], 0, 3, 0, 0)))
                        if informations[17] == 1:
                            if (isinstance(echequier[elt.x + 1 + (elt.y) * 8], list) and echequier[elt.x + 1 + (elt.y) * 8][1] == []) and (isinstance(echequier[elt.x + 2 + (elt.y) * 8], list) and echequier[elt.x + 2 + (elt.y) * 8][1] == []):
                                coups_bl.append(((elt, 0, 6, 0, 4), (echequier[7], 0, 5, 0, 7)))
                if vitesse == "lent":
                    elt.coups(echequier)
                if isinstance(elt, Pion) and elt.y == 4:
                    if elt.x > 0 and informations[8 + elt.x - 1] == 1 and (5, elt.x - 1) not in elt.injouables and (5, elt.x - 1) not in elt.coups_piece:
                        coups_bl.append(((echequier[elt.x - 1 + 4 * 8], 5, elt.x - 1, 4, elt.x - 1), (elt, 5, elt.x - 1, 4, elt.x)))
                    if elt.x < 7 and informations[8 + elt.x + 1] == 1 and (5, elt.x + 1) not in elt.injouables and (5, elt.x + 1) not in elt.coups_piece:
                        coups_bl.append(((echequier[elt.x + 1 + 4 * 8], 5, elt.x + 1, 4, elt.x + 1), (elt, 5, elt.x + 1, 4, elt.x)))
                for coup in elt.coups_piece:
                    if coup not in elt.injouables:
                        if not isinstance(elt, Pion) or coup[0] != 7:
                            coups_bl.append((elt, coup[0], coup[1], elt.y, elt.x))
                        else:
                            coups_bl.append((elt, coup[0], coup[1], elt.y, elt.x, Dame(coup[1], 7, 0)))
                            coups_bl.append((elt, coup[0], coup[1], elt.y, elt.x, Tour(coup[1], 7, 0)))
                            coups_bl.append((elt, coup[0], coup[1], elt.y, elt.x, Cavalier(coup[1], 7, 0)))
                            coups_bl.append((elt, coup[0], coup[1], elt.y, elt.x, Fou(coup[1], 7, 0)))
    if echec == 1:
        coups_blancs = []
        for elt in coups_bl:
            cle2 = cle_virtuelle(cle(echequier), elt)
            infos3 = copy.deepcopy(informations)
            r = recherche(cle2, 1)
            if not r[0]:
                chessboard3 = copie_echequier(echequier)
                roi2 = chessboard3[echequier.index(roi)]
                if len(elt) == 5:
                    elt2 = (chessboard3[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4])
                elif len(elt) == 2:
                    elt2 = ((chessboard3[echequier.index(elt[0][0])], elt[0][1], elt[0][2], elt[0][3], elt[0][4]), (chessboard3[echequier.index(elt[1][0])], elt[1][1], elt[1][2], elt[1][3], elt[1][4]))
                else:
                    elt2 = (chessboard3[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4], elt[5])
                chessboard3, infos3 = echequier_virtuel(chessboard3, elt2, infos3)
                if roi2.attaque == []:
                    evaluation = analyse(chessboard3, 1, "lent")
                    #evaluation = analyse2(chessboard3, 1, W[0], W[1], W[2], W[3], W[4], W[5], W[6], W[7], W[8], W[9], W[10], W[11], W[12], W[13])
                    inserer(cle2, (evaluation, chessboard3), 1)
                    coups_blancs.append(elt)
            else:
                if (not isinstance(elt[0], Roi) and r[1][1][echequier.index(roi)].attaque == []) or (isinstance(elt[0], Roi) and r[1][1][elt[2] + elt[1] * 8].attaque == []):
                    coups_blancs.append(elt)
        coups_bl = coups_blancs
    return coups_bl

def coups_n(echequier, informations, vitesse):
    coups_no = []
    for elt in echequier:
        if isinstance(elt, Piece):
            if elt.couleur == 1:
                if isinstance(elt, Roi):
                    roi = elt
                    if elt.attaque != []:
                        echec = 1
                    else:
                        echec = 0
                        if informations[18] == 1:
                            if (isinstance(echequier[elt.x - 1 + (elt.y) * 8], list) and echequier[elt.x - 1 + (elt.y) * 8][0] == []) and (isinstance(echequier[elt.x - 2 + (elt.y) * 8], list) and echequier[elt.x - 2 + (elt.y) * 8][0] == []) and (isinstance(echequier[elt.x - 3 + (elt.y) * 8], list) and echequier[elt.x - 3 + (elt.y) * 8][0] == []):
                                coups_no.append(((elt, 7, 2, 7, 4), (echequier[56], 7, 3, 7, 0)))
                        if informations[19] == 1:
                            if (isinstance(echequier[elt.x + 1 + (elt.y) * 8], list) and echequier[elt.x + 1 + (elt.y) * 8][0] == []) and (isinstance(echequier[elt.x + 2 + (elt.y) * 8], list) and echequier[elt.x + 2 + (elt.y) * 8][0] == []):
                                coups_no.append(((elt, 7, 6, 7, 4), (echequier[63], 7, 5, 7, 7)))
                if vitesse == "lent":
                    elt.coups(echequier)
                if isinstance(elt, Pion) and elt.y == 3:
                    if elt.x > 0 and informations[elt.x - 1] == 1 and (2, elt.x - 1) not in elt.injouables and (2, elt.x - 1) not in elt.coups_piece:
                        coups_no.append(((echequier[elt.x - 1 + 3 * 8], 2, elt.x - 1, 3, elt.x - 1), (elt, 2, elt.x - 1, 3, elt.x)))
                    if elt.x < 7 and informations[elt.x + 1] == 1 and (2, elt.x + 1) not in elt.injouables and (2, elt.x + 1) not in elt.coups_piece:
                        coups_no.append(((echequier[elt.x + 1 + 3 * 8], 2, elt.x + 1, 3, elt.x + 1), (elt, 2, elt.x + 1, 3, elt.x)))
                for coup in elt.coups_piece:
                    if coup not in elt.injouables:
                        if not isinstance(elt, Pion) or coup[0] != 0:
                            coups_no.append((elt, coup[0], coup[1], elt.y, elt.x))
                        else:
                            coups_no.append((elt, coup[0], coup[1], elt.y, elt.x, Dame(coup[1], 0, 1)))
                            coups_no.append((elt, coup[0], coup[1], elt.y, elt.x, Tour(coup[1], 0, 1)))
                            coups_no.append((elt, coup[0], coup[1], elt.y, elt.x, Cavalier(coup[1], 0, 1)))
                            coups_no.append((elt, coup[0], coup[1], elt.y, elt.x, Fou(coup[1], 0, 1)))
    if echec == 1:
        coups_noirs = []
        for elt in coups_no:
            cle2 = cle_virtuelle(cle(echequier), elt)
            infos3 = copy.deepcopy(informations)
            r = recherche(cle2, 0)
            if not r[0]:
                chessboard3 = copie_echequier(echequier)
                roi2 = chessboard3[echequier.index(roi)]
                if len(elt) == 5:
                    elt2 = (chessboard3[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4])
                elif len(elt) == 2:
                    elt2 = ((chessboard3[echequier.index(elt[0][0])], elt[0][1], elt[0][2], elt[0][3], elt[0][4]), (chessboard3[echequier.index(elt[1][0])], elt[1][1], elt[1][2], elt[1][3], elt[1][4]))
                else:
                    elt2 = (chessboard3[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4], elt[5])
                chessboard3, infos3 = echequier_virtuel(chessboard3, elt2, infos3)
                if roi2.attaque == []:
                    evaluation = analyse(chessboard3, 0, "lent")
                    #evaluation = analyse2(chessboard3, 0, W[0], W[1], W[2], W[3], W[4], W[5], W[6], W[7], W[8], W[9], W[10], W[11], W[12], W[13])
                    inserer(cle2, (evaluation, chessboard3), 0)
                    coups_noirs.append(elt)
            else:
                if (not isinstance(elt[0], Roi) and r[1][1][echequier.index(roi)].attaque == []) or (isinstance(elt[0], Roi) and r[1][1][elt[2] + elt[1] * 8].attaque == []):
                    coups_noirs.append(elt)
        coups_no = coups_noirs
    return coups_no

def analyse(echequier, tour, vitesse):
    evaluation = 0
    if vitesse == "lent":
        for elt in echequier:
            if isinstance(elt, Piece):
                elt.valeur()
                if isinstance(elt, Roi) and elt.couleur == tour:
                    if elt.attaque != []:
                        echec = 1
                    else:
                        echec = 0
                    pos_roi = (elt.y, elt.x)
    else:
        for elt in echequier:
            if isinstance(elt, Roi) and elt.couleur == tour:
                if elt.attaque != []:
                    echec = 1
                else:
                    echec = 0
                pos_roi = (elt.y, elt.x)
                break
    for elt in echequier:
        if isinstance(elt, Piece):
            if elt.couleur == 0:
                evaluation += elt.valeur_piece
                if tour == 1 and elt.attaque != [] and (echec == 0 or pos_roi in elt.attaque or pos_roi in elt.attaquant):
                    p = en_prise(echequier, elt)
                    if p[0]:
                        evaluation -= p[1]
            else:
                evaluation -= elt.valeur_piece
                if tour == 0 and elt.attaque != [] and (echec == 0 or pos_roi in elt.attaque or pos_roi in elt.attaquant):
                    p = en_prise(echequier, elt)
                    if p[0]:
                        evaluation += p[1]
        elif len(elt[0]) != len(elt[1]):
            evaluation += ((len(elt[0]) - len(elt[1])) / abs((len(elt[0]) - len(elt[1])))) / 64
    return round(evaluation, 5)

def en_prise(echequier, piece):
    attaquants_defenseurs = []
    for elt in piece.defendu:
        pi = echequier[elt[1] + elt[0] * 8]
        attaquants_defenseurs.append(batterie_def_att(echequier, pi, piece, [(pi.valeur_piece, "def")]))
    for elt in piece.attaque:
        pi = echequier[elt[1] + elt[0] * 8]
        attaquants_defenseurs.append(batterie_def_att(echequier, pi, piece, [(pi.valeur_piece, "att")]))
    gains = [piece.valeur_piece]
    gain = 0
    gains_att = [0]
    gains_def = [0]
    lose_a = -1
    lose_d = -1
    n = 0
    while 1:
        n += 1
        attaquants = []
        for i in range(len(attaquants_defenseurs)):
            if attaquants_defenseurs[i][0][1] == "att":
                attaquants.append((attaquants_defenseurs[i][0][0], i))
        if len(attaquants) != 0:
            front = [attaquants[i][0] for i in range(len(attaquants))]
            envoye = min(front)
            if len(attaquants_defenseurs[attaquants[front.index(envoye)][1]]) == 1:
                attaquants_defenseurs.pop(attaquants[front.index(envoye)][1])
            else:
                attaquants_defenseurs[attaquants[front.index(envoye)][1]].pop(0)
            gain += gains[-1]
            gains.append(envoye)
            gains_att.append(gain)
            if gain < 0:
                if lose_d == -1:
                    return (False, 0)
                else:
                    return (True, gains_def[lose_d])
        else:
            gains_att.append(gain)
            if gain < 0:
                if lose_d == -1:
                    return (False, 0)
            if lose_d != -1:
                return (True, gains_def[lose_d])
            break
        defenseurs = []
        for i in range(len(attaquants_defenseurs)):
            if attaquants_defenseurs[i][0][1] == "def":
                defenseurs.append((attaquants_defenseurs[i][0][0], i))
        if len(defenseurs) != 0:
            front = [defenseurs[i][0] for i in range(len(defenseurs))]
            envoye = min(front)
            if len(attaquants_defenseurs[defenseurs[front.index(envoye)][1]]) == 1:
                attaquants_defenseurs.pop(defenseurs[front.index(envoye)][1])
            else:
                attaquants_defenseurs[defenseurs[front.index(envoye)][1]].pop(0)
            gain -= gains[-1]
            gains.append(envoye)
            gains_def.append(gain)
            if gain > 0:
                if lose_d == -1:
                    lose_d = n
                elif gain > gains_def[lose_d]:
                    lose_d = n
        else:
            gains_def.append(gain)
            if gain > 0:
                if lose_d == -1:
                    lose_d = n
                elif gain > gains_def[lose_d]:
                    lose_d = n
                return (True, gains_def[lose_d])
    assert lose_a == -1 and lose_d == -1
    assert gain == 0
    return (False, 0)


def batterie_def_att(echequier, piece2, cible, batterie):
    bat = batterie
    if piece2.y < cible.y and piece2.x < cible.x:
        n = 1
        while piece2.y - n >= 0 and piece2.x - n >= 0:
            if (piece2.y - n, piece2.x - n) in piece2.defendu:
                if isinstance(echequier[piece2.x - n + (piece2.y - n) * 8], Fou) or isinstance(echequier[piece2.x - n + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y - n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y - n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y - n) * 8], cible, bat)
                    return bat
            elif (piece2.y - n, piece2.x - n) in piece2.attaque:
                if isinstance(echequier[piece2.x - n + (piece2.y - n) * 8], Fou) or isinstance(echequier[piece2.x - n + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y - n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y - n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y - n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.y > cible.y and piece2.x < cible.x:
        n = 1
        while piece2.y + n <= 7 and piece2.x - n >= 0:
            if (piece2.y + n, piece2.x - n) in piece2.defendu:
                if isinstance(echequier[piece2.x - n + (piece2.y + n) * 8], Fou) or isinstance(echequier[piece2.x - n + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y + n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y + n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y + n) * 8], cible, bat)
                    return bat
            elif (piece2.y + n, piece2.x - n) in piece2.attaque:
                if isinstance(echequier[piece2.x - n + (piece2.y + n) * 8], Fou) or isinstance(echequier[piece2.x - n + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y + n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y + n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y + n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.y < cible.y and piece2.x > cible.x:
        n = 1
        while piece2.y - n >= 0 and piece2.x + n <= 7:
            if (piece2.y - n, piece2.x + n) in piece2.defendu:
                if isinstance(echequier[piece2.x + n + (piece2.y - n) * 8], Fou) or isinstance(echequier[piece2.x + n + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y - n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y - n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y - n) * 8], cible, bat)
                    return bat
            elif (piece2.y - n, piece2.x + n) in piece2.attaque:
                if isinstance(echequier[piece2.x + n + (piece2.y - n) * 8], Fou) or isinstance(echequier[piece2.x + n + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y - n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y - n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y - n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.y > cible.y and piece2.x > cible.x:
        n = 1
        while piece2.y + n <= 7 and piece2.x + n <= 7:
            if (piece2.y + n, piece2.x + n) in piece2.defendu:
                if isinstance(echequier[piece2.x + n + (piece2.y + n) * 8], Fou) or isinstance(echequier[piece2.x + n + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y + n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y + n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y + n) * 8], cible, bat)
                    return bat
            elif (piece2.y + n, piece2.x + n) in piece2.attaque:
                if isinstance(echequier[piece2.x + n + (piece2.y + n) * 8], Fou) or isinstance(echequier[piece2.x + n + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y + n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y + n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y + n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.y < cible.y:
        n = 1
        while piece2.y - n >= 0:
            if (piece2.y - n, piece2.x) in piece2.defendu:
                if isinstance(echequier[piece2.x + (piece2.y - n) * 8], Tour) or isinstance(echequier[piece2.x + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + (piece2.y - n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x + (piece2.y - n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + (piece2.y - n) * 8], cible, bat)
                    return bat
            elif (piece2.y - n, piece2.x) in piece2.attaque:
                if isinstance(echequier[piece2.x + (piece2.y - n) * 8], Tour) or isinstance(echequier[piece2.x + (piece2.y - n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + (piece2.y - n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x + (piece2.y - n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + (piece2.y - n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.y > cible.y:
        n = 1
        while piece2.y + n <= 7:
            if (piece2.y + n, piece2.x) in piece2.defendu:
                if isinstance(echequier[piece2.x + (piece2.y + n) * 8], Tour) or isinstance(echequier[piece2.x + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + (piece2.y + n) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x + (piece2.y + n) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + (piece2.y + n) * 8], cible, bat)
                    return bat
            elif (piece2.y + n, piece2.x) in piece2.attaque:
                if isinstance(echequier[piece2.x + (piece2.y + n) * 8], Tour) or isinstance(echequier[piece2.x + (piece2.y + n) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + (piece2.y + n) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x + (piece2.y + n) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + (piece2.y + n) * 8], cible, bat)
                    return bat
            n += 1
    elif piece2.x < cible.x:
        n = 1
        while piece2.x - n >= 0:
            if (piece2.y, piece2.x - n) in piece2.defendu:
                if isinstance(echequier[piece2.x - n + (piece2.y) * 8], Tour) or isinstance(echequier[piece2.x - n + (piece2.y) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y) * 8], cible, bat)
                    return bat
            elif (piece2.y, piece2.x - n) in piece2.attaque:
                if isinstance(echequier[piece2.x - n + (piece2.y) * 8], Tour) or isinstance(echequier[piece2.x - n + (piece2.y) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x - n + (piece2.y) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x - n + (piece2.y) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x - n + (piece2.y) * 8], cible, bat)
                    return bat
            n += 1
    else:
        n = 1
        while piece2.x + n <= 7:
            if (piece2.y, piece2.x + n) in piece2.defendu:
                if isinstance(echequier[piece2.x + n + (piece2.y) * 8], Tour) or isinstance(echequier[piece2.x + n + (piece2.y) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y) * 8].valeur_piece, "def"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y) * 8].valeur_piece, "att"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y) * 8], cible, bat)
                    return bat
            elif (piece2.y, piece2.x + n) in piece2.attaque:
                if isinstance(echequier[piece2.x + n + (piece2.y) * 8], Tour) or isinstance(echequier[piece2.x + n + (piece2.y) * 8], Dame):
                    if bat[-1][1] == "def":
                        bat.append((echequier[piece2.x + n + (piece2.y) * 8].valeur_piece, "att"))
                    else:
                        bat.append((echequier[piece2.x + n + (piece2.y) * 8].valeur_piece, "def"))
                    bat = batterie_def_att(echequier, echequier[piece2.x + n + (piece2.y) * 8], cible, bat)
                    return bat
            n += 1
    return bat


def distance(centre, piece):
    return ((centre[0] - piece.y) ** 2 + (centre[1] - piece.x) ** 2) ** 0.5


def informations_virtuelles(coup, informations):
    if len(coup) != 2:
        if isinstance(coup[0], Pion) and abs(coup[1] - coup[3]) == 2:
            informations[8 * coup[0].couleur + coup[2]] = 1
        else:
            for i in range(16):
                informations[i] = 0
        if isinstance(coup[0], Roi):
            informations[16 + coup[0].couleur * 2] = 0
            informations[16 + coup[0].couleur * 2 + 1] = 0
        elif (coup[3] == 0 or coup[3] == 7) and (coup[4] == 0 or coup[4] == 7):
            informations[int(16 + (coup[3] / 7) * 2 + coup[4] / 7)] = 0
    elif isinstance(coup[0][0], Roi):
        informations[16 + coup[0][0].couleur * 2] = 0
        informations[16 + coup[0][0].couleur * 2 + 1] = 0
    return informations

def echequier_virtuel(echequier_v, coup_v, informations):
    i = 0
    n = 2
    while n != 0:
        if isinstance(echequier_v[i], Roi):
            for elt in echequier_v[i].mur:
                echequier_v[elt[1] + elt[0] * 8].mur.pop()
            n -= 1
        i += 1
    if len(coup_v) != 2:
        case = [[], []]
        case = maj1(echequier_v, coup_v, case)
        informations = informations_virtuelles(coup_v, informations)
        if len(coup_v) == 5:
            echequier_v[coup_v[4] + coup_v[3] * 8] = case[0:2]
            echequier_v[coup_v[2] + coup_v[1] * 8] = coup_v[0]
            coup_v[0].x, coup_v[0].y = coup_v[2], coup_v[1]
            coup_v[0].coups(echequier_v)
        else:
            echequier_v[coup_v[4] + coup_v[3] * 8] = case[0:2]
            echequier_v[coup_v[2] + coup_v[1] * 8] = coup_v[5]
            coup_v[5].coups(echequier_v)
            coup_v[5].attaque, coup_v[5].defendu = coup_v[0].attaque, coup_v[0].defendu
    else:
        for coup in coup_v:
            case = [[], []]
            case = maj1(echequier_v, coup, case)
            informations = informations_virtuelles(coup, informations)
            echequier_v[coup[4] + coup[3] * 8] = case[0:2]
            echequier_v[coup[2] + coup[1] * 8] = coup[0]
            coup[0].x, coup[0].y = coup[2], coup[1]
            coup[0].coups(echequier_v)
    n = 2
    i = 0
    while n != 0:
        if isinstance(echequier_v[i], Roi):
            echequier_v[i].muraille(echequier_v, informations)
            echequier_v[i].injouable(echequier_v, informations)
            for elt in echequier_v[i].mur:
                echequier_v[elt[1] + elt[0] * 8].injouable(echequier_v, informations)
            n -= 1
        i += 1
    return echequier_v, informations


def maj1(echequier_v1, coup, case):
    case = maj2(echequier_v1, coup, case)
    if isinstance(echequier_v1[coup[2] + coup[1] * 8], Piece):
        case = maj3(echequier_v1, coup, case)
        maj6(echequier_v1, coup)
    else:
        case = maj4(echequier_v1, coup, case)
        case = maj5(echequier_v1, coup, case)
        maj6(echequier_v1, coup)
        maj7(echequier_v1, coup)
    return case


def maj2(echequier_v1, coup, case):
    defendu2 = []
    attaque2 = []
    for elt in coup[0].defenseur:
        echequier_v1[elt[1] + elt[0] * 8].defendu.remove((coup[3], coup[4]))
    if not isinstance(coup[0], Pion):
        for elt in coup[0].coups_piece:
            if isinstance(echequier_v1[elt[1] + elt[0] * 8], Piece):
                echequier_v1[elt[1] + elt[0] * 8].attaque.remove((coup[3], coup[4]))
            else:
                echequier_v1[elt[1] + elt[0] * 8][coup[0].couleur].remove((coup[3], coup[4]))
    else:
        for elt in coup[0].attaquant:
            echequier_v1[elt[1] + elt[0] * 8].attaque.remove((coup[3], coup[4]))
        for elt in coup[0].coups_potentiels:
            if isinstance(echequier_v1[elt[1] + elt[0] * 8], list) and (coup[3], coup[4]) in echequier_v1[elt[1] + elt[0] * 8][coup[0].couleur]:
                echequier_v1[elt[1] + elt[0] * 8][coup[0].couleur].remove((coup[3], coup[4]))
    for elt in coup[0].defendu:
        case[coup[0].couleur].append(elt)
        echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((coup[3], coup[4]))
        if isinstance(echequier_v1[elt[1] + elt[0] * 8], Pion):
            echequier_v1[elt[1] + elt[0] * 8].coups_potentiels.append((coup[3], coup[4]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Cavalier):
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
            if coup[4] < elt[1] and coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups1.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups1.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] < elt[1] and coup[3] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups2.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                n = elt[1] - coup[4] + 1
                while elt[0] + n <= 7 and elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups2.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8].attaque.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] > elt[1] and coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups3.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups3.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups4.append((coup[3], coup[4]))
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups4.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8].attaque.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
            if coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups5.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and ((isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1])) or (isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups5.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0:
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] - n) * 8].defendu.append((elt[0], elt[1]))
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[3] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups6.append((coup[3], coup[4]))
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and ((isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1])) or (isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups6.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] + n) * 8].attaque.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + (elt[0] + n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] < elt[1]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups7.append((coup[3], coup[4]))
                n = elt[1] - coup[4] + 1
                while elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], list) and not (coup[1] == elt[0] and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0]) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups7.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0]) * 8].attaque.append(elt)
                        n = elt[1] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0]) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0]) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups8.append((coup[3], coup[4]))
                n = coup[4] - elt[1] + 1
                while elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], list) and not (coup[1] == elt[0] and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0]) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups8.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0]) * 8].attaque.append((elt[0], elt[1]))
                        n = 8 - elt[1]
                    else:
                        echequier_v1[elt[1] + n + (elt[0]) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0]) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
            if coup[4] < elt[1] and coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups1.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups1.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] < elt[1] and coup[3] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups2.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                n = elt[1] - coup[4] + 1
                while elt[0] + n <= 7 and elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups2.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8].attaque.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] > elt[1] and coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups3.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups3.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] > elt[1] and coup[3] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups4.append((coup[3], coup[4]))
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups4.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8].attaque.append((elt[0], elt[1]))
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8][coup[0].couleur].append((elt[0], elt[1]))
                    n += 1
                if elt[0] + n <= 7 and elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[3] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups5.append((coup[3], coup[4]))
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and ((isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], list) and not (coup[1] == elt[0] - n and coup[2] == elt[1])) or (isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece) and echequier_v1[elt[1] + (elt[0] - n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups5.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] - n) * 8].attaque.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + (elt[0] - n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] - n >= 0:
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] - n) * 8].defendu.append((elt[0], elt[1]))
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[3] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups6.append((coup[3], coup[4]))
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and ((isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], list) and not (coup[1] == elt[0] + n and coup[2] == elt[1])) or (isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece) and echequier_v1[elt[1] + (elt[0] + n) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups6.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] + n) * 8].attaque.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + (elt[0] + n) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[0] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1]))
                        echequier_v1[elt[1] + (elt[0] + n) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            elif coup[4] < elt[1]:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups7.append((coup[3], coup[4]))
                n = elt[1] - coup[4] + 1
                while elt[1] - n >= 0 and ((isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], list) and not (coup[1] == elt[0] and coup[2] == elt[1] - n)) or (isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece) and echequier_v1[elt[1] - n + (elt[0]) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups7.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0]) * 8].attaque.append(elt)
                        n = elt[1] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0]) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[1] - n >= 0:
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] - n))
                        echequier_v1[elt[1] - n + (elt[0]) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
                echequier_v1[elt[1] + elt[0] * 8].coups8.append((coup[3], coup[4]))
                n = coup[4] - elt[1] + 1
                while elt[1] + n <= 7 and ((isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], list) and not (coup[1] == elt[0] and coup[2] == elt[1] + n)) or (isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece) and echequier_v1[elt[1] + n + (elt[0]) * 8].couleur != coup[0].couleur)):
                    echequier_v1[elt[1] + elt[0] * 8].coups8.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0]) * 8].attaque.append(elt)
                        n = 8 - elt[1]
                    else:
                        echequier_v1[elt[1] + n + (elt[0]) * 8][coup[0].couleur].append(elt)
                    n += 1
                if elt[1] + n <= 7:
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] + n))
                        echequier_v1[elt[1] + n + (elt[0]) * 8].defendu.append(elt)
                    else:
                        echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((coup[1], coup[2]))
                        defendu2.append(elt)
        else:
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[3], coup[4]))
    coup[0].defendu = defendu2
    for elt in coup[0].attaque:
        case[abs(coup[0].couleur - 1)].append(elt)
        echequier_v1[elt[1] + elt[0] * 8].attaquant.remove((coup[3], coup[4]))
        if isinstance(echequier_v1[elt[1] + elt[0] * 8], Pion):
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.remove((coup[3], coup[4]))
            echequier_v1[elt[1] + elt[0] * 8].coups_potentiels.append((coup[3], coup[4]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
            if coup[4] < elt[1] and coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] - n >= 0 and (isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], list) or echequier_v1[elt[1] - n + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups1.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0] - n) * 8].defendu.append(elt)
            elif coup[4] < elt[1] and coup[3] > elt[0]:
                n = elt[1] - coup[4] + 1
                while elt[0] + n <= 7 and elt[1] - n >= 0 and (isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], list) or echequier_v1[elt[1] - n + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups2.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0] + n) * 8].defendu.append(elt)
            elif coup[4] > elt[1] and coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] + n <= 7 and (isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], list) or echequier_v1[elt[1] + n + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups3.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0] - n) * 8].defendu.append(elt)
            else:
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and elt[1] + n <= 7 and (isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], list) or echequier_v1[elt[1] + n + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups4.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0] + n) * 8].defendu.append((elt[0], elt[1]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
            if coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0  and (isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], list) or echequier_v1[elt[1] + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups5.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] == coup[2]):
                        if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1]))
                            echequier_v1[elt[1] + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + (elt[0] - n) * 8].defendu.append(elt)
            elif coup[3] > elt[0]:
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7  and (isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], list) or echequier_v1[elt[1] + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups6.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] == coup[2]):
                        if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1]))
                            echequier_v1[elt[1] + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + (elt[0] + n) * 8].defendu.append(elt)
            elif coup[4] < elt[1]:
                n = elt[1] - coup[4] + 1
                while elt[1] - n >= 0  and (isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], list) or echequier_v1[elt[1] - n + (elt[0]) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups7.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece) or (elt[0] == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0]) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[1] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0]) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0]) * 8].defendu.append(elt)
            else:
                n = coup [4] - elt[1] + 1
                while elt[1] + n <= 7  and (isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], list) or echequier_v1[elt[1] + n + (elt[0]) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups8.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece) or (elt[0] == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0]) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[1]
                    else:
                        echequier_v1[elt[1] + n + (elt[0]) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0]) * 8].defendu.append(elt)
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
            if coup[4] < elt[1] and coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] - n >= 0 and (isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], list) or echequier_v1[elt[1] - n + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups1.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0] - n) * 8].defendu.append(elt)
            elif coup[4] < elt[1] and coup[3] > elt[0]:
                n = elt[1] - coup[4] + 1
                while elt[0] + n <= 7 and elt[1] - n >= 0 and (isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], list) or echequier_v1[elt[1] - n + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups2.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] - n + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0] + n) * 8].defendu.append(elt)
            elif coup[4] > elt[1] and coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0 and elt[1] + n <= 7 and (isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], list) or echequier_v1[elt[1] + n + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups3.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + n + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0 and elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0] - n) * 8].defendu.append(elt)
            elif coup[4] > elt[1] and coup[3] > elt[0]:
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7 and elt[1] + n <= 7 and (isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], list) or echequier_v1[elt[1] + n + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups4.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + n + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7 and elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0] + n) * 8].defendu.append(elt)
            elif coup[3] < elt[0]:
                n = elt[0] - coup[3] + 1
                while elt[0] - n >= 0  and (isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], list) or echequier_v1[elt[1] + (elt[0] - n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups5.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] - n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece) or (elt[0] - n == coup[1] and elt[1] == coup[2]):
                        if isinstance(echequier_v1[elt[1] + (elt[0] - n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] - n, elt[1]))
                            echequier_v1[elt[1] + (elt[0] - n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[0] + 1
                    else:
                        echequier_v1[elt[1] + (elt[0] - n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] - n, elt[1]))
                    echequier_v1[elt[1] + (elt[0] - n) * 8].defendu.append(elt)
            elif coup[3] > elt[0]:
                n = coup[3] - elt[0] + 1
                while elt[0] + n <= 7  and (isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], list) or echequier_v1[elt[1] + (elt[0] + n) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups6.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0] + n, elt[1]))
                    if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece) or (elt[0] + n == coup[1] and elt[1] == coup[2]):
                        if isinstance(echequier_v1[elt[1] + (elt[0] + n) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0] + n, elt[1]))
                            echequier_v1[elt[1] + (elt[0] + n) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[0]
                    else:
                        echequier_v1[elt[1] + (elt[0] + n) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[0] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0] + n, elt[1]))
                    echequier_v1[elt[1] + (elt[0] + n) * 8].defendu.append(elt)
            elif coup[4] < elt[1]:
                n = elt[1] - coup[4] + 1
                while elt[1] - n >= 0  and (isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], list) or echequier_v1[elt[1] - n + (elt[0]) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups7.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] - n))
                    if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece) or (elt[0] == coup[1] and elt[1] - n == coup[2]):
                        if isinstance(echequier_v1[elt[1] - n + (elt[0]) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] - n))
                            echequier_v1[elt[1] - n + (elt[0]) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = elt[1] + 1
                    else:
                        echequier_v1[elt[1] - n + (elt[0]) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[1] - n >= 0:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] - n))
                    echequier_v1[elt[1] - n + (elt[0]) * 8].defendu.append(elt)
            else:
                n = coup [4] - elt[1] + 1
                while elt[1] + n <= 7  and (isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], list) or echequier_v1[elt[1] + n + (elt[0]) * 8].couleur != abs(coup[0].couleur - 1)):
                    echequier_v1[elt[1] + elt[0] * 8].coups8.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((elt[0], elt[1] + n))
                    if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece) or (elt[0] == coup[1] and elt[1] + n == coup[2]):
                        if isinstance(echequier_v1[elt[1] + n + (elt[0]) * 8], Piece):
                            echequier_v1[elt[1] + elt[0] * 8].attaquant.append((elt[0], elt[1] + n))
                            echequier_v1[elt[1] + n + (elt[0]) * 8].attaque.append(elt)
                        else:
                            echequier_v1[elt[1] + (elt[0]) * 8].attaquant.append((coup[1], coup[2]))
                            attaque2.append(elt)
                        n = 8 - elt[1]
                    else:
                        echequier_v1[elt[1] + n + (elt[0]) * 8][abs(coup[0].couleur - 1)].append(elt)
                    n += 1
                if elt[1] + n <= 7:
                    echequier_v1[elt[1] + (elt[0]) * 8].defenseur.append((elt[0], elt[1] + n))
                    echequier_v1[elt[1] + n + (elt[0]) * 8].defendu.append(elt)
    coup[0].attaque = attaque2
    return case


def maj3(echequier_v1, coup, case):
    for elt in echequier_v1[coup[2] + coup[1] * 8].defenseur:
        echequier_v1[elt[1] + elt[0] * 8].defendu.remove((coup[1], coup[2]))
    if not isinstance(echequier_v1[coup[2] + coup[1] * 8], Pion):
        for elt in echequier_v1[coup[2] + coup[1] * 8].coups_piece:
            if isinstance(echequier_v1[elt[1] + elt[0] * 8], Piece):
                if elt != (coup[3], coup[4]):
                    echequier_v1[elt[1] + elt[0] * 8].attaque.remove((coup[1], coup[2]))
                else:
                    case[abs(coup[0].couleur - 1)].remove((coup[1], coup[2]))
            else:
                echequier_v1[elt[1] + elt[0] * 8][echequier_v1[coup[2] + coup[1] * 8].couleur].remove((coup[1], coup[2]))
    else:
        for elt in echequier_v1[coup[2] + coup[1] * 8].attaquant:
            echequier_v1[elt[1] + elt[0] * 8].attaque.remove((coup[1], coup[2]))
        for elt in echequier_v1[coup[2] + coup[1] * 8].coups_potentiels:
            if isinstance(echequier_v1[elt[1] + elt[0] * 8], list):
                if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8][echequier_v1[coup[2] + coup[1] * 8].couleur]:
                    echequier_v1[elt[1] + elt[0] * 8][echequier_v1[coup[2] + coup[1] * 8].couleur].remove((coup[1], coup[2]))
            elif elt == (coup[3], coup[4]):
                if (coup[1], coup[2]) in case[abs(coup[0].couleur - 1)]:
                    case[abs(coup[0].couleur - 1)].remove((coup[1], coup[2]))
    for elt in echequier_v1[coup[2] + coup[1] * 8].defendu:
        echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((coup[1], coup[2]))
        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((coup[1], coup[2]))
        coup[0].attaque.append(elt)
        echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[1], coup[2]))
        if isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
            if coup[2] < elt[1] and coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups1.append((coup[1], coup[2]))
            elif coup[2] < elt[1] and coup[1] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups2.append((coup[1], coup[2]))
            elif coup[2] > elt[1] and coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups3.append((coup[1], coup[2]))
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups4.append((coup[1], coup[2]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
            if coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups5.append((coup[1], coup[2]))
            elif coup[1] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups6.append((coup[1], coup[2]))
            elif coup[2] < elt[1]:
                echequier_v1[elt[1] + elt[0] * 8].coups7.append((coup[1], coup[2]))
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups8.append((coup[1], coup[2]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
            if coup[2] < elt[1] and coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups1.append((coup[1], coup[2]))
            elif coup[2] < elt[1] and coup[1] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups2.append((coup[1], coup[2]))
            elif coup[2] > elt[1] and coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups3.append((coup[1], coup[2]))
            elif coup[2] > elt[1] and coup[1] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups4.append((coup[1], coup[2]))
            elif coup[1] < elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups5.append((coup[1], coup[2]))
            elif coup[1] > elt[0]:
                echequier_v1[elt[1] + elt[0] * 8].coups6.append((coup[1], coup[2]))
            elif coup[2] < elt[1]:
                echequier_v1[elt[1] + elt[0] * 8].coups7.append((coup[1], coup[2]))
            else:
                echequier_v1[elt[1] + elt[0] * 8].coups8.append((coup[1], coup[2]))
    for elt in echequier_v1[coup[2] + coup[1] * 8].attaque:
        echequier_v1[elt[1] + elt[0] * 8].attaquant.remove((coup[1], coup[2]))
        echequier_v1[elt[1] + elt[0] * 8].defenseur.append((coup[1], coup[2]))
        coup[0].defendu.append(elt)
        if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups_piece:
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.remove((coup[1], coup[2]))
            if isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
                if coup[2] < elt[1] and coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
                elif coup[2] < elt[1] and coup[1] > elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
                elif coup[2] > elt[1] and coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
                else:
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
            elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
                if coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
                elif coup[1] > elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
                elif coup[2] < elt[1]:
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
                else:
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
            elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
                if coup[2] < elt[1] and coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
                elif coup[2] < elt[1] and coup[1] > elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
                elif coup[2] > elt[1] and coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
                elif coup[2] > elt[1] and coup[1] > elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
                elif coup[1] < elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
                elif coup[1] > elt[0]:
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
                elif coup[2] < elt[1]:
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
                else:
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
    return case


def maj4(echequier_v1, coup, case):
    for elt in echequier_v1[coup[2] + coup[1] * 8][coup[0].couleur]:
        if isinstance(echequier_v1[elt[1] + elt[0] * 8], Pion):
            echequier_v1[elt[1] + elt[0] * 8].coups_potentiels.remove((coup[1], coup[2]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Cavalier):
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.remove((coup[1], coup[2]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                if (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups1[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                    if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups1[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                if (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups2[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                    if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups2[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                if (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups3[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                    if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups3[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups4[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups4:
                    if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups4[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups1 + echequier_v1[elt[1] + elt[0] * 8].coups2 + echequier_v1[elt[1] + elt[0] * 8].coups3 + echequier_v1[elt[1] + elt[0] * 8].coups4
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                if (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups5[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                    if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups5[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                if (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups6[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                    if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups6[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                if (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups7[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                    if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups7[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8 ].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups8[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups8:
                    if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups8[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups5 + echequier_v1[elt[1] + elt[0] * 8].coups6 + echequier_v1[elt[1] + elt[0] * 8].coups7 + echequier_v1[elt[1] + elt[0] * 8].coups8
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                if (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups1[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                    if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups1[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                if (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups2[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                    if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups2[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                if (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups3[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                    if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups3[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups4:
                if (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups4[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups4:
                    if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups4[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                if (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups5[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                    if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups5[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                if (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups6[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                    if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups6[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                if (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups7[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                    if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups7[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8 ].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups8[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8].attaque.remove(elt)
                while (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups8:
                    if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] != (coup[1], coup[2]) and isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8][coup[0].couleur].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups8[-1] == (coup[3], coup[4]):
                        case[coup[0].couleur].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups1 + echequier_v1[elt[1] + elt[0] * 8].coups2 + echequier_v1[elt[1] + elt[0] * 8].coups3 + echequier_v1[elt[1] + elt[0] * 8].coups4 + echequier_v1[elt[1] + elt[0] * 8].coups5 + echequier_v1[elt[1] + elt[0] * 8].coups6 + echequier_v1[elt[1] + elt[0] * 8].coups7 + echequier_v1[elt[1] + elt[0] * 8].coups8
        else:
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.remove((coup[1], coup[2]))
        echequier_v1[elt[1] + elt[0] * 8].defenseur.append((coup[1], coup[2]))
        coup[0].defendu.append(elt)
    return case


def maj5(echequier_v1, coup, case):
    for elt in echequier_v1[coup[2] + coup[1] * 8][abs(coup[0].couleur - 1)]:
        if isinstance(echequier_v1[elt[1] + elt[0] * 8], Pion):
            echequier_v1[elt[1] + elt[0] * 8].coups_potentiels.remove((coup[1], coup[2]))
            echequier_v1[elt[1] + elt[0] * 8].coups_piece.append((coup[1], coup[2]))
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Fou):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                if (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups1[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups1[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups1[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                if (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups2[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups2[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups2[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                if (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups3[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups3[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups3[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups4[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups4[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8], list):
                       echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups4[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups1 + echequier_v1[elt[1] + elt[0] * 8].coups2 + echequier_v1[elt[1] + elt[0] * 8].coups3 + echequier_v1[elt[1] + elt[0] * 8].coups4
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Tour):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                if (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups5[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups5[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups5[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                if (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups6[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups6[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups6[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                if (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups7[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups7[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups7[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8 ].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups8[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups8[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups8[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups5 + echequier_v1[elt[1] + elt[0] * 8].coups6 + echequier_v1[elt[1] + elt[0] * 8].coups7 + echequier_v1[elt[1] + elt[0] * 8].coups8
        elif isinstance(echequier_v1[elt[1] + elt[0] * 8], Dame):
            if (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups1:
                if (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups1[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups1[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups1[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups1[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups1[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups1[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups1.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups2:
                if (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups2[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups2[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups2[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups2[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups2[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups2[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups2.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups3:
                if (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups3[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups3[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups3[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups3[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups3[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups3[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups3.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups4:
                if (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups4[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups4[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups4[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups4[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups4[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups4[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups4.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups5:
                if (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1, echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] - 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups5[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups5[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups5[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups5[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups5[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups5[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups5.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups6:
                if (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1, echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1]))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + (echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] + 1) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups6[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups6[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups6[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups6[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups6[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups6[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups6.pop()
            elif (coup[1], coup[2]) in echequier_v1[elt[1] + elt[0] * 8].coups7:
                if (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] - 1 + (echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups7[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups7[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups7[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups7[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups7[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups7[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups7.pop()
            else:
                if (echequier_v1[elt[1] + elt[0] * 8 ].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1) in echequier_v1[elt[1] + elt[0] * 8].defenseur:
                    echequier_v1[elt[1] + elt[0] * 8].defenseur.remove((echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0], echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1))
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + 1 + (echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0]) * 8].defendu.remove(elt)
                if echequier_v1[elt[1] + elt[0] * 8].coups8[-1] in echequier_v1[elt[1] + elt[0] * 8].attaquant:
                    echequier_v1[elt[1] + elt[0] * 8].attaquant.remove(echequier_v1[elt[1] + elt[0] * 8].coups8[-1])
                    echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8].attaque.remove(elt)
                while echequier_v1[elt[1] + elt[0] * 8].coups8[-1] != (coup[1], coup[2]):
                    if isinstance(echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8], list):
                        echequier_v1[echequier_v1[elt[1] + elt[0] * 8].coups8[-1][1] + echequier_v1[elt[1] + elt[0] * 8].coups8[-1][0] * 8][abs(coup[0].couleur - 1)].remove(elt)
                    elif echequier_v1[elt[1] + elt[0] * 8].coups8[-1] == (coup[3], coup[4]):
                        case[abs(coup[0].couleur - 1)].remove(elt)
                    echequier_v1[elt[1] + elt[0] * 8].coups8.pop()
            echequier_v1[elt[1] + elt[0] * 8].coups_piece = echequier_v1[elt[1] + elt[0] * 8].coups1 + echequier_v1[elt[1] + elt[0] * 8].coups2 + echequier_v1[elt[1] + elt[0] * 8].coups3 + echequier_v1[elt[1] + elt[0] * 8].coups4 + echequier_v1[elt[1] + elt[0] * 8].coups5 + echequier_v1[elt[1] + elt[0] * 8].coups6 + echequier_v1[elt[1] + elt[0] * 8].coups7 + echequier_v1[elt[1] + elt[0] * 8].coups8
        echequier_v1[elt[1] + elt[0] * 8].attaquant.append((coup[1], coup[2]))
        coup[0].attaque.append(elt)
    return case


def maj6(echequier_v1, coup):
    if coup[3] == 3:
        if isinstance(echequier_v1[coup[4] + 8], Pion) and echequier_v1[coup[4] + 8].couleur == 0:
            if (coup[3], coup[4]) in echequier_v1[coup[4] + 8].coups_potentiels:
                echequier_v1[coup[4] + 8].coups_potentiels.remove((coup[3], coup[4]))
                echequier_v1[coup[4] + 8].coups_piece.append((coup[3], coup[4]))
            else:
                echequier_v1[coup[4] + 8].coups_potentiels.append((coup[3], coup[4]))
    if coup[3] >= 2 and isinstance(echequier_v1[coup[4] + (coup[3] - 1) * 8], Pion) and echequier_v1[coup[4] + (coup[3] - 1) * 8].couleur == 0:
        if (coup[3], coup[4]) in echequier_v1[coup[4]  + (coup[3] - 1) * 8].coups_potentiels:
            echequier_v1[coup[4] + (coup[3] - 1) * 8].coups_potentiels.remove((coup[3], coup[4]))
            echequier_v1[coup[4] + (coup[3] - 1) * 8].coups_piece.append((coup[3], coup[4]))
            if coup[3] == 2:
                if (coup[3] + 1, coup[4]) in echequier_v1[coup[4] + (coup[3] - 1) * 8].coups_potentiels:
                    echequier_v1[coup[4] + 8].coups_potentiels.remove((coup[3] + 1, coup[4]))
                    echequier_v1[coup[4] + 8].coups_piece.append((coup[3] + 1, coup[4]))
                else:
                    echequier_v1[coup[4] + 8].coups_potentiels.append((coup[3] + 1, coup[4]))
    if coup[3] == 4:
        if isinstance(echequier_v1[coup[4] + 48], Pion) and echequier_v1[coup[4] + 48].couleur == 1:
            if (coup[3], coup[4]) in echequier_v1[coup[4] + 48].coups_potentiels:
                echequier_v1[coup[4] + 48].coups_potentiels.remove((coup[3], coup[4]))
                echequier_v1[coup[4] + 48].coups_piece.append((coup[3], coup[4]))
            else:
                echequier_v1[coup[4] + 48].coups_potentiels.append((coup[3], coup[4]))
    if coup[3] <= 5 and isinstance(echequier_v1[coup[4] + (coup[3] + 1) * 8], Pion):
        if (coup[3], coup[4]) in echequier_v1[coup[4] + (coup[3] + 1) * 8].coups_potentiels and echequier_v1[coup[4] + (coup[3] + 1) * 8].couleur == 1:
            echequier_v1[coup[4] + (coup[3] + 1) * 8].coups_potentiels.remove((coup[3], coup[4]))
            echequier_v1[coup[4] + (coup[3] + 1) * 8].coups_piece.append((coup[3], coup[4]))
            if coup[3] == 5:
                if (coup[3] - 1, coup[4]) in echequier_v1[coup[4] + (coup[3] + 1) * 8].coups_potentiels:
                    echequier_v1[coup[4] + 48].coups_potentiels.remove((coup[3] - 1, coup[4]))
                    echequier_v1[coup[4] + 48].coups_piece.append((coup[3] - 1, coup[4]))
                else:
                    echequier_v1[coup[4] + 48].coups_potentiels.append((coup[3] - 1, coup[4]))

def maj7(echequier_v1, coup):
    if coup[1] == 3:
        if isinstance(echequier_v1[coup[2] + 8], Pion) and echequier_v1[coup[2] + 8].couleur == 0:
            if (coup[1], coup[2]) in echequier_v1[coup[2] + 8].coups_piece:
                echequier_v1[coup[2] + 8].coups_piece.remove((coup[1], coup[2]))
                echequier_v1[coup[2] + 8].coups_potentiels.append((coup[1], coup[2]))
            else:
                echequier_v1[coup[2] + 8].coups_potentiels.remove((coup[1], coup[2]))
    if coup[1] >= 2 and isinstance(echequier_v1[coup[2] + (coup[1] - 1) * 8], Pion) and echequier_v1[coup[2] + (coup[1] - 1) * 8].couleur == 0:
        if (coup[1], coup[2]) in echequier_v1[coup[2] + (coup[1] - 1) * 8].coups_piece:
            echequier_v1[coup[2] + (coup[1] - 1) * 8].coups_piece.remove((coup[1], coup[2]))
            echequier_v1[coup[2] + (coup[1] - 1) * 8].coups_potentiels.append((coup[1], coup[2]))
            if coup[1] == 2:
                if (coup[1] + 1, coup[2]) in echequier_v1[coup[2]  + (coup[1] - 1) * 8].coups_piece:
                    echequier_v1[coup[2] + 8].coups_piece.remove((coup[1] + 1, coup[2]))
                    echequier_v1[coup[2] + 8].coups_potentiels.append((coup[1] + 1, coup[2]))
                else:
                    echequier_v1[coup[2] + 8].coups_potentiels.remove((coup[1] + 1, coup[2]))
    if coup[1] == 4:
        if isinstance(echequier_v1[coup[2] + 48], Pion) and echequier_v1[coup[2] + 48].couleur == 1:
            if (coup[1], coup[2]) in echequier_v1[coup[2] + 48].coups_piece:
                echequier_v1[coup[2] + 48].coups_piece.remove((coup[1], coup[2]))
                echequier_v1[coup[2] + 48].coups_potentiels.append((coup[1], coup[2]))
            else:
                echequier_v1[coup[2] + 48].coups_potentiels.remove((coup[1], coup[2]))
    if coup[1] <= 5 and isinstance(echequier_v1[coup[2] + (coup[1] + 1) * 8], Pion):
        if (coup[1], coup[2]) in echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_piece and echequier_v1[coup[2] + (coup[1] + 1) * 8].couleur == 1:
            echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_piece.remove((coup[1], coup[2]))
            echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_potentiels.append((coup[1], coup[2]))
            if coup[1] == 5:
                if (coup[1] - 1, coup[2]) in echequier_v1[coup[2]  + (coup[1] + 1) * 8].coups_piece:
                    echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_piece.remove((coup[1] - 1, coup[2]))
                    echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_potentiels.append((coup[1] - 1, coup[2]))
                else:
                    echequier_v1[coup[2] + (coup[1] + 1) * 8].coups_potentiels.remove((coup[1] - 1, coup[2]))


def parcours_arbre_b(racine, n):
    if isinstance(racine.valeur, str):
        for elt in racine.branches:
            if elt.branches != []:
                parcours_arbre_b(elt, n + 0.5)
    if n % 1 == 0:
        racine.valeur = max(racine.branches[i].valeur for i in range (len(racine.branches)))
    else:
        racine.valeur = min(racine.branches[i].valeur for i in range (len(racine.branches)))
    if n == 0:
        for elt in racine.branches:
            if elt.valeur == racine.valeur:
                print(racine.valeur)
                return (elt, elt.noeud)
                break


def parcours_arbre_n(racine, n):
    if isinstance(racine.valeur, str):
        for elt in racine.branches:
            if elt.branches != []:
                parcours_arbre_n(elt, n + 0.5)
    if n % 1 == 0:
        racine.valeur = min(racine.branches[i].valeur for i in range (len(racine.branches)))
    else:
        racine.valeur = max(racine.branches[i].valeur for i in range (len(racine.branches)))
    if n == 0:
        for elt in racine.branches:
            if elt.valeur == racine.valeur:
                print(racine.valeur)
                return (elt, elt.noeud)
                break


def cle(echequier):
    cle = []
    for elt in echequier:
        val = 0
        if isinstance(elt, Piece):
            if isinstance(elt, Pion):
                val = 1
            elif isinstance(elt, Cavalier):
                val = 2
            elif isinstance(elt, Fou):
                val = 3
            elif isinstance(elt, Tour):
                val = 4
            elif isinstance(elt, Dame):
                val = 5
            else:
                val = 6
            if elt.couleur == 0:
                val += 6
        cle.append(val)
    return tuple(cle)


def creer(cle, infos_n = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]):
    echequier = []
    for i in range(8):
        for k in range(8):
            if cle[i * 8 + k] == 0:
                echequier.append([[], []])
            elif cle[i * 8 + k] <= 6:
                if cle[i * 8 + k] == 1:
                    echequier.append(Pion(k, i, 1))
                elif cle[i * 8 + k] == 2:
                    echequier.append(Cavalier(k, i, 1))
                elif cle[i * 8 + k] == 3:
                    echequier.append(Fou(k, i, 1))
                elif cle[i * 8 + k] == 4:
                    echequier.append(Tour(k, i, 1))
                elif cle[i * 8 + k] == 5:
                    echequier.append(Dame(k, i, 1))
                else:
                    echequier.append(Roi(k, i, 1))
            else:
                if cle[i * 8 + k] == 7:
                    echequier.append(Pion(k, i, 0))
                elif cle[i * 8 + k] == 8:
                    echequier.append(Cavalier(k, i, 0))
                elif cle[i * 8 + k] == 9:
                    echequier.append(Fou(k, i, 0))
                elif cle[i * 8 + k] == 10:
                    echequier.append(Tour(k, i, 0))
                elif cle[i * 8 + k] == 11:
                    echequier.append(Dame(k, i, 0))
                else:
                    echequier.append(Roi(k, i, 0))
    for elt in echequier:
        if isinstance(elt, Piece):
            elt.coups(echequier)
            if isinstance(elt, Roi):
                elt.muraille(echequier, infos_n)
    for elt in echequier:
        if isinstance(elt, Piece) and elt.mur != [] or isinstance(elt, Roi):
            elt.injouable(echequier, infos_n)
    return echequier

def copie_echequier(echequier):
    copie = []
    for case in echequier:
        if isinstance(case, list):
            l = [[], []]
            for i in range(2):
                for tup in case[i]:
                    l[i].append(tup)
            copie.append(l)
        else:
            if isinstance(case, Pion):
                p = Pion(case.x, case.y, case.couleur)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.coups_potentiels:
                    p.coups_potentiels.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            elif isinstance(case, Cavalier):
                p = Cavalier(case.x, case.y, case.couleur)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            elif isinstance(case, Fou):
                p = Fou(case.x, case.y, case.couleur)
                for elt in case.coups1:
                    p.coups1.append(elt)
                for elt in case.coups2:
                    p.coups2.append(elt)
                for elt in case.coups3:
                    p.coups3.append(elt)
                for elt in case.coups4:
                    p.coups4.append(elt)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            elif isinstance(case, Tour):
                p = Tour(case.x, case.y, case.couleur)
                for elt in case.coups5:
                    p.coups5.append(elt)
                for elt in case.coups6:
                    p.coups6.append(elt)
                for elt in case.coups7:
                    p.coups7.append(elt)
                for elt in case.coups8:
                    p.coups8.append(elt)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            elif isinstance(case, Dame):
                p = Dame(case.x, case.y, case.couleur)
                for elt in case.coups1:
                    p.coups1.append(elt)
                for elt in case.coups2:
                    p.coups2.append(elt)
                for elt in case.coups3:
                    p.coups3.append(elt)
                for elt in case.coups4:
                    p.coups4.append(elt)
                for elt in case.coups5:
                    p.coups5.append(elt)
                for elt in case.coups6:
                    p.coups6.append(elt)
                for elt in case.coups7:
                    p.coups7.append(elt)
                for elt in case.coups8:
                    p.coups8.append(elt)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            else:
                p = Roi(case.x, case.y, case.couleur)
                for elt in case.coups_piece:
                    p.coups_piece.append(elt)
                for elt in case.defenseur:
                    p.defenseur.append(elt)
                for elt in case.attaquant:
                    p.attaquant.append(elt)
                for elt in case.defendu:
                    p.defendu.append(elt)
                for elt in case.attaque:
                    p.attaque.append(elt)
            copie.append(p)
    return copie


def cle_virtuelle(cle1, coup):
    cle_v = []
    if len(coup) == 2:
        return cle_virtuelle(cle_virtuelle(cle1, coup[0]), coup[1])
    for i in range(64):
        if coup[4] + coup[3] * 8 == i:
            cle_v.append(0)
        elif coup[2] + coup[1] * 8 == i:
            if len(coup) == 5:
                cle_v.append(cle1[coup[4] + coup[3] * 8])
            else:
                cle_v.append(cle([coup[5]])[0])
        else:
            cle_v.append(cle1[i])
    return tuple(cle_v)


def recherche(cle, couleur):
    a = 0
    b = len(echequiers[couleur][0]) - 1
    if b == -1:
        return (False, 0)
    while a < b:
        if cle < echequiers[couleur][0][int((a + b) / 2)]:
            b = int((a + b) / 2 - 1)
        elif cle == echequiers[couleur][0][int((a + b) / 2)]:
            return (True, echequiers[couleur][1][int((a + b) / 2)])
        else:
            a = int((a + b) / 2 + 1)
    if cle == echequiers[couleur][0][a]:
        return (True, echequiers[couleur][1][a])
    else:
        return (False, 0)


def inserer(cle, echequier, couleur):
    a = 0
    b = len(echequiers[couleur][0])
    if b == 0:
        echequiers[couleur][0].insert(0, cle)
        echequiers[couleur][1].insert(0, echequier)
    else:
        while 1:
            if cle < echequiers[couleur][0][int((a + b) / 2)]:
                b = int((a + b) / 2)
                if a == b:
                    echequiers[couleur][0].insert(a, cle)
                    echequiers[couleur][1].insert(a, echequier)
                    break
            else:
                a = int((a + b + 1) / 2)
                if b == a:
                    echequiers[couleur][0].insert(b, cle)
                    echequiers[couleur][1].insert(b, echequier)
                    break

def choix_coup_b(echequier, informations, nb, racine, cle, profondeur):
    while nb * 2 < len(partie_v):
        partie_v.pop()
    if nb * 2 > len(partie_v):
        partie_v.append(cle)
    elif len(partie_v) != 0:
        partie_v.pop()
        partie_v.append(cle)
    liste = []
    for elt in (coups_b(echequier, informations, "rapide")):
        cle2 = cle_virtuelle(cle, elt)
        infos2 = copy.deepcopy(informations)
        r = recherche(cle2, 1)
        if not r[0]:
            compteur[1] += 1
            temps2[0] -= time.time()
            #chessboard2 = copy.deepcopy(echequier)
            #chessboard2 = creer(cle2, informations_virtuelles(elt, infos2))
            chessboard2 = copie_echequier(echequier)
            temps2[0] += time.time()
            if len(elt) == 5:
                elt2 = (chessboard2[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4])
            elif len(elt) == 2:
                elt2 = ((chessboard2[echequier.index(elt[0][0])], elt[0][1], elt[0][2], elt[0][3], elt[0][4]), (chessboard2[echequier.index(elt[1][0])], elt[1][1], elt[1][2], elt[1][3], elt[1][4]))
            else:
                elt2 = (chessboard2[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4], elt[5])
            chessboard2, infos2 = echequier_virtuel(chessboard2, elt2, infos2)
            evaluation = analyse(chessboard2, 1, "lent")
            #evaluation = analyse2(chessboard2, 1, W[0], W[1], W[2], W[3], W[4], W[5], W[6], W[7], W[8], W[9], W[10], W[11], W[12], W[13])
            if (partie + partie_v).count(cle2) >= 2:
                evaluation = 0
            liste.append((evaluation, elt2, chessboard2, infos2, cle2))
            inserer(cle2, (evaluation, chessboard2), 1)
        else:
            compteur[0] += 1
            liste.append((r[1][0], elt, r[1][1], informations_virtuelles(elt, infos2), cle2))
    eval = sorted([liste[i][0] for i in range(len(liste))])
    eval.reverse()
    if len(eval) == 0:
        for elt in echequier:
            if isinstance(elt, Roi) and elt.couleur == 0:
                if elt.attaque != []:
                    echec = 1
                else:
                    echec = 0
                break
        if echec == 1 and nb != 0:
            racine.valeur = -10000 / nb
        elif echec == 0 and nb != 0:
            racine.valeur = 0
        elif echec == 1 and nb == 0:
            print("Echec et mat !")
            exit()
        else:
            print("nulle")
            exit()
        nb += 0.5
    elif nb == 0:
        liste_triee = []
        while eval != []:
            for i in range(len(liste)):
                if liste[i][0] == eval[0]:
                    liste_triee.append(liste.pop(i)[1:])
                    eval.pop(0)
                    break
        racine0 = Noeud("racine")
        for elt in liste_triee:
            racine0.fils(elt[0])
        nb += 0.5
        for i in range(len(liste_triee)):
            choix_coup_n(liste_triee[i][1], liste_triee[i][2], nb, racine0.branches[i], liste_triee[i][3], 5 - int(i / (int(len(liste_triee) / 5) + 1)))
    else:
        eval2 = eval[0]
        liste_triee = []
        while eval != []:
            for i in range(len(liste)):
                if liste[i][0] == eval[0]:
                    liste_triee.append(liste.pop(i)[1:])
                    eval.pop(0)
                    break
            if len(liste_triee) == profondeur:
                break
        for elt in liste_triee[0][1]:
            if isinstance(elt, Roi) and elt.couleur == 1:
                if elt.attaque != []:
                    echec = 1
                else:
                    echec = 0
                break
        if 1 < profondeur or nb % 1 == 0 or (echec == 1 and nb < 8):
            for elt2 in liste_triee:
                racine.fils(elt2[0])
            nb += 0.5
            if 1 < profondeur:
                for i in range(len(liste_triee)):
                    choix_coup_n(liste_triee[i][1], liste_triee[i][2], nb, racine.branches[i], liste_triee[i][3], profondeur - int(i / 2) - 1)
            else:
                choix_coup_n(liste_triee[0][1], liste_triee[0][2], nb, racine.branches[0], liste_triee[0][3], 1)
        else:
            racine.valeur = eval2
            nb += 0.5
    if nb == 0.5:
        try:
            racine_coup, coup = parcours_arbre_b(racine0, 0)
            cle_v = cle_virtuelle(cle_actuelle, coup)
            racine_coup.branches, racine_coup.valeur = [], ""
            choix_coup_n(recherche(cle_v, 1)[1][1], informations_virtuelles(coup, informations), nb, racine_coup, cle_v, 5)
            parcours_arbre_n(racine_coup, 0)
            racine_coup2, coup2 = parcours_arbre_b(racine0, 0)
            while coup2 != coup:
                racine_coup, coup = racine_coup2, coup2
                cle_v = cle_virtuelle(cle_actuelle, coup)
                racine_coup.branches, racine_coup.valeur = [], ""
                choix_coup_n(recherche(cle_v, 1)[1][1], informations_virtuelles(coup, informations), nb, racine_coup, cle_v, 5)
                parcours_arbre_n(racine_coup, 0)
                racine_coup2, coup2 = parcours_arbre_b(racine0, 0)
            racine1.append(racine0)
            return coup2
        except:
            return coup

def choix_coup_n(echequier, informations, nb, racine, cle, profondeur):
    while nb * 2 < len(partie_v):
        partie_v.pop()
    if nb * 2 > len(partie_v):
        partie_v.append(cle)
    elif len(partie_v) != 0:
        partie_v.pop()
        partie_v.append(cle)
    liste = []
    for elt in (coups_n(echequier, informations, "rapide")):
        cle2 = cle_virtuelle(cle, elt)
        infos2 = copy.deepcopy(informations)
        r = recherche(cle2, 0)
        if not r[0]:
            compteur[1] += 1
            temps2[0] -= time.time()
            #chessboard2 = copy.deepcopy(echequier)
            #chessboard2 = creer(cle2, informations_virtuelles(elt, infos2))
            chessboard2 = copie_echequier(echequier)
            temps2[0] += time.time()
            if len(elt) == 5:
                elt2 = (chessboard2[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4])
            elif len(elt) == 2:
                elt2 = ((chessboard2[echequier.index(elt[0][0])], elt[0][1], elt[0][2], elt[0][3], elt[0][4]), (chessboard2[echequier.index(elt[1][0])], elt[1][1], elt[1][2], elt[1][3], elt[1][4]))
            else:
                elt2 = (chessboard2[echequier.index(elt[0])], elt[1], elt[2], elt[3], elt[4], elt[5])
            chessboard2, infos2 = echequier_virtuel(chessboard2, elt2, infos2)
            evaluation = analyse(chessboard2, 0, "lent")
            #evaluation = analyse2(chessboard2, 0, W[0], W[1], W[2], W[3], W[4], W[5], W[6], W[7], W[8], W[9], W[10], W[11], W[12], W[13])
            if (partie + partie_v).count(cle2) >= 2:
                evaluation =  0
            liste.append((evaluation, elt2, chessboard2, infos2, (cle2)))
            inserer(cle2, (evaluation, chessboard2), 0)
        else:
            compteur[0] += 1
            liste.append((r[1][0], elt, r[1][1], informations_virtuelles(elt, infos2), cle2))
    eval = sorted([liste[i][0] for i in range(len(liste))])
    if len(eval) == 0:
        for elt in echequier:
            if isinstance(elt, Roi) and elt.couleur == 1:
                if elt.attaque != []:
                    echec = 1
                else:
                    echec = 0
                break
        if echec == 1 and nb != 0:
            racine.valeur = 10000 / nb
        elif echec == 0 and nb != 0:
            racine.valeur = 0
        elif echec == 1 and nb == 0:
            print("Echec et mat !")
            exit()
        else:
            print("nulle")
            exit()
        nb += 0.5
    elif nb == 0:
        liste_triee = []
        while eval != []:
            for i in range(len(liste)):
                if liste[i][0] == eval[0]:
                    liste_triee.append(liste.pop(i)[1:])
                    eval.pop(0)
                    break
        racine0 = Noeud("racine")
        for elt in liste_triee:
            racine0.fils(elt[0])
        nb += 0.5
        for i in range(len(liste_triee)):
            choix_coup_b(liste_triee[i][1], liste_triee[i][2], nb, racine0.branches[i], liste_triee[i][3],  5 - int(i / (int(len(liste_triee) / 5) + 1)))
    else:
        eval2 = eval[0]
        liste_triee = []
        while eval != []:
            for i in range(len(liste)):
                if liste[i][0] == eval[0]:
                    liste_triee.append(liste.pop(i)[1:])
                    eval.pop(0)
                    break
            if len(liste_triee) == profondeur:
                break
        for elt in liste_triee[0][1]:
            if isinstance(elt, Roi) and elt.couleur == 0:
                if elt.attaque != []:
                    echec = 1
                else:
                    echec = 0
                break
        if 1 < profondeur or nb % 1 == 0 or (echec == 1 and nb < 8):
            for elt2 in liste_triee:
                racine.fils(elt2[0])
            nb += 0.5
            if 1 < profondeur:
                for i in range(len(liste_triee)):
                    choix_coup_b(liste_triee[i][1], liste_triee[i][2], nb, racine.branches[i], liste_triee[i][3], profondeur - int(i / 2) - 1)
            else:
                choix_coup_b(liste_triee[0][1], liste_triee[0][2], nb, racine.branches[0], liste_triee[0][3], 1)
        else:
            racine.valeur = eval2
            nb += 0.5
    if nb == 0.5:
        try:
            racine_coup, coup = parcours_arbre_n(racine0, 0)
            cle_v = cle_virtuelle(cle_actuelle, coup)
            racine_coup.branches, racine_coup.valeur = [], ""
            choix_coup_b(recherche(cle_v, 0)[1][1], informations_virtuelles(coup, informations), nb, racine_coup, cle_v, 5)
            parcours_arbre_b(racine_coup, 0)
            racine_coup2, coup2 = parcours_arbre_n(racine0, 0)
            while coup2 != coup:
                racine_coup, coup = racine_coup2, coup2
                cle_v = cle_virtuelle(cle_actuelle, coup)
                racine_coup.branches, racine_coup.valeur = [], ""
                choix_coup_b(recherche(cle_v, 0)[1][1], informations_virtuelles(coup, informations), nb, racine_coup, cle_v, 5)
                parcours_arbre_b(racine_coup, 0)
                racine_coup2, coup2 = parcours_arbre_n(racine0, 0)
            racine1.append(racine0)
            return coup2
        except:
            return coup


def valeur_p(X, W, b):
    return (X.dot(W))[0][0] + b[0]


def valeur_p2(X, W, b):
    v = 1
    l = [sig(X[0][i] * W[i][0]) for i in range (len(X[0]))]
    for elt in l:
        v *= elt
    return (rec_sig(v ** (1 / len(W))) + 1 ) * b[0]


def f(x):
    return (np.exp(x) - 1) * (np.exp(1) + 1) / ((np.exp(x) + 1) * (np.exp(1) - 1))

def sig(x):
    return 1 / (1 + np.exp(-x))

def rec_sig(x):
    return np.log(x / (1 - x))


def analyse2(echequier, tour, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour):
    cases_vides = 0
    n = 2
    m = 0
    while n != 0:
        if isinstance(echequier[m], Roi):
            n -= 1
            if echequier[m].couleur == 0:
                roi_b = echequier[m]
            else:  
                roi_n = echequier[m]
        m += 1
    for i in range(8):
        for k in range(8):
            case = echequier[k + 8 * i]
            if isinstance(case, Piece):
                if case.couleur == 0:
                    if isinstance(case, Pion):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) + len(case.coups_potentiels) * 0.5 - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_n)]]), W_pion, b_pion)
                    elif isinstance(case, Cavalier):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_n)]]), W_cavalier, b_cavalier)
                    elif isinstance(case, Fou):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_n)]]), W_fou, b_fou)
                    elif isinstance(case, Tour):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_n)]]), W_tour, b_tour)
                    elif isinstance(case, Dame):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_n)]]), W_dame, b_dame)
                    else:
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables) * 2, f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.attaque))]]), W_roi, b_roi)
                else:
                    if isinstance(case, Pion):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) + len(case.coups_potentiels) * 0.5 - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_b)]]), W_pion, b_pion)
                    elif isinstance(case, Cavalier):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_b)]]), W_cavalier, b_cavalier)
                    elif isinstance(case, Fou):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_b)]]), W_fou, b_fou)
                    elif isinstance(case, Tour):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_b)]]), W_tour, b_tour)
                    elif isinstance(case, Dame):
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables), f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.defendu)), f(len(case.attaque)), distance((i, k), roi_b)]]), W_dame, b_dame)
                    else:
                        case.valeur_piece = valeur_p(np.array([[abs(k - 3.5), 7 - i, abs(i - 3.5), len(case.coups_piece) - len(case.injouables) * 2, f(len(case.defenseur)), f(len(case.attaquant)), f(len(case.attaque))]]), W_roi, b_roi)
            else:
                cases_vides +=  (1 / (((k - 3.5) ** 2 + (i - 3.5) ** 2) ** (1 / 2) + 1)) * w_list[0] * f(len(case[0]) - len(case[1]))
    return analyse(echequier, tour, "rapide") + cases_vides + b_prochain_tour[0] * (-tour * 2 + 1)


def ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour):
    ecart = 0
    for elt in base:
        ecart += abs(analyse2(elt[0], elt[1], W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour) - elt[2])
    return ecart / len(base)

def ecart2(parametres):
    W_pion = np.array([[-1 / 32], [1 / 8], [-1 / 32], [1 / 16], [1 / 64], [1 / 32], [1 / 64], [-1 / 32], [-1 / 32]])
    b_pion = [0.375]
    W_cavalier = np.array([[-1 / 16], [1 / 64], [-1 / 16], [1 / 32], [1 / 64], [1 / 16], [1 / 64], [-1 / 16], [-1 / 32]])
    b_cavalier = [2.5]
    W_fou = np.array([[-1 / 64], [1 / 64], [-1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]])
    b_fou = [2.25]
    W_tour = np.array([[0], [1 / 32], [1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]])
    b_tour = [4]
    W_dame = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 64], [1 / 128], [1 / 64], [1 / 128], [-1 / 16], [-1 / 32]])
    b_dame = [8.25]
    W_roi = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 16], [1 / 64], [1 / 32], [-1 / 8]])
    b_roi = [101]
    w_list = [1 / 64]
    w_centre_roi = [1]
    w_mur = [0.5]
    b_prochain_tour = [0.1]
    params = [W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour]
    i = 0
    for elt in params:
        if len(elt) == 1:
            elt[0] = parametres[i]
            i += 1
        else:
            for elt2 in elt:
                elt2[0] = parametres[i]
                i += 1
    ecart = 0
    for elt in base_entrainement:
        ecart += abs(analyse2(elt[0], elt[1], W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour) - elt[2])
    return ecart / len(base_entrainement)


def entrainement(base, W_pion = np.array([[-1 / 32], [1 / 8], [-1 / 32], [1 / 16], [1 / 64], [1 / 32], [1 / 64], [-1 / 32], [-1 / 32]]), b_pion = [0.375], W_cavalier = np.array([[-1 / 16], [1 / 64], [-1 / 16], [1 / 32], [1 / 64], [1 / 16], [1 / 64], [-1 / 16], [-1 / 32]]), b_cavalier = [2.5], W_fou = np.array([[-1 / 64], [1 / 64], [-1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]]), b_fou = [2.25], W_tour = np.array([[0], [1 / 32], [1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]]), b_tour = [4], W_dame = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 64], [1 / 128], [1 / 64], [1 / 128], [-1 / 16], [-1 / 32]]), b_dame = [8.25], W_roi = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 16], [1 / 64], [1 / 32], [-1 / 8]]), b_roi = [101], w_list = [1 / 64], w_centre_roi = [1], w_mur = [0.5], b_prochain_tour = [0.1]):
    ecart_min = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
    print(ecart_min)
    precision = 5
    while precision < 5:
        ecart_fixe = ecart_min
        for elt in W_pion:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        b_pion += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_pion -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_pion -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_pion += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        for elt in W_cavalier:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        b_cavalier += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_cavalier -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_cavalier -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_cavalier += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        for elt in W_fou:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        b_fou += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_fou -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_fou -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_fou += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        for elt in W_tour:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        b_tour += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_tour -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_tour -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_tour += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        for elt in W_dame:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        b_dame += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_dame -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_dame -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_dame += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        for elt in W_roi:
            elt[0] += 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] -= 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
            elt[0] -= 1 / (512 * 2 ** precision)
            new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
            if new_ecart > ecart_min:
                elt[0] += 1 / (512 * 2 ** precision)
            else:
                ecart_min = new_ecart
        w_list += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_list -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        w_list -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_list += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        w_centre_roi += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_centre_roi -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        w_centre_roi -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_centre_roi += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        w_mur += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_mur -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        w_mur -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            w_mur += 1 / (512 * 2 ** precision)
        b_prochain_tour += 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_prochain_tour -= 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        b_prochain_tour -= 1 / (512 * 2 ** precision)
        new_ecart = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if new_ecart > ecart_min:
            b_prochain_tour += 1 / (512 * 2 ** precision)
        else:
            ecart_min = new_ecart
        if ecart_fixe - ecart_min < 1 * 10 **(-5):
            precision += 1
            print(ecart_min)
            print(W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
    return (W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)


def entrainement2(base, W_pion = np.array([[-1 / 32], [1 / 8], [-1 / 32], [1 / 16], [1 / 64], [1 / 32], [1 / 64], [-1 / 32], [-1 / 32]]), b_pion = [0.375], W_cavalier = np.array([[-1 / 16], [1 / 64], [-1 / 16], [1 / 32], [1 / 64], [1 / 16], [1 / 64], [-1 / 16], [-1 / 32]]), b_cavalier = [2.5], W_fou = np.array([[-1 / 64], [1 / 64], [-1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]]), b_fou = [2.25], W_tour = np.array([[0], [1 / 32], [1 / 32], [1 / 32], [1 / 64], [1 / 32], [1 / 64], [-1 / 16], [-1 / 32]]), b_tour = [4], W_dame = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 64], [1 / 128], [1 / 64], [1 / 128], [-1 / 16], [-1 / 32]]), b_dame = [8.25], W_roi = np.array([[-1 / 64], [1 / 64], [-1 / 64], [1 / 16], [1 / 64], [1 / 32], [-1 / 8]]), b_roi = [101], w_list = [1 / 64], w_centre_roi = [1], w_mur = [0.5], b_prochain_tour = [0.1]):
    parametres = [W_pion, [b_pion], W_cavalier, [b_cavalier], W_fou, [b_fou], W_tour, [b_tour], W_dame, [b_dame], W_roi, [w_list], [w_centre_roi], [w_mur], [b_prochain_tour]]
    ecart_min = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
    a = 0.01
    print(ecart_min)
    while 1:
        ecart_fixe = ecart_min
        for elt in parametres:
            for elt2 in elt:
                elt2[0] += 0.02
                elt2[0] -= ((ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour) - ecart_min) * a / 0.02) + 0.02
                ecart_min = ecart(base, W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)
        if ecart_fixe - ecart_min < 1 * 10 ** (-5):
            print(ecart_min)
            break
        print(ecart_min)
        if a > 0.005:
            a = a / 1.1
    return (W_pion, b_pion, W_cavalier, b_cavalier, W_fou, b_fou, W_tour, b_tour, W_dame, b_dame, W_roi, b_roi, w_list, b_prochain_tour)

def afficher(echequier):
    liste = []
    for elt in echequier:
        if isinstance(elt, Piece):
            if isinstance(elt, Pion):
                if elt.couleur == 0:
                    liste.append("PB")
                else:
                    liste.append("PN")
            elif isinstance(elt, Fou):
                if elt.couleur == 0:
                    liste.append("FB")
                else:
                    liste.append("FN")
            elif isinstance(elt, Cavalier):
                if elt.couleur == 0:
                    liste.append("CB")
                else:
                    liste.append("CN")
            elif isinstance(elt, Tour):
                if elt.couleur == 0:
                    liste.append("TB")
                else:
                    liste.append("TN")
            elif isinstance(elt, Dame):
                if elt.couleur == 0:
                    liste.append("DB")
                else:
                    liste.append("DN")
            else:
                if elt.couleur == 0:
                    liste.append("RB")
                else:
                    liste.append("RN")
        else:
            liste.append("  ")
    liste.reverse()
    for i in range(8):
        l = liste[i * 8:(i + 1) * 8]
        l.reverse()
        print(l)
    print("")


def arbre(racine, chemin):
    feuille = racine
    for elt in chemin:
        feuille = feuille.branches[elt - 1]
    if feuille.branches != []:
        for elt in feuille.branches:
            print(elt.noeud, elt.valeur)
    else:
        print(feuille.valeur)


chessboard = [Tour(0, 0, 0), Cavalier(1, 0, 0), Fou(2, 0, 0), Dame(3, 0, 0), Roi(4, 0, 0), Fou(5, 0, 0), Cavalier(6, 0, 0), Tour(7, 0, 0), Pion(0, 1, 0), Pion(1, 1, 0), Pion(2, 1, 0), Pion(3, 1, 0), Pion(4, 1, 0), Pion(5, 1, 0), Pion(6, 1, 0), Pion(7, 1, 0), [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], [[],[]], Pion(0, 6, 1), Pion(1, 6, 1), Pion(2, 6, 1), Pion(3, 6, 1), Pion(4, 6, 1), Pion(5, 6, 1), Pion(6, 6, 1), Pion(7, 6, 1), Tour(0, 7, 1), Cavalier(1, 7, 1), Fou(2, 7, 1), Dame(3, 7, 1), Roi(4, 7, 1), Fou(5, 7, 1), Cavalier(6, 7, 1), Tour(7, 7, 1)]
infos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]
cle_actuelle = cle(chessboard)
echequiers = [[[], []], [[], []]]
temps2 = [0]
coups_b(chessboard, infos, "lent")
coups_n(chessboard, infos, "lent")
temps = time.time()
compteur = [0, 0]
racine1 = []
tour = 1
partie = [cle_actuelle]
partie_v = []
print(cle_actuelle)
base_entrainement = [(creer((10, 0, 9, 11, 12, 9, 0, 10, 7, 7, 7, 0, 0, 7, 7, 7, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 8, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 4, 2, 3, 5, 6, 3, 0, 4)), 1, 0.24), (creer((10, 8, 9, 11, 10, 0, 12, 0, 7, 7, 0, 7, 0, 7, 7, 7, 0, 9, 7, 0, 0, 8, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 2, 1, 0, 2, 0, 0, 0, 0, 1, 0, 3, 1, 1, 1, 4, 0, 3, 5, 0, 4, 6, 0)), 0, 0.54), (creer((10, 0, 9, 11, 12, 9, 0, 10, 7, 7, 7, 0, 0, 7, 7, 7, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 4, 2, 0, 0, 6, 3, 0, 4)), 0, 0.75), (creer((10, 0, 9, 0, 12, 9, 0, 10, 0, 0, 7, 0, 8, 7, 7, 7, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 5, 0, 2, 1, 0, 11, 4, 2, 3, 0, 6, 0, 4, 0)), 1, 0.05), (creer((10, 0, 0, 11, 0, 10, 9, 12, 7, 7, 7, 0, 0, 0, 7, 7, 0, 8, 8, 9, 0, 0, 0, 0, 0, 0, 0, 0, 2, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 2, 0, 3, 7, 1, 0, 1, 1, 0, 0, 1, 0, 3, 1, 4, 0, 5, 4, 0, 0, 6, 0)), 1, -0.29), (creer((10, 0, 0, 11, 0, 10, 12, 0, 0, 0, 7, 8, 9, 7, 7, 7, 7, 0, 0, 7, 0, 8, 0, 0, 0, 7, 0, 0, 0, 0, 0, 9, 0, 0, 3, 1, 1, 3, 0, 0, 0, 0, 2, 0, 0, 2, 0, 1, 1, 1, 1, 0, 0, 4, 1, 0, 4, 0, 0, 5, 0, 0, 6, 0)), 1, -0.49), (creer((10, 0, 9, 11, 12, 9, 8, 10, 7, 7, 7, 7, 0, 7, 7, 7, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 4, 2, 3, 0, 6, 3, 2, 4)), 1, 0.92), (creer((0, 12, 0, 10, 0, 0, 0, 10, 7, 7, 7, 9, 0, 7, 7, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0, 1, 2, 0, 1, 1, 1, 0, 0, 3, 1, 1, 0, 4, 0, 0, 5, 0, 4, 6, 0)), 0, 0.72), (creer((0, 12, 0, 10, 0, 0, 0, 10, 7, 7, 7, 11, 0, 0, 7, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0, 0, 0, 7, 0, 7, 0, 0, 4, 7, 0, 0, 8, 1, 1, 5, 0, 1, 0, 0, 1, 0, 0, 3, 0, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0)), 1, 0.00), (creer((0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 7, 0, 0, 0, 0, 0, 7, 7, 0, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 8, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0)), 0, -4.49), (creer((10, 0, 0, 0, 0, 0, 0, 12, 0, 7, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 11, 1, 0, 6, 0, 0, 1, 1, 0, 0, 0, 4, 0, 0, 0, 4)), 1, 3.11), (creer((10, 0, 0, 0, 0, 0, 12, 0, 7, 7, 11, 0, 9, 7, 0, 7, 0, 0, 8, 0, 0, 8, 7, 0, 0, 0, 0, 10, 7, 0, 0, 0, 0, 1, 3, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 3, 5, 0, 0, 1, 0, 1, 4, 0, 0, 0, 0, 4, 6, 0)), 0, 0.00), (creer((10, 0, 0, 11, 0, 10, 12, 0, 0, 7, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 7, 2, 0, 0, 0, 1, 2, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 4, 0, 3, 0, 6, 3, 0, 4)), 0, 0.50), (creer((0, 12, 0, 10, 0, 0, 0, 10, 0, 7, 7, 0, 0, 0, 11, 0, 7, 9, 0, 0, 0, 7, 0, 0, 0, 0, 2, 8, 0, 0, 0, 7, 1, 1, 0, 7, 0, 0, 9, 2, 0, 5, 0, 1, 0, 0, 1, 0, 0, 0, 0, 3, 1, 1, 3, 0, 0, 0, 0, 0, 4, 0, 6, 0)), 0, 0.88), (creer((0, 0, 0, 10, 0, 0, 0, 0, 7, 0, 0, 0, 0, 3, 12, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 10, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 4, 6, 0)), 1, 1.87), (creer((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 12, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 7, 6, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0)), 1, 2.14), (creer((10, 8, 9, 0, 12, 9, 8, 10, 7, 7, 7, 7, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 4, 2, 3, 5, 6, 3, 0, 4)), 1, 0.02), (creer((10, 0, 0, 11, 0, 10, 12, 0, 7, 9, 0, 0, 8, 7, 7, 7, 0, 0, 8, 0, 0, 0, 0, 0, 0, 3, 9, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 4, 2, 3, 5, 6, 0, 0, 4)), 1, 0.41), (creer((0, 0, 0, 0, 0, 10, 0, 0, 7, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 10, 0, 0, 1, 0, 0, 1, 12, 1, 0, 6, 0, 1, 0, 0, 1, 0, 4, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0)), 1, 1.16), (creer((10, 8, 9, 0, 0, 0, 12, 0, 7, 7, 7, 7, 11, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 9, 0, 0, 8, 0, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 1, 3, 1, 1, 1, 4, 0, 3, 5, 0, 4, 6, 0)), 0, -0.31), (creer((0, 12, 0, 10, 0, 0, 0, 10, 7, 7, 7, 0, 8, 7, 7, 0, 0, 0, 8, 9, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 11, 1, 0, 0, 0, 1, 7, 0, 0, 0, 0, 2, 2, 0, 1, 0, 1, 0, 1, 1, 1, 3, 5, 1, 0, 0, 0, 0, 6, 4, 0, 0, 0, 4)), 1, -1.25), (creer((0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 9, 4)), 1, 2.24), (creer((10, 0, 0, 0, 10, 0, 0, 0, 0, 7, 0, 9, 0, 7, 12, 0, 0, 0, 7, 9, 0, 8, 7, 11, 0, 0, 0, 7, 2, 0, 0, 7, 0, 0, 1, 1, 0, 4, 8, 1, 0, 1, 0, 0, 1, 2, 1, 0, 0, 3, 0, 0, 5, 0, 3, 0, 0, 0, 0, 0, 0, 4, 6, 0)), 0, 0.00), (creer((10, 8, 0, 0, 0, 12, 0, 0, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 9, 0, 0, 0, 0, 1, 0, 4, 0, 0, 1, 1, 2, 2, 0, 0, 1, 0, 4, 0, 0, 5, 0, 6, 3, 11)), 0, 0.00), (creer((0, 0, 0, 0, 10, 11, 12, 10, 7, 9, 7, 8, 9, 7, 7, 7, 0, 7, 0, 7, 0, 8, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 2, 3, 0, 2, 0, 0, 0, 0, 0, 3, 0, 1, 1, 1, 0, 4, 0, 5, 0, 4, 6, 0)), 0, -1.75), (creer((0, 10, 0, 0, 0, 10, 12, 0, 7, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 1, 0, 4, 11, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 1, 0, 0, 6, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 0, 0)), 0, -0.86), (creer((0, 0, 12, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 10, 0, 7, 0, 0, 0, 0, 0, 7, 7, 0, 0, 1, 0, 10, 0, 0, 0, 0, 1, 0, 2, 11, 1, 0, 0, 0, 0, 0, 5, 1, 0, 0, 1, 6, 0, 0, 4, 0, 0, 4, 0, 0)), 0, 1.28), (creer((10, 0, 9, 11, 12, 9, 0, 10, 7, 7, 0, 8, 0, 7, 7, 7, 0, 0, 7, 0, 0, 8, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 1, 1, 7, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 1, 1, 0, 0, 3, 1, 1, 1, 4, 2, 3, 5, 0, 4, 6, 0)), 1, 0.04), (creer((0, 10, 0, 11, 0, 10, 12, 0, 7, 0, 7, 9, 9, 7, 7, 0, 0, 0, 8, 0, 0, 8, 0, 7, 0, 5, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1, 0, 1, 2, 0, 0, 1, 1, 0, 2, 0, 1, 1, 1, 4, 0, 0, 0, 6, 3, 0, 4)), 1, 1.02), (creer((10, 0, 0, 0, 0, 10, 12, 0, 0, 7, 7, 0, 11, 7, 7, 7, 0, 0, 0, 7, 0, 1, 0, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 9, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 4, 0, 0, 5, 4, 0, 6, 0)), 0, -0.70), (creer((10, 0, 0, 0, 0, 10, 12, 0, 0, 9, 0, 0, 9, 0, 7, 7, 7, 7, 0, 7, 0, 0, 11, 0, 0, 0, 7, 1, 7, 7, 0, 0, 1, 0, 0, 0, 1, 8, 0, 0, 0, 1, 2, 0, 0, 5, 0, 1, 0, 3, 1, 0, 0, 1, 1, 2, 4, 0, 0, 0, 4, 0, 6, 0)), 1, 2.35), (creer((10, 0, 9, 0, 0, 10, 12, 0, 7, 7, 11, 0, 0, 7, 7, 7, 0, 0, 8, 9, 7, 8, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 1, 3, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 4, 0, 3, 5, 0, 4, 6, 0)), 0, -0.14), (creer((0, 0, 10, 11, 0, 10, 12, 0, 7, 7, 0, 0, 0, 7, 9, 7, 0, 0, 8, 0, 0, 0, 7, 0, 0, 0, 7, 2, 1, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 1, 3, 1, 0, 1, 1, 0, 1, 4, 0, 0, 5, 6, 0, 0, 4)), 0, -0.98), (creer((10, 0, 0, 11, 10, 9, 12, 0, 7, 9, 0, 8, 0, 7, 7, 0, 0, 7, 0, 7, 0, 8, 0, 7, 1, 0, 7, 1, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 2, 3, 0, 0, 1, 5, 2, 0, 1, 1, 1, 4, 0, 0, 0, 0, 4, 6, 0)), 0, -0.47), (creer((0, 0, 10, 11, 10, 0, 12, 0, 7, 7, 0, 8, 0, 7, 7, 7, 0, 0, 7, 9, 0, 8, 0, 0, 0, 0, 0, 7, 0, 9, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 1, 1, 3, 0, 2, 3, 1, 1, 0, 4, 0, 0, 5, 0, 4, 6, 0)), 0, -0.65), (creer((0, 0, 10, 0, 10, 0, 12, 0, 7, 7, 0, 0, 0, 7, 3, 7, 0, 11, 0, 0, 9, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 4, 5, 0, 3, 6, 4)), 0, -5.00), (creer((10, 0, 10, 0, 9, 0, 12, 0, 11, 0, 0, 0, 0, 0, 7, 0, 0, 7, 8, 9, 7, 0, 0, 7, 0, 0, 0, 7, 2, 7, 0, 0, 0, 0, 0, 1, 8, 1, 0, 0, 1, 2, 0, 0, 1, 0, 1, 0, 0, 3, 0, 0, 5, 0, 3, 1, 4, 0, 4, 0, 0, 0, 6, 0)), 1, 0.89), (creer((10, 0, 0, 11, 0, 0, 12, 10, 7, 7, 0, 0, 9, 7, 7, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 7, 8, 7, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 2, 0, 0, 0, 0, 1, 0, 6, 0, 4, 0, 3, 5, 0, 0, 0, 4)), 0, 0.37), (creer((10, 8, 9, 0, 0, 10, 12, 0, 7, 7, 7, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 9, 0, 7, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 4, 2, 3, 5, 6, 3, 2, 4)), 1, -0.70), (creer((10, 0, 9, 11, 12, 0, 0, 10, 0, 0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 8, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 8, 0, 0, 3, 2, 0, 1, 0, 6, 0, 1, 1, 0, 0, 2, 1, 1, 0, 4, 0, 3, 5, 0, 4, 0, 0)), 1, 6.75), (creer((10, 0, 0, 11, 12, 9, 0, 10, 7, 5, 7, 9, 7, 7, 7, 7, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 4, 0, 3, 0, 6, 3, 2, 4)), 1, 2.25), (creer((10, 0, 0, 11, 0, 10, 12, 0, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 8, 0, 0, 8, 9, 0, 0, 0, 9, 0, 7, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0, 1, 1, 3, 1, 1, 0, 1, 0, 0, 4, 2, 0, 5, 0, 4, 6, 0)), 0, 1.60), (creer((10, 8, 0, 11, 12, 0, 0, 10, 7, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 7, 0, 1, 0, 0, 0, 1, 7, 0, 0, 0, 0, 0, 0, 0, 1, 8, 1, 0, 0, 1, 1, 0, 2, 2, 0, 0, 1, 4, 5, 0, 0, 6, 3, 0, 4)), 0, 6.39), (creer((10, 8, 0, 0, 12, 0, 0, 10, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 3, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 4, 0, 0, 5, 0, 6, 0, 4)), 0, -1.71), (creer((10, 0, 9, 11, 0, 0, 8, 10, 0, 7, 7, 7, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 3, 1, 12, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 4, 0, 0, 6, 0, 0, 0, 4)), 1, 0.00), (creer((0, 0, 12, 10, 0, 0, 8, 3, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 9, 0, 7, 0, 0, 0, 0, 7, 7, 0, 0, 0, 11, 0, 0, 0, 1, 0, 0, 9, 0, 0, 1, 1, 0, 0, 7, 1, 0, 1, 0, 0, 2, 0, 1, 0, 1, 4, 0, 0, 5, 0, 4, 6, 0)), 0, 0.00), (creer((10, 0, 0, 11, 8, 10, 12, 0, 0, 7, 0, 0, 9, 9, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7, 1, 1, 0, 7, 0, 0, 7, 1, 0, 0, 1, 0, 0, 7, 1, 0, 2, 2, 0, 8, 1, 1, 3, 0, 0, 3, 0, 4, 0, 0, 5, 0, 4, 6, 0)), 1, 1.69), (creer((0, 12, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 7, 7, 0, 0, 0, 7, 0, 0, 0, 0, 7, 6, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 0, 0.00), (creer((10, 0, 0, 11, 0, 10, 12, 0, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 8, 9, 9, 8, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 2, 0, 1, 0, 0, 1, 1, 0, 1, 3, 0, 1, 1, 4, 0, 3, 5, 0, 4, 6, 0)), 1, -0.85), (creer((10, 0, 0, 11, 9, 10, 12, 0, 7, 7, 0, 8, 9, 7, 7, 7, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 4, 2, 3, 5, 6, 3, 2, 4)), 1, 1.67), (creer((0, 12, 0, 10, 0, 0, 0, 10, 7, 7, 7, 0, 11, 0, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 5, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 6, 0, 1, 0, 4, 0, 0, 4, 0, 0, 0, 0)), 0, 2.20), (creer((10, 0, 9, 0, 12, 0, 0, 0, 7, 7, 7, 0, 9, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 1, 1, 6, 1, 0, 0, 10, 1, 4, 0, 3, 0, 0, 0, 0, 2)), 1, -1.05), (creer((10, 0, 0, 0, 0, 10, 12, 0, 7, 7, 7, 0, 0, 7, 7, 0, 0, 0, 8, 0, 0, 11, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 7, 0, 1, 0, 5, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 9, 1, 0, 4, 0, 3, 6, 0, 0, 0, 4)), 1, -1.20), (creer((10, 0, 9, 11, 0, 0, 0, 0, 7, 7, 7, 7, 0, 12, 7, 0, 0, 0, 8, 0, 0, 8, 0, 7, 0, 0, 9, 0, 7, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 4, 0, 3, 5, 0, 4, 6, 0)), 0, 2.51), (creer((10, 8, 9, 0, 12, 0, 0, 10, 7, 7, 7, 7, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 9, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 1, 1, 1, 0, 0, 0, 1, 1, 4, 2, 3, 5, 0, 3, 2, 4)), 0, 5.12), (creer((0, 12, 0, 10, 0, 0, 0, 10, 7, 9, 7, 7, 11, 7, 7, 7, 0, 7, 0, 9, 0, 8, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 1, 3, 0, 0, 3, 1, 1, 1, 4, 2, 0, 5, 0, 4, 6, 0)), 1, 0.00), (creer((0, 0, 0, 10, 0, 0, 12, 0, 0, 7, 0, 0, 0, 7, 7, 7, 7, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 3, 6, 0, 1, 0, 4, 0, 0, 0, 0, 0, 0, 0)), 1, 0.83), (creer((10, 0, 0, 0, 0, 10, 12, 0, 7, 7, 7, 0, 0, 7, 7, 7, 0, 0, 9, 7, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 5, 0, 0, 0, 0, 1, 0, 0, 0, 4, 4, 6, 0, 0)), 1, -0.58), (creer((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 0, 0, 0, 5, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 0, -0.37), (creer((0, 0, 10, 0, 0, 10, 12, 0, 7, 7, 11, 9, 9, 0, 7, 7, 0, 0, 0, 8, 0, 7, 0, 0, 0, 0, 0, 0, 7, 1, 0, 0, 0, 8, 0, 7, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 0, 4, 3, 1, 4, 0, 3, 5, 2, 0, 6, 0)), 0, 0.36), (creer((9, 0, 0, 0, 12, 0, 0, 10, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 7, 0, 7, 7, 1, 0, 7, 0, 0, 1, 0, 1, 2, 0, 1, 8, 0, 1, 0, 0, 0, 0, 0, 1, 2, 11, 1, 6, 4, 0, 0, 0, 0, 3, 0, 4)), 1, 5.19), (creer((10, 0, 9, 11, 12, 9, 0, 10, 7, 7, 0, 0, 0, 7, 7, 7, 0, 0, 8, 0, 0, 8, 0, 0, 0, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 1, 0, 1, 1, 1, 0, 1, 1, 3, 1, 4, 2, 3, 5, 0, 4, 6, 0)), 0, 0.33), (creer((0, 12, 0, 0, 0, 0, 0, 10, 7, 7, 0, 8, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 5, 7, 7, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 1, 0, 0, 1, 8, 0, 1, 0, 0, 0, 0, 2, 6, 1, 0, 0, 0, 0, 4, 0, 4, 0, 0, 0)), 0, -1.15), (creer((0, 12, 0, 0, 0, 0, 0, 0, 7, 9, 11, 10, 0, 7, 7, 0, 0, 7, 8, 0, 0, 8, 10, 0, 0, 5, 9, 0, 7, 0, 0, 0, 5, 0, 1, 7, 1, 0, 0, 2, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 3, 1, 1, 0, 3, 4, 0, 0, 0, 0, 6, 0)), 0, -2.86), (creer((10, 0, 9, 0, 0, 0, 12, 0, 0, 7, 7, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 4, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 4, 8, 0, 2, 0, 0, 0, 0, 0, 0, 6, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)), 0, 2.51), (creer((0, 0, 0, 0, 10, 0, 12, 0, 7, 7, 7, 3, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 1, 0, 6, 0, 1, 1, 1, 0, 0, 0, 0, 4, 0, 0, 0)), 0, 0.00), (creer((10, 0, 9, 0, 10, 0, 12, 0, 7, 7, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 1, 8, 7, 3, 1, 0, 0, 0, 5, 0, 0, 1, 2, 0, 0, 0, 0, 1, 1, 4, 2, 0, 0, 0, 4, 6, 0)), 1, 3.44), (creer((0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 12, 8, 0, 0, 7, 0, 0, 7, 0, 7, 11, 7, 1, 7, 0, 1, 7, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 10, 3, 0, 1, 0, 0, 0, 0, 4, 6, 5, 3, 0, 4)), 0, 0.87), (creer((0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0, 0, 7, 7, 0, 0, 0, 1, 0, 7, 0, 0, 0, 1, 0, 0, 8, 1, 0, 0, 1, 0, 0, 0, 2, 6, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 0, 1.37), (creer((0, 0, 10, 0, 9, 10, 12, 9, 7, 0, 0, 0, 11, 7, 0, 7, 0, 7, 0, 0, 7, 0, 7, 1, 0, 0, 8, 7, 2, 0, 1, 0, 0, 0, 1, 3, 8, 0, 0, 0, 0, 1, 0, 0, 1, 2, 0, 0, 1, 0, 5, 0, 3, 1, 4, 0, 0, 0, 0, 0, 0, 0, 4, 6)), 1, -0.82), (creer((0, 8, 0, 0, 0, 0, 0, 10, 7, 0, 9, 0, 0, 0, 12, 0, 0, 8, 0, 0, 11, 0, 0, 7, 0, 0, 0, 0, 0, 4, 0, 2, 0, 0, 9, 1, 0, 0, 0, 7, 0, 0, 1, 0, 5, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 4, 6, 0)), 0, -6.01), (creer((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 7, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 7, 10, 0, 7, 0, 0, 0, 10, 7, 0, 9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 3, 3, 0, 0, 0, 1, 0, 0, 4, 1, 0, 0, 4, 0, 0, 0, 0, 6, 0)), 1, -0.56), (creer((10, 0, 0, 0, 0, 0, 0, 10, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 0, 9, 12, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 2, 0, 0, 7, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 7, 1, 0, 0, 0, 0, 0, 0, 6, 0)), 1, 0.97), (creer((10, 0, 9, 11, 12, 10, 0, 0, 7, 7, 7, 0, 0, 0, 7, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1, 0, 1, 0, 7, 0, 1, 2, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 1, 6, 4, 0, 3, 0, 0, 4, 0, 0)), 0, 1.78), (creer((10, 0, 9, 0, 12, 0, 0, 10, 7, 7, 7, 7, 0, 7, 9, 7, 0, 0, 8, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 4, 2, 3, 0, 0, 0, 6, 0)), 1, -1.18), (creer((0, 0, 0, 0, 0, 0, 12, 0, 0, 7, 0, 0, 10, 0, 7, 7, 0, 9, 8, 10, 0, 0, 0, 0, 7, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 0, 1, 0, 0, 0, 1, 0, 4, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 3, 1, 0, 0, 6, 0, 0, 0, 0, 4)), 0, -1.60), (creer((0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 10, 0, 12, 0, 7, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 7, 11, 0, 0, 7, 0, 5, 0, 0, 0, 0, 7, 0, 1, 0, 0, 3, 0, 0, 1, 1, 0, 1, 0, 0, 4, 1, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 0, -0.62), (creer((0, 0, 0, 8, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 1, 0, 12, 0, 0, 1, 0, 0, 0, 0, 2, 0, 4, 0, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)), 0, 0.00), (creer((0, 10, 0, 0, 12, 0, 8, 0, 4, 1, 0, 8, 0, 0, 0, 0, 0, 7, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 0, 0, 1, 0, 0, 1, 1, 0, 3, 0, 0, 0, 0, 0, 3, 0, 4, 6, 0, 10)), 1, -0.68)]
"""for elt in base_entrainement:
    afficher(elt[0])
param = entrainement2(base_entrainement) #environ 30min de temps de calcul
print(param)
W = [param[i] for i in range(len(param))]"""
while 1:
    afficher(chessboard)
    if partie.count(cle_actuelle) == 3:
        print("nulle")
        exit()
    echequiers = [[[], []], [[], []]]
    coup = choix_coup_b(chessboard, infos, 0, "racine", cle_actuelle, "1")
    print(tour, coup, time.time() - temps, compteur[0], compteur[1], (time.time() - temps) / compteur[1], temps2[0] / (time.time() - temps))
    temps = time.time()
    compteur = [0, 0]
    temps2 = [0]
    cle_actuelle = cle_virtuelle(cle_actuelle, coup)
    partie.append(cle_actuelle)
    chessboard = recherche(cle_actuelle, 1)[1][1]
    infos = informations_virtuelles(coup, infos)
    afficher(chessboard)
    if partie.count(cle_actuelle) == 3:
        print("nulle")
        exit()
    echequiers = [[[], []], [[], []]]
    coup = choix_coup_n(chessboard, infos, 0, "racine", cle_actuelle, "1")
    print(tour, coup, time.time() - temps, compteur[0], compteur[1], (time.time() - temps) / compteur[1], temps2[0] / (time.time() - temps))
    compteur = [0, 0]
    temps2 = [0]
    temps = time.time()
    cle_actuelle = cle_virtuelle(cle_actuelle, coup)
    partie.append(cle_actuelle)
    chessboard = recherche(cle_actuelle, 0)[1][1]
    tour += 1