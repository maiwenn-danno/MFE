import numpy as np
import random as rd


class Sequence:
    # Sequence de 2 critères: améliorer le critère 2 après avoir amélioré le critère 1
    def __init__(self,crit1,crit2,dico_criteres):
        self.lettres=(crit1,crit2)
        self.indices=(dico_criteres[crit1],dico_criteres[crit2])

    def get_lettres(self):
        return self.lettres

    def get_indices(self):
        return self.indices

