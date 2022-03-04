import numpy as np
from Sequence import *

class Question_DM:
    # n= Nombre de critères
    # Phi_DM: matrice du DM
    def __init__(self, Phi_DM, dico_criteres, p, q_type, parameters,Print):

        self.Phi_DM=Phi_DM
        self.dico_criteres=dico_criteres
        self.p=p
        self.q_type = q_type
        self.param=parameters
        self.liste_contraintes_equal=[]
        self.liste_contraintes_diff=[]
        self.dico_valeurs_fixes={}
        self.Print=Print

        self.poser_question()

    def poser_question(self):
        if self.q_type == "Sequences_plus_difficiles" :
            if self.valid_sequences(self.param):
                if self.Print:
                    print("====> Quelle(s) séquences sont les plus difficiles parmi "+str([self.param[i].lettres for i in range(len(self.param))])+" ?")
                self.question_type_A()
            else:
                print("Mauvaise question")

        elif self.q_type == "Classement_sequences" :
            if self.valid_sequences(self.param):
                if self.Print:
                    print("====> Classement des séquences: "+str([self.param[i].lettres for i in range(len(self.param))])+" par ordre croissant de difficulté?")
                self.question_type_B()
            else:
                print("Mauvaise question")

        elif self.q_type == "Criteres_plus_difficiles" :
            if self.Print:
                print("====> Quels critères parmi "+str(self.param)+" sont les plus difficiles à améliorer depuis 0?");
            if self.valid_criteres(self.param):
                self.question_type_C()
            else:
                print("Mauvaise question")

        elif self.q_type == "Classement_criteres" :
            if self.Print:
                print("====> Classement des critères "+str(self.param)+" par ordre croissant de difficulté?")
            if self.valid_criteres(self.param):
                self.question_type_D()
            else:
                print("Mauvaise question")

        elif self.q_type == "Niveaux_diff_criteres":
            if self.Print:
                print("====> A quels niveaux de difficulté les critères "+str(self.param)+" appartiennent sur une échelle de 0 à 1 à "+str(self.p)+" niveaux ?")
            if self.valid_criteres(self.param):
                self.question_type_E()
            else:
                print("Mauvaise question")

        elif self.q_type == "Sequences_independantes" :
            if self.valid_sequences_diff(self.param):
                if self.Print:
                    print("====> Quelles séquences [k,l] parmi "+str([self.param[i].lettres for i in range(len(self.param))])+" sont aussi difficiles que les séquences [l,l] correspondantes ?")
                self.question_type_F()
            else:
                print("Mauvaise question")

