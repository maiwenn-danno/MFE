import numpy as np

class Question_simulation:

    def __init__(self, q_type, nb_sequences, arr_sequences):

        self.q_type=q_type
        self.nb_sequences=nb_sequences
        self.sequences=arr_sequences # Liste de 2 ou 3 objets Sequences

    def get_sequences(self):
        return self.sequences

    def simulation(self,Phi_possibles,liste_criteres):
        if self.q_type=="Sequences_plus_difficiles":
            if self.nb_sequences==2:
                nb_Phi_possibles=self.simulation_type_A_2(Phi_possibles,liste_criteres)
            elif self.nb_sequences==3:
                nb_Phi_possibles=self.simulation_type_A_3(Phi_possibles,liste_criteres)
        if self.q_type=="Classement_sequences":
            if self.nb_sequences==2:
                nb_Phi_possibles=self.simulation_type_B_2(Phi_possibles,liste_criteres)
            elif self.nb_sequences==3:
                nb_Phi_possibles=self.simulation_type_B_3(Phi_possibles,liste_criteres)
        return nb_Phi_possibles

    def simulation_type_A_2(self,Phi_possibles,liste_criteres):
        # question: [(c1,c2),(c3,c4)]
        # Simule les 3 réponses possibles à une question de type A qui renvoie la/les séquences les + difficiles parmi 2 séquences
        # Retourne le nombre de Phi_possibles après avoir posé cette Q, pour chaque réponse possible
        [(s0_0,s0_1),(s1_0,s1_1)]=[self.sequences[0].indices,self.sequences[1].indices]
        # question_i: quelle est la séquence la plus difficile parmi 2 séquences [A,B]
        reponse=[0 for i in range(3)]
        # contient le nbre de Phi_possibles si la réponse est : [0] - B, [1] - Aucune, [2] - A
        for Phi in Phi_possibles:
            Phi=Phi.get_Phi()
            if Phi[s0_0,s0_1]<Phi[s1_0,s1_1]:
                reponse[0]+=1
            elif Phi[s0_0,s0_1]==Phi[s1_0,s1_1]:
                reponse[1]+=1
            else:
                reponse[2]+=1
        return reponse

    def simulation_type_A_3(self,Phi_possibles,liste_criteres):
        # question: [(c1,c2),(c3,c4),(c5,c6)]
        # Simule les 7 réponses possibles à une question de type A qui qui renvoie la/les séquences les + difficiles parmi 3 séquences
        # Retourne le nombre de Phi_possibles après avoir posé cette Q, pour chaque réponse possible
        [(s0_0,s0_1),(s1_0,s1_1),(s2_0,s2_1)]=[self.sequences[0].indices,self.sequences[1].indices,self.sequences[2].indices]
        # question_i: quelle est la séquence la plus difficile parmi 3 séquences [A,B,C]
        reponse=[0 for i in range(7)]
        # contient le nbre de Phi_possibles si la réponse est : [0] - A, [1] - B, [2] - C, [3] - A,B, [4] - B,C, [5] - A,C, [6] - aucune
        for Phi in Phi_possibles:
            Phi=Phi.get_Phi()
            if Phi[s0_0,s0_1]>Phi[s1_0,s1_1] and Phi[s0_0,s0_1]>Phi[s2_0,s2_1]:
                reponse[0]+=1
            elif Phi[s1_0,s1_1]>Phi[s0_0,s0_1] and Phi[s1_0,s1_1]>Phi[s2_0,s2_1]:
                reponse[1]+=1
            elif Phi[s2_0,s2_1]>Phi[s0_0,s0_1] and Phi[s2_0,s2_1]>Phi[s1_0,s1_1]:
                reponse[2]+=1
            elif Phi[s0_0,s0_1]>Phi[s2_0,s2_1] and Phi[s0_0,s0_1]==Phi[s1_0,s1_1]:
                reponse[3]+=1
            elif Phi[s1_0,s1_1]>Phi[s0_0,s0_1] and Phi[s2_0,s2_1]==Phi[s1_0,s1_1]:
                reponse[4]+=1
            elif Phi[s0_0,s0_1]>Phi[s1_0,s1_1] and Phi[s2_0,s2_1]==Phi[s0_0,s0_1]:
                reponse[5]+=1
            else:
                reponse[6]+=1
        return reponse

    def simulation_type_B_2(self,Phi_possibles,liste_criteres):
        # question: [(c1,c2),(c3,c4)]
        # Simule les 3 réponses possibles à une question de type 2 qui classe 2 séquences par ordre croissant de difficulté
        # Retourne le nombre de Phi_possibles après avoir posé cette Q, pour chaque réponse possible
        [(s0_0,s0_1),(s1_0,s1_1)]=[self.sequences[0].indices,self.sequences[1].indices]
        # question_i: Classer les 2 séquences [A,B] par ordre croissant de difficulté
        reponse=[0 for i in range(3)]
        # contient le nbre de Phi_possibles si la réponse est : [0] - A<B, [1] - A=B, [2] - B>A
        for Phi in Phi_possibles:
            Phi=Phi.get_Phi()
            if Phi[s0_0,s0_1]<Phi[s1_0,s1_1]:
                reponse[0]+=1
            elif Phi[s0_0,s0_1]==Phi[s1_0,s1_1]:
                reponse[1]+=1
            else:
                reponse[2]+=1
        return reponse

    def simulation_type_B_3(self,Phi_possibles,liste_criteres):
        # question: [(c1,c2),(c3,c4),(c5,c6)]
        # Simule les 13 réponses possibles à une question de type B qui classe 3 séquences par ordre croissant de difficulté
        # Retourne le nombre de Phi_possibles après avoir posé cette Q, pour chaque réponse possible
        [(s0_0,s0_1),(s1_0,s1_1),(s2_0,s2_1)]=[self.sequences[0].indices,self.sequences[1].indices,self.sequences[2].indices]
        # question_i: Classer les 3 séquences [A,B,C] par ordre croissant de difficulté
        reponse=[0 for i in range(13)]
        # contient le nbre de Phi_possibles si la réponse est : [0] - C-B<A, [1] - A-C<B, [2] - A-B<C, [3] - C<A-B, [4] - A<B-C, [5] - B<A-C, [6] - A<B<C, [7] - A<C<B, [8] - B<A<C, [9] - B<C<A, [10] - C<A<B, [11] - C<B<A, [12] - A-B-C
        for Phi in Phi_possibles:
            Phi=Phi.get_Phi()
            if Phi[s0_0,s0_1]>Phi[s1_0,s1_1] and Phi[s1_0,s1_1]==Phi[s2_0,s2_1]:
                reponse[0]+=1
            elif Phi[s1_0,s1_1]>Phi[s0_0,s0_1] and Phi[s0_0,s0_1]==Phi[s2_0,s2_1]:
                reponse[1]+=1
            elif Phi[s2_0,s2_1]>Phi[s0_0,s0_1] and Phi[s0_0,s0_1]==Phi[s1_0,s1_1]:
                reponse[2]+=1
            elif Phi[s0_0,s0_1]>Phi[s2_0,s2_1] and Phi[s0_0,s0_1]==Phi[s1_0,s1_1]:
                reponse[3]+=1
            elif Phi[s1_0,s1_1]>Phi[s0_0,s0_1] and Phi[s2_0,s2_1]==Phi[s1_0,s1_1]:
                reponse[4]+=1
            elif Phi[s0_0,s0_1]>Phi[s1_0,s1_1] and Phi[s2_0,s2_1]==Phi[s0_0,s0_1]:
                reponse[5]+=1
            elif Phi[s0_0,s0_1]<Phi[s1_0,s1_1] and Phi[s1_0,s1_1]<Phi[s2_0,s2_1]:
                reponse[6]+=1
            elif Phi[s0_0,s0_1]<Phi[s2_0,s2_1] and Phi[s2_0,s2_1]<Phi[s1_0,s1_1]:
                reponse[7]+=1
            elif Phi[s1_0,s1_1]<Phi[s0_0,s0_1] and Phi[s0_0,s0_1]<Phi[s2_0,s2_1]:
                reponse[8]+=1
            elif Phi[s1_0,s1_1]<Phi[s2_0,s2_1] and Phi[s2_0,s2_1]<Phi[s0_0,s0_1]:
                reponse[9]+=1
            elif Phi[s2_0,s2_1]<Phi[s0_0,s0_1] and Phi[s0_0,s0_1]<Phi[s1_0,s1_1]:
                reponse[10]+=1
            elif Phi[s2_0,s2_1]<Phi[s1_0,s1_1] and Phi[s1_0,s1_1]<Phi[s0_0,s0_1]:
                reponse[11]+=1
            else:
                reponse[12]+=1
        return reponse
