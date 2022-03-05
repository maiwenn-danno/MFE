import numpy as np
import copy


class Prediction:
    # Contient les informations sur Phi qui peuvent être retirées des réponses aux questions
    # --> Valeurs fixées ou valeurs possibles pour les Phi[k,l]
    def __init__(self,n,p,dico_val_fixes):
        self.n=n
        self.p=p
        self.niveaux_de_diff=[round(i/(p-1),2) for i in range(p)] #[0,...,p-1]
        self.dico_valeurs_fixes=copy.deepcopy(dico_val_fixes)
        self.dico_valeurs_possibles=self.create_dico_valeurs_possibles(dico_val_fixes)

    def get_val_fixes(self):
        return self.dico_valeurs_fixes

    def get_val_possibles(self):
        return self.dico_valeurs_possibles

    def create_dico_valeurs_possibles(self,dico_val_fixes):
        dico_valeurs_possibles=dict()
        for l in range(self.n):
            for c in range(self.n):
                if (l,c) in dico_val_fixes.keys():
                    dico_valeurs_possibles[(l,c)]=dico_val_fixes[(l,c)]
                else:
                    dico_valeurs_possibles[(l,c)]=set(self.niveaux_de_diff)
        return dico_valeurs_possibles
    
    def cleaning(self):
        for key in self.dico_valeurs_possibles.keys():
            if type(self.dico_valeurs_possibles[key])==set and len(self.dico_valeurs_possibles[key]) == 1:
                if key not in self.dico_valeurs_fixes.keys():
                    self.dico_valeurs_fixes[key]=list(self.dico_valeurs_possibles[key])[0]
                    self.dico_valeurs_possibles[key]=list(self.dico_valeurs_possibles[key])[0]
    
    def update_from_c_equal(self,liste_contraintes_equal):
        res=False #y a t'il eu une update
        for c in liste_contraintes_equal:
            s1=(c[0][0],c[0][1]) # séquence 1
            s2=(c[1][0],c[1][1]) # séquence 2
            if s1 in self.dico_valeurs_fixes.keys() and s2 not in self.dico_valeurs_fixes.keys():
                diff=self.dico_valeurs_fixes[s1]
                self.dico_valeurs_fixes[s2]=diff
                self.dico_valeurs_possibles[s2]=diff
                res=True
            elif s2 in self.dico_valeurs_fixes.keys() and s1 not in self.dico_valeurs_fixes.keys():
                diff=self.dico_valeurs_fixes[s2]
                self.dico_valeurs_fixes[s1]=diff
                self.dico_valeurs_possibles[s1]=diff
                res=True
            elif s2 not in self.dico_valeurs_fixes.keys() and s1 not in self.dico_valeurs_fixes.keys(): 
                # cas où aucun des deux n'est fixé
                res=self.update_from_c_equal_3(s1,s2)
        return res

    def update_from_c_equal_3(self,s1,s2):
        res=False
        intersection=self.dico_valeurs_possibles[s1]&self.dico_valeurs_possibles[s2]
        if self.dico_valeurs_possibles[s1]!=intersection:
            self.dico_valeurs_possibles[s1]=copy.deepcopy(intersection)
            res=True
        if self.dico_valeurs_possibles[s2]!=intersection:
            self.dico_valeurs_possibles[s2]=copy.deepcopy(intersection)
            res=True
        return res

    def update_from_c_diff_1(self,s1,s2):
        res=False
        borne_inf=self.dico_valeurs_fixes[s1]
        val_poss=self.value_possibles(borne_inf,2)
        if len(val_poss)==1:
            self.dico_valeurs_fixes[s2]=val_poss[0]
            self.dico_valeurs_possibles[s2]=val_poss[0]
            res=True
        elif len(val_poss)>1:
            new_value=set(val_poss)&self.dico_valeurs_possibles[s2] # intersection
            if self.dico_valeurs_possibles[s2]!=new_value:
                self.dico_valeurs_possibles[s2]=new_value # update
                res=True
        return res

    def update_from_c_diff_2(self,s1,s2):
        res=False
        borne_sup=self.dico_valeurs_fixes[s2]
        val_poss=self.value_possibles(-1,borne_sup)
        if len(val_poss)==1:
            self.dico_valeurs_fixes[s1]=val_poss[0]
            self.dico_valeurs_possibles[s1]=val_poss[0]
            res=True
        elif len(val_poss)>1:
            new_value=set(val_poss)&self.dico_valeurs_possibles[s1] # intersection
            if self.dico_valeurs_possibles[s1]!=new_value:
                self.dico_valeurs_possibles[s1]=new_value # update
                res=True
        return res

    def update_from_c_diff_3(self,s1,s2):
        res=False
        val_1=np.array(list(self.dico_valeurs_possibles[s1]))
        val_2=np.array(list(self.dico_valeurs_possibles[s2]))
        val_1_new=val_1[val_1<np.max(val_2)]
        val_2_new=val_2[val_2>np.min(val_1)]
        if set(val_1)!=set(val_1_new):
            self.dico_valeurs_possibles[s1]=set(val_1_new)
            res=True
        if set(val_2)!=set(val_2_new):
            self.dico_valeurs_possibles[s2]=set(val_2_new)
            res=True
        return res

    def update_from_c_diff(self,liste_contraintes_diff):
        res=False #y a t'il eu une update sur un des deux dico
        for c in liste_contraintes_diff:
            s1=(c[0][0],c[0][1]) # séquence 1
            s2=(c[1][0],c[1][1]) # séquence 2
            # contrainte Phi(s1_c1,s1_c2)<Phi(s2_c1,s2_c2)
            if s1 in self.dico_valeurs_fixes.keys() and s2 not in self.dico_valeurs_fixes.keys():
                res=self.update_from_c_diff_1(s1,s2)
            elif s2 in self.dico_valeurs_fixes.keys() and s1 not in self.dico_valeurs_fixes.keys():
                res=self.update_from_c_diff_2(s1,s2)
            elif s2 not in self.dico_valeurs_fixes.keys() and s1 not in self.dico_valeurs_fixes.keys(): # aucun des deux n'a une valeur fixée
                res=self.update_from_c_diff_3(s1,s2)
        return res

    def update(self,liste_contraintes_equal,liste_contraintes_diff):
        # Compléter dico_valeurs_fixes et dico_valeurs_possibles si de nouvelles valeurs peuvent être fixées/précisées
        res=True
        while res:
            for fix in self.dico_valeurs_fixes.keys():
                self.dico_valeurs_possibles[fix]=self.dico_valeurs_fixes[fix]
            res1=self.update_from_c_equal(liste_contraintes_equal)
            res2=self.update_from_c_diff(liste_contraintes_diff)
            self.cleaning() # si 1 seule valeur possible => dans valeur fixe
            if res1==False and res2==False:
                res=False

    def value_possibles(self,borne_inf,borne_sup):
        # Compte le nombre de niveaux de difficultés qui sont possibles, entre borne inf et borne sup (non inclus)
        value_possibles=[]
        for diff in self.niveaux_de_diff:
            if diff>borne_inf and diff<borne_sup:
                value_possibles.append(diff)
        return value_possibles