# ----------------- Définition des fonctions questions -------------

    def question_type_A(self):
        # Renvoie la/les séquences les plus difficiles
        # Input=param: sequences =[s1,s2,...]=[(s1_1,s1_2),(s2_1,s2_2),...] où si est un objet de la classe Sequence
        sequences=self.param
        diff_seq=np.array(self.difficultes_sequences(sequences))
        diff_max=max(diff_seq)
        diff_max_index=np.where(diff_seq==diff_max)[0]
        diff_non_max_index=np.where(diff_seq<diff_max)[0]
        sequences_max=[]
        sequences_non_max=[]
        for index_max in diff_max_index:
            sequences_max.append(sequences[index_max])
        if len(sequences_max)==len(sequences): # si toutes les séquences ont la meme difficulté:
            if self.Print:
                print("Aucune")
        else:
            seq_max_lettres=[]
            for i in range(len(sequences_max)):
                seq_max_lettres.append(sequences_max[i].get_lettres())
            if self.Print:
                print(seq_max_lettres)
            for index_non_max in diff_non_max_index:
                sequences_non_max.append(sequences[index_non_max])
        for sequ_max in sequences_max:
            for sequ_max_2 in sequences_max:
                if sequ_max!=sequ_max_2:
                    contrainte_equal=[sequ_max.indices,sequ_max_2.indices]
                    if (contrainte_equal not in self.liste_contraintes_equal) and ([contrainte_equal[1],contrainte_equal[0]] not in self.liste_contraintes_equal):
                        self.liste_contraintes_equal.append(contrainte_equal)
            if len(sequences_max)!=len(sequences):
                for sequ_non_max in sequences_non_max:
                    contrainte_diff=[sequ_non_max.indices,sequ_max.indices]
                    if contrainte_diff not in self.liste_contraintes_diff:
                        self.liste_contraintes_diff.append(contrainte_diff)

    def question_type_B(self):
        # Classe les séquences par ordre croissant de difficulté
        # Input = param: liste de sequences : [s1,s2,...]=[(s1_1,s1_2),(s2_1,s2_2),...]
        sequences=self.param
        diff_seq=self.difficultes_sequences(sequences)
        valeurs_diff=list(set(diff_seq)) #pour supprimer les doublons de difficulté
        classement_indexes=[]
        while len(valeurs_diff)!=0:
            diff_min=min(valeurs_diff)
            diff_min_index=np.where(np.array(diff_seq)==diff_min)[0]
            seq_diff_min_lettres, seq_diff_min_indices=[],[]
            for index in diff_min_index:
                seq_diff_min_lettres.append(sequences[index].lettres)
                seq_diff_min_indices.append(sequences[index].indices)
            if self.Print:
                print(seq_diff_min_lettres)
            classement_indexes.append(seq_diff_min_indices)
            valeurs_diff.remove(diff_min)
        for classe in classement_indexes:
                for i_seq in range(len(classe)-1):
                    contrainte_equal=[classe[i_seq],classe[i_seq+1]]
                    if (contrainte_equal not in self.liste_contraintes_equal) and ([contrainte_equal[1],contrainte_equal[0]] not in self.liste_contraintes_equal):
                        self.liste_contraintes_equal.append(contrainte_equal)
                for classe_2 in classement_indexes:
                    if classement_indexes.index(classe) < classement_indexes.index(classe_2):
                        contrainte_diff=[classe[0],classe_2[0]]
                        if contrainte_diff not in self.liste_contraintes_diff:
                            self.liste_contraintes_diff.append(contrainte_diff)

    def question_type_C(self):
        # Renvoie les critères avec la plus grande difficulté Phi(vide,k)
        # Input: liste de critères
        criteres=self.param
        sequences_fictives=[]
        for critere in criteres:
            sequences_fictives.append(Sequence(critere,critere,self.dico_criteres))
        diff_criteres=self.difficultes_sequences(sequences_fictives)

        diff_max_index=np.where(np.array(diff_criteres)==max(diff_criteres))[0]
        crit_max=[]
        for index in diff_max_index:
            crit_max.append(criteres[index])
        crit_max_lettres=list(set(crit_max))
        if self.Print:
            print(crit_max_lettres)
        crit_max_indices=self.criteres_to_indexes(crit_max_lettres)
        for i_max in range(len(crit_max_indices)-1):
            contrainte_equal=[(crit_max_indices[i_max],crit_max_indices[i_max]),(crit_max_indices[i_max+1],crit_max_indices[i_max+1])]
            if (contrainte_equal not in self.liste_contraintes_equal) and ([contrainte_equal[1],contrainte_equal[0]] not in self.liste_contraintes_equal):
                self.liste_contraintes_equal.append(contrainte_equal)

        crit_inf_indices=[]
        for critere in list(set(criteres)):
            if critere not in crit_max_lettres:
                crit_inf_indices.append(self.dico_criteres[critere])
        for i_inf in range(len(crit_inf_indices)):
            contrainte_diff=[(crit_inf_indices[i_inf],crit_inf_indices[i_inf]),(crit_max_indices[0],crit_max_indices[0])]
            if contrainte_diff not in self.liste_contraintes_diff:
                self.liste_contraintes_diff.append(contrainte_diff)

    def question_type_D(self):
        # Renvoie les critères triées par ordre croissant de difficulté depuis 0(égalités possibles)
        # Input: liste de critères
        criteres=self.param
        sequences_fictives=[]
        for critere in criteres:
            sequences_fictives.append(Sequence(critere,critere,self.dico_criteres))
        diff_criteres=self.difficultes_sequences(sequences_fictives)
        valeurs_diff=list(set(diff_criteres)) #pour supprimer les doublons de difficulté
        classement=[]
        classement_indexes=[]
        while len(valeurs_diff)!=0:
            diff_min=min(valeurs_diff)
            diff_min_index=np.where(np.array(diff_criteres)==diff_min)[0]
            crit_diff_min=[]
            for index in diff_min_index:
                crit_diff_min.append(criteres[index])
            crit_diff_min=list(set(crit_diff_min))
            crit_diff_min_index=self.criteres_to_indexes(crit_diff_min)
            classement.append(crit_diff_min)
            classement_indexes.append(crit_diff_min_index)
            valeurs_diff.remove(diff_min)
        if self.Print:
            print(classement)
        for classe in classement_indexes:
            for i_crit in range(len(classe)-1):
                # Contrainte d'égalité de difficulté entre 2 séquences d'une même classe
                contrainte_equal= [(classe[i_crit],classe[i_crit]),(classe[i_crit+1],classe[i_crit+1])]
                if (contrainte_equal not in self.liste_contraintes_equal) and ([contrainte_equal[1],contrainte_equal[0]] not in self.liste_contraintes_equal):
                    self.liste_contraintes_equal.append(contrainte_equal)
            for classe_2 in classement_indexes:
                if classement_indexes.index(classe) < classement_indexes.index(classe_2):
                    # Contraintes de différence entre 2 séquences de 2 classes différentes
                    for i_crit in range(len(classe)):
                        for i_crit_2 in range(len(classe_2)):
                            contrainte_diff=[(classe[i_crit],classe[i_crit]),(classe_2[i_crit_2],classe_2[i_crit_2])]
                            if contrainte_diff not in self.liste_contraintes_diff:
                                self.liste_contraintes_diff.append(contrainte_diff)

    def question_type_E(self):
        # Attribue à chaque critère un niveau de difficulté sur une échelle de 0 à 1 à p niveaux
        # Input: liste de critères
        criteres=self.param
        echelle_difficulte=[i/(self.p-1) for i in range(self.p)] #[0,...,p-1]
        for critere in criteres:
            diff=self.Phi_DM[self.dico_criteres[critere],self.dico_criteres[critere]]
            if (self.dico_criteres[critere],self.dico_criteres[critere]) not in self.dico_valeurs_fixes.keys():
                self.dico_valeurs_fixes[(self.dico_criteres[critere],self.dico_criteres[critere])]=diff
        if self.Print:
            print(self.dico_valeurs_fixes)

    def question_type_F(self):
        # Renvoie des séquences [k,l] qui sont aussi difficiles que les séquences [l,l] correspondantes
        # Input=param: sequences =[s1,s2,...]=[(s1_1,s1_2),(s2_1,s2_2),...] avec deux critères différents
        sequences=self.param
        list_seq_indep=[]
        list_seq_indep_lettres=[]
        for sequence in sequences:
            if self.Phi_DM[sequence.get_indices()[0],sequence.get_indices()[1]]==self.Phi_DM[sequence.get_indices()[1],sequence.get_indices()[1]]:
                list_seq_indep.append(sequence)
                list_seq_indep_lettres.append(sequence.lettres)
        if len(list_seq_indep)==0:
            # si toutes les séquences ont la meme difficulté:
            if self.Print:
                print("Aucune")
            # On ne rajoute pas pour autant la contrainte que Phi[k,l]!=Phi[l,l] sinon le problème serait déjà résolu en binaire
            # Permet de simuler un DM qui n'arrive pas à trouver tous les cas d'indépendance.
        else:
            if self.Print:
                print(list_seq_indep_lettres)
            for sequence in list_seq_indep:
                contrainte_equal=[sequence.indices,(sequence.indices[1],sequence.indices[1])]
                if (contrainte_equal not in self.liste_contraintes_equal) and ([contrainte_equal[1],contrainte_equal[0]] not in self.liste_contraintes_equal):
                    self.liste_contraintes_equal.append(contrainte_equal)


