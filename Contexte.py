import numpy as np
import random as rd
from Sequence import *

class Contexte:
    # Contient les paramètres du problème
    def __init__(self,liste_criteres,nb_sequences):
        self.nb_sequences=nb_sequences
        self.liste_criteres=liste_criteres
        self.dico_criteres=self.build_dico()
        self.liste_sequences_diff_possibles=self.build_sequences(True)
        self.liste_sequences_possibles=self.build_sequences(False)
        self.liste_questions=self.build_arr_sequences()

    def build_dico(self):
        dico_criteres={}
        for critere in self.liste_criteres:
            dico_criteres[critere]=self.liste_criteres.index(critere)
        return dico_criteres

    def build_sequences(self, different=True):
        # Construit toutes les séquences de 2 critères possibles
        # different=True si les deux critères doivent être différents, different=False si pas forcément
        liste_sequences_possibles=[]
        for critere1 in self.liste_criteres:
            for critere2 in self.liste_criteres:
                seq=Sequence(critere1,critere2,self.dico_criteres)
                if different:
                    if critere1!=critere2 and seq not in liste_sequences_possibles:
                        liste_sequences_possibles.append(seq)
                else:
                    if seq not in liste_sequences_possibles:
                        liste_sequences_possibles.append(seq)
        return liste_sequences_possibles

    def build_arr_sequences(self):
        # Renvoie tous les arrangements possibles avec "nb_sequences" séquences de 2 critères par question
        # Format de l'output pour nb_sequences=2: [[(c,c),(d,d)],[(d,c),(c,d)],...]
        liste_arr_sequences_possibles=[]
        if self.nb_sequences==2 or self.nb_sequences==3:
            for seq_1 in self.liste_sequences_possibles:
                for seq_2 in self.liste_sequences_possibles:
                    if self.nb_sequences==2:
                        if seq_1.lettres!=seq_2.lettres and [seq_1,seq_2] not in liste_arr_sequences_possibles:
                            liste_arr_sequences_possibles.append([seq_1,seq_2])
                    else: #nb_sequences=3
                        for seq_3 in self.liste_sequences_possibles:
                            if seq_1.lettres!=seq_2.lettres and seq_2.lettres!=seq_3.lettres and seq_1.lettres!=seq_3.lettres and [seq_1,seq_2,seq_3] not in liste_arr_sequences_possibles:
                                liste_arr_sequences_possibles.append([seq_1,seq_2,seq_3])
        else:
            print(" /!\   Erreur: trop de séquences demandées par question   /!\  ")
        return liste_arr_sequences_possibles

    def get_liste_criteres(self):
        return self.liste_criteres

    def get_dico_criteres(self):
        return self.dico_criteres

    def get_liste_seq_diff_possibles(self):
        return self.liste_sequences_diff_possibles
    
    def get_liste_seq_possibles(self):
        return self.liste_sequences_possibles
        
    def get_liste_questions(self):
        return self.liste_questions