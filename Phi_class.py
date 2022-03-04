import numpy as np
import random as rd


class Phi_class:
    def __init__(self, n, p=2, mode="aleatoire", k=0, prediction=[], liste_valeurs=[]):

        self.n = n
        self.p = p
        self.mode=mode
        # initialisation Phi
        if self.mode == "AI":  # Si on construit la Matrice de l'AI (qui représente celle du DM)
            self.k = k
            self.Phi = self.constr_Phi_DM_discret()
        elif self.mode=="aleatoire2":
            self.dico_valeurs_fixes=prediction.get_val_fixes()
            self.dico_valeurs_possibles=prediction.get_val_possibles()
            self.Phi = self.generate_matrix()
        else: # mode == "fixe"
            self.liste=liste_valeurs
            self.Phi=self.liste_to_matrices(self.liste)

    def generate_matrix(self):
        Phi = np.zeros((self.n, self.n))
        for l in range(self.n):
            for c in range(self.n):
                if (l,c) in self.dico_valeurs_fixes.keys():
                    Phi[l,c]=self.dico_valeurs_fixes[(l,c)]
                else:
                    Phi[l,c]=rd.sample(self.dico_valeurs_possibles[(l,c)],1)[0]
        return Phi

    def liste_to_matrices(self, liste):
        # Construit une matrice nxn avec les n**2 contenues dans liste
        Matrice = np.zeros((self.n, self.n))
        for ligne in range(self.n):
            for column in range(self.n):
                Matrice[ligne, column] = liste[column + ligne * self.n]
        return Matrice

    def get_Phi(self):
        return self.Phi

    def get_liste(self):
        if self.mode==False:
            return self.liste
        else:
            return []

    #rd.seed(12)

    def constr_Phi_DM_discret(self):
        # Construiction de la matrice Phi avec p niveaux de valeurs et k valeurs non-nules => Phi(phi,l) sur la diagonale et Phi(k,l) ailleurs
        # valeurs: 0, 1/(p-1), 2/(p-1), ..., 1
        if type(self.p) == int:
            possible_values = [round(i / (self.p - 1),2) for i in range(1, max(2, self.p))]
        else:
            possible_values = [1]
        Phi_DM = np.zeros((self.n, self.n))
        possible_indexes = []
        for i in range(self.n):
            for j in range(self.n):
                possible_indexes.append((i, j))
        for i in range(self.k):
            index = rd.choice(possible_indexes)
            Phi_DM[index[0], index[1]] = rd.choice(possible_values)
            possible_indexes.remove(index)
        return Phi_DM

    def check_contraintes(self, liste_contraintes_equal, liste_contraintes_diff, dico_valeurs_fixes):
        res=self.check_contraintes_valeurs(dico_valeurs_fixes)
        if res==True:
            res = self.check_contraintes_equal(liste_contraintes_equal)
            if res == True:
                res = self.check_contraintes_diff(liste_contraintes_diff)
        return res

    def check_contraintes_valeurs(self,dico_contraintes):
        res=True
        for indices_fixes in dico_contraintes.keys():
            if res==True:
                if self.Phi[indices_fixes[0],indices_fixes[1]] != dico_contraintes[indices_fixes]:
                    res=False
        return res

    def check_contraintes_equal(self, liste_contraintes):
        res = True
        for contrainte in liste_contraintes:
            if res == True:
                if self.Phi[contrainte[0][0], contrainte[0][1]] != self.Phi[contrainte[1][0], contrainte[1][1]]:
                    res = False
        return res

    def check_contraintes_diff(self, liste_contraintes):
        res = True
        for contrainte in liste_contraintes:
            if res == True:
                if self.Phi[contrainte[0][0], contrainte[0][1]] >= self.Phi[contrainte[1][0], contrainte[1][1]]:
                    res = False
        return res

    def check_Phi_DM(self,liste_Phi_possibles):
        res=False
        if self.mode=='AI':
            for Phi in liste_Phi_possibles:
                Phi_genere=Phi.get_Phi()
                if (Phi_genere==self.Phi).all():
                    res=True
        return res

        ## On ne garde que les parties des listes deja testees qui nous intéressent (cf celle à random)
        #listes_deja_testees_random=[]
        #for liste_deja_testee in listes_deja_testees:
        #    liste_cut= [liste_deja_testee[i] for i in range((self.n) ** 2) if i not in indices_Phi_fixes]
        #    if liste_cut not in listes_deja_testees_random:
        #        listes_deja_testees_random.append(liste_cut)
        """if len(listes_deja_testees_random)<nb_random**2: # Si on n'a pas déjà tout testé
            new_list_random=False
            if liste_random not in listes_deja_testees_random:
                new_list_random=True
            while not new_list_random:
                liste_random_not_scaled = np.random.randint(0, self.p, nb_random)
                liste_random = [i / (self.p-1) for i in liste_random_not_scaled]
                if liste_random not in listes_deja_testees_random:
                    new_list_random=True"""
        