# ---------- Fonctions de check de validité, de calcul et de conversions -----

    def valid_criteres(self, criteres):
        # Renvoie True si les critères donnés sont valides
        res=True
        for critere in criteres:
            if critere not in self.dico_criteres.keys():
                res=False
        return res

    def valid_sequences(self, sequences):
        # Renvoie True si les séquences données sont constituées de 2 critères valides  => Cf Phi(k,l) ou Phi(phi,l)
        # Input: liste de séquences
        sequences_lettres=[]
        for seq in sequences:
            sequences_lettres.append(seq.get_lettres())
        res=True
        for sequence in sequences_lettres:
            for critere in sequence:
                if critere not in self.dico_criteres.keys():
                    res=False
        return res

    def valid_sequences_diff(self, sequences):
        # Renvoie True si les séquences données sont constituées de 2 critères valides différents => Cf Phi(k,l)
        # Input: liste de séquences
        sequences_lettres=[]
        for seq in sequences:
            sequences_lettres.append(seq.get_lettres())
        res=True
        for sequence in sequences_lettres:
            for critere in sequence:
                if critere not in self.dico_criteres.keys():
                    res=False
            if sequence[0]==sequence[1]:
                res=False
        return res

    def criteres_to_indexes(self,criteres):
        # Convertit les critères en index correspondants dans liste_critères
        # input: liste de critères
        indexes=[]
        for critere in criteres:
            indexes.append(self.dico_criteres[critere])
        return indexes

    def difficultes_sequences(self,sequences):
        # Retourne la liste des difficultés des séquences
        diff_seq=[]
        if type(sequences)==tuple:
            [k,l]=sequences.indices
            diff_seq.append(self.Phi_DM[k,l])
        else:
            for sequence in sequences:
                [k,l]=sequence.indices
                diff_seq.append(self.Phi_DM[k,l])
        return diff_seq

    def get_valeurs_fixes(self):
        return self.dico_valeurs_fixes

    def get_contraintes_equal(self):
        return self.liste_contraintes_equal

    def get_contraintes_diff(self):
        return self.liste_contraintes_diff

    def get_contraintes(self):
        contraintes_equal=self.get_contraintes_equal()
        contraintes_diff=self.get_contraintes_diff()

        return contraintes_equal,contraintes_diff
