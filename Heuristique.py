import numpy as np
import random as rd
import copy
from Phi_class import *
from Question_simulation import *
from Question_DM import *

class Heuristique:
    def __init__(self,n,p,prediction,liste_contraintes_equal,liste_contraintes_diff,contexte,q_type,nb_quest_exact,max_nb_biais,max_biais,nb_Phi_seuil,nb_Phi_max,nb_it_max,Phi_DM,type="heuristique",Print=False):
        self.n=n
        self.p=p
        self.prediction=copy.deepcopy(prediction)
        self.liste_contraintes_equal=copy.deepcopy(liste_contraintes_equal)
        self.liste_contraintes_diff=copy.deepcopy(liste_contraintes_diff)
        self.contexte=contexte
        self.liste_questions=copy.deepcopy(contexte.get_liste_questions())
        self.q_type=q_type
        self.nb_quest_exact=nb_quest_exact
        self.max_nb_biais=max_nb_biais
        self.max_biais=max_biais
        self.nb_Phi_seuil=nb_Phi_seuil
        self.nb_Phi_max=nb_Phi_max
        self.nb_it_max=nb_it_max
        self.Phi_DM=Phi_DM
        self.stockage_all_Phi=False
        self.nb_questions=0
        self.Phi_possibles=[]
        self.nb_sol_estimate=0
        self.Print=Print # True if we want to print details of each question

        if self.Print:
            if type=="heuristique":
                print("\n ------- Début heuristique ------- ")
            else:
                print("\n ------- Début Random questioning ------- ")

        self.estimate_nb_Phi_possibles()
        self.init_Phi_possibles()

        if type=="heuristique":
            # Heuristique qui choisit itérativement la meilleure question à poser
            self.poser_quest_heuristique()
        else:
            # Sélection random de la question à poser
            self.poser_quest_random()

    def init_Phi_possibles(self):
        # Chercher solutions admissibles 
        if self.nb_sol_estimate <= self.nb_Phi_seuil:
            self.stockage_all_Phi=True
            self.Phi_possibles=self.generate_all_Phi_possibles()
        else:
            self.Phi_possibles=self.generate_Phi_possibles([])
    
    def estimate_nb_Phi_possibles(self):
        dico_valeurs_fixes=self.prediction.get_val_fixes()
        dico_valeurs_possibles=self.prediction.get_val_possibles()
        nb_Phi_possibles=1
        for crit1 in range(self.n):
            for crit2 in range(self.n):
                if (crit1,crit2) in dico_valeurs_fixes.keys():
                    nb_Phi_possibles*=1
                else:
                    if self.constrained_equal(crit1,crit2):
                        # si Phi[(crit1,crit2)] doit être égal à un Phi[(i,j)] dont les nb de possibilités ont déjà été comptées
                        nb_Phi_possibles*=1
                    else:
                        nb_Phi_possibles*=len(dico_valeurs_possibles[(crit1,crit2)])
        if self.Print:
            print("\n Estimation : nb de solutions admissibles : "+str(nb_Phi_possibles))
        self.nb_sol_estimate=nb_Phi_possibles

    def constrained_equal(self,crit1,crit2):
        # parcourt les contraintes d'égalités
        # regarde s'il y a une contrainte d'égalité entre (crit1,crit2) et (i,j) où i<crit1 OU (i=crit1 et j<crit2)
        res=False
        for [seq1,seq2] in self.liste_contraintes_equal:
            if seq1==(crit1,crit2):
                if seq2[0]<crit1 or (seq2[0]==crit1 and seq2[1]<crit2):
                    res=True
            elif seq2==(crit1,crit2):
                if seq1[0]<crit1 or (seq1[0]==crit1 and seq1[1]<crit2):
                    res=True
        return res

    def generate_all_Phi_possibles(self):
        if self.Print:
            print("--> génération de TOUTES les solutions admissibles")
        dico_valeurs_fixes=self.prediction.get_val_fixes()
        dico_valeurs_possibles=self.prediction.get_val_possibles()
        Phi_possibles_in_list=[]
        Phi_possibles_in_list.append([-1 for i in range(self.n**2)])
        for l in range(self.n):
            for c in range(self.n):
                if (l,c) in dico_valeurs_fixes.keys():
                    for liste in Phi_possibles_in_list:
                        liste[c+l*self.n]=dico_valeurs_fixes[(l,c)]
                else: # if plusieurs valeurs possibles ou pas présent dans le dico
                    values=list(dico_valeurs_possibles[(l,c)])
                    # TO DO : adapter pour que si contrainte == ou < avec une valeur déjà fixée => à prendre en compte dans values
                    old=Phi_possibles_in_list
                    Phi_possibles_in_list=[]
                    for liste in old:
                        for i in range(len(values)):
                            new_list=copy.deepcopy(liste)
                            new_list[c+l*self.n]=values[i]
                            Phi_possibles_in_list.append(new_list)
        Phi_possibles=[]
        for liste in Phi_possibles_in_list:
            Phi=Phi_class(self.n,self.p,"fixe",0, [],liste)
            if Phi.check_contraintes(self.liste_contraintes_equal,self.liste_contraintes_diff,self.prediction.get_val_fixes())==True:
                Phi_possibles.append(Phi)
            # Exemple où une contrainte n'est pas respectée
            # contrainte Phi[(0,1)]<Phi[(0,2)] => dico valeurs possibles = { (0,1)={0,0.33,0.67}; (0,2)={0.33,0.67,1}} mais la solution avec Phi[(0,1)]=0.67 et Phi[(0,2)]=0.33 n'est pas possible
        if self.Print:
            print("nb Phi admissibles générés: "+str(len(Phi_possibles)))
        return Phi_possibles

    def generate_question(self):
        # input: liste_arr_sequences: liste avec tous les arrangements possibles de nb sequences
        # output au format [(c1,c2),(c3,c4)] si q_type="Classement_sequences" et nb_sequences=2
        best_question=[] # question la plus discriminante, c-à-d avec le plus petit espace de Phi possibles résultant (dans le pire des cas)
        best_question_nb_Phi_max=len(self.Phi_possibles)
        best_question_nb_Phi_avg=len(self.Phi_possibles)
        i=0
        for arr_sequences in self.liste_questions:
            Question=Question_simulation(self.q_type,len(arr_sequences),arr_sequences)
            Question_simul_Phi_possibles=Question.simulation(self.Phi_possibles,self.contexte.get_liste_criteres())
            if ((max(Question_simul_Phi_possibles)<best_question_nb_Phi_max) or (max(Question_simul_Phi_possibles)==best_question_nb_Phi_max and sum(Question_simul_Phi_possibles)/len(Question_simul_Phi_possibles)<best_question_nb_Phi_avg)) and sum(Question_simul_Phi_possibles)/len(Question_simul_Phi_possibles)>0:
                i+=1
                best_question_nb_Phi_max=max(Question_simul_Phi_possibles)
                best_question_nb_Phi_avg=sum(Question_simul_Phi_possibles)/len(Question_simul_Phi_possibles)
                best_question=Question.get_sequences()
        if best_question==[]:
            print("error")
            print(i)
        if self.Print:
            print("Meilleure question avec -- Max : "+str(best_question_nb_Phi_max)+" , Avg : "+str(round(best_question_nb_Phi_avg,2)))
        return best_question

    def generate_Phi_possibles(self,pre_liste_Phi_possibles):
        # Génère nb_Phi_max solutions admissibles (sauf si on boucle trop avant de les trouver)
        liste_Phi_possibles=pre_liste_Phi_possibles
        it=0
        while it<self.nb_it_max and len(liste_Phi_possibles)<min(self.nb_sol_estimate,self.nb_Phi_max):
            new_Phi=Phi_class(self.n, self.p, "aleatoire2", 0, self.prediction)
            if new_Phi.check_contraintes(self.liste_contraintes_equal,self.liste_contraintes_diff,self.prediction.get_val_fixes())==True:
                if new_Phi not in liste_Phi_possibles:
                    liste_Phi_possibles.append(new_Phi)
            it+=1
        return liste_Phi_possibles
    
    def poser_quest_heuristique(self):        
        while self.critere_arret()==False:
            self.nb_questions+=1
            if self.Print:
                print("\n Q"+str(self.nb_questions))
            best_question=self.generate_question()
            Question=Question_DM(self.Phi_DM.get_Phi(), self.contexte.get_dico_criteres(), self.p, self.q_type,best_question,self.Print)
            new_liste_contraintes_equal,new_liste_contraintes_diff=Question.get_contraintes()
            self.liste_contraintes_equal.extend(new_liste_contraintes_equal)
            self.liste_contraintes_diff.extend(new_liste_contraintes_diff)
            if self.Phi_DM.check_contraintes(self.liste_contraintes_equal,self.liste_contraintes_diff,self.prediction.get_val_fixes())!=True:
                print(" /!\ contrainte pas compatible avec Phi_DM /!\ ")
            self.prediction.update(self.liste_contraintes_equal,self.liste_contraintes_diff)
            
            if self.stockage_all_Phi:
                # Si Phi_possibles contient tous les Phi possibles, on fait le tri dedans directement avec les nouvelles contraintes
                new_Phi_possibles=[]
                old_nb=len(self.Phi_possibles)
                for Phi in self.Phi_possibles:
                    if Phi.check_contraintes(new_liste_contraintes_equal,new_liste_contraintes_diff,{})==True:
                        new_Phi_possibles.append(Phi)
                self.Phi_possibles=new_Phi_possibles
                if self.Print:
                    print("Après la Q"+str(self.nb_questions)+", nb de solutions admissibles: "+str(len(self.Phi_possibles)))
                    print("Phi_DM toujours dans Phi_possibles? "+str(self.Phi_DM.check_Phi_DM(self.Phi_possibles))+" !")
                if len(self.Phi_possibles)==old_nb:
                    print(" -/!\- Bottleneck : impossible de trouver Phi_DM sans fixer une valeur supplémentaire")
                    break 
            else:
                # Sinon, on trie les Phi qu'on avait déjà et on en cherche de nouveaux
                self.estimate_nb_Phi_possibles()
                if self.nb_sol_estimate <= self.nb_Phi_seuil:
                    self.stockage_all_Phi=True
                    self.prediction.update(self.liste_contraintes_equal,self.liste_contraintes_diff)
                    self.Phi_possibles=self.generate_all_Phi_possibles()
                else:
                    self.stockage_all_Phi=False
                    #Tri de Phi_possibles
                    old_nb=len(self.Phi_possibles)
                    new_Phi_possibles=[]
                    for Phi in self.Phi_possibles:
                        if Phi.check_contraintes(new_liste_contraintes_equal,new_liste_contraintes_diff,self.prediction.get_val_fixes())==True:
                            new_Phi_possibles.append(Phi)
                    self.Phi_possibles=new_Phi_possibles
                    if self.Print:
                        print(str(len(self.Phi_possibles))+"/"+str(old_nb)+" Phi possibles gardés, puis génération aléatoire pour compléter")
                    self.Phi_possibles=self.generate_Phi_possibles(self.Phi_possibles)
        
                if self.Print:
                    print("Phi_DM dans Phi_possibles? "+str(self.Phi_DM.check_Phi_DM(self.Phi_possibles))+" !")    
            self.liste_questions.remove(best_question)
        
    def poser_quest_random(self):      
        while self.critere_arret()==False:
            self.nb_questions+=1
            if self.Print:
                print("\n Q"+str(self.nb_questions))
            question=rd.choice(self.liste_questions)
            Question=Question_DM(self.Phi_DM.get_Phi(), self.contexte.get_dico_criteres(), self.p, self.q_type,question,self.Print)
            new_liste_contraintes_equal,new_liste_contraintes_diff=Question.get_contraintes()
            self.liste_contraintes_equal.extend(new_liste_contraintes_equal)
            self.liste_contraintes_diff.extend(new_liste_contraintes_diff)
            if self.Phi_DM.check_contraintes(self.liste_contraintes_equal,self.liste_contraintes_diff,self.prediction.get_val_fixes())!=True:
                print(" /!\ contrainte pas compatible avec Phi_DM /!\ ")
            self.prediction.update(self.liste_contraintes_equal,self.liste_contraintes_diff)
            
            if self.stockage_all_Phi:
                # Si Phi_possibles contient tous les Phi possibles, on fait le tri dedans directement avec les nouvelles contraintes
                new_Phi_possibles=[]
                for Phi in self.Phi_possibles:
                    if Phi.check_contraintes(new_liste_contraintes_equal,new_liste_contraintes_diff,{})==True:
                        new_Phi_possibles.append(Phi)
                self.Phi_possibles=new_Phi_possibles
                if self.Print:
                    print("Après la Q"+str(self.nb_questions)+", nb de solutions admissibles: "+str(len(self.Phi_possibles)))
                    print("Phi_DM toujours dans Phi_possibles? "+str(self.Phi_DM.check_Phi_DM(self.Phi_possibles))+" !")
            else:
                # Sinon, on trie les Phi qu'on avait déjà et on en cherche de nouveaux
                self.estimate_nb_Phi_possibles()
                if self.nb_sol_estimate <= self.nb_Phi_seuil:
                    self.stockage_all_Phi=True
                    self.prediction.update(self.liste_contraintes_equal,self.liste_contraintes_diff)
                    self.Phi_possibles=self.generate_all_Phi_possibles()
                else:
                    self.stockage_all_Phi=False
                    #Tri de Phi_possibles
                    old_nb=len(self.Phi_possibles)
                    new_Phi_possibles=[]
                    for Phi in self.Phi_possibles:
                        if Phi.check_contraintes(new_liste_contraintes_equal,new_liste_contraintes_diff,self.prediction.get_val_fixes())==True:
                            new_Phi_possibles.append(Phi)
                    self.Phi_possibles=new_Phi_possibles
                    if self.Print:
                        print(str(len(self.Phi_possibles))+"/"+str(old_nb)+" Phi possibles gardés, puis génération aléatoire pour compléter")
                    self.Phi_possibles=self.generate_Phi_possibles(self.Phi_possibles)
        
                if self.Print:
                    print("Phi_DM dans Phi_possibles? "+str(self.Phi_DM.check_Phi_DM(self.Phi_possibles))+" !")    
            self.liste_questions.remove(question)
            if len(self.liste_questions)==0:
                print(" -/!\- Bottleneck : Aucune question ne permet de déterminer Phi_DM")
                break 
            
    def critere_arret(self):
        # return True si l'heuristique doit s'arrêter
        if self.nb_questions<self.nb_quest_exact:
            if len(self.Phi_possibles)>1:
                reponse=False
            else: # if =1
                reponse=True
        else: 
            reponse=self.precision()
        return reponse

    def precision(self):
        # Return True si les valeurs de Phi sont suffisamment fixées
        # c-à-d si max "max_nb_biais" séquences ont plus de 1 valeur possible, avec max max_biais valeurs possibles chacun
        reponse = False
        dico_fixes=self.prediction.get_val_fixes()
        dico_possibles=self.prediction.get_val_possibles()
        if len(dico_fixes)==self.n**2:
            reponse=True
        elif len(dico_fixes)>=self.n**2-self.max_nb_biais:
            biais_max=max([len(i) for i in dico_possibles.values() if type(i)==set])
            if biais_max <= self.max_biais:
                nb_biais=len(dico_possibles)-len(dico_fixes)
                if nb_biais<=self.max_nb_biais:
                    reponse=True
        return reponse

    def get_nb_questions(self):
        return self.nb_questions

    def get_Phi_possibles(self):
        return self.Phi_possibles

    def get_prediction(self):
        return self.prediction
    
    def get_stockage_all_Phi(self):
        return self.stockage_all_Phi

    def get_contraintes_equal(self):
        return self.liste_contraintes_equal

    def get_contraintes_diff(self):
        return self.liste_contraintes_diff