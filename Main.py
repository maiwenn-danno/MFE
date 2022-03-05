import numpy as np
import copy
import math
import pandas as pd
from Contexte import *
from Heuristique import * 
from Question_DM import *
from Phi_class import *
from Sequence import *
from Prediction import *
from Question_simulation import *

def poser_quest_init(n,p,Phi_DM,dico_criteres,liste_criteres,liste_sequences_diff_possibles,liste_contraintes_equal,liste_contraintes_diff,Print):
    print("1--- Questions initiales")
    # 1: Attribuer les critères aux niveaux de difficulté
    Question_1=Question_DM(Phi_DM.get_Phi(), dico_criteres, p, "Niveaux_diff_criteres", liste_criteres,True)
    prediction=Prediction(n,p,Question_1.get_valeurs_fixes())
    # 2: Séquences [k,l] qui sont aussi difficiles que les séquences [l,l] correspondantes
    Question_2=Question_DM(Phi_DM.get_Phi(), dico_criteres, p, "Sequences_independantes", liste_sequences_diff_possibles,True)
    liste_contraintes_equal.extend(Question_2.get_contraintes_equal())
    liste_contraintes_diff.extend(Question_2.get_contraintes_diff())
    prediction.update(liste_contraintes_equal,liste_contraintes_diff)
    return prediction,liste_contraintes_equal,liste_contraintes_diff

def find_estimate(n,p,stockage_all_Phi,Phi_possibles,prediction,liste_contraintes_equal,liste_contraintes_diff):
    if stockage_all_Phi:
            Phi_estimate=rd.choice(Phi_possibles).get_Phi()
    else:
        Phi_estimate=Phi_class(n, p, "aleatoire2", 0, prediction)
        while Phi_estimate.check_contraintes(liste_contraintes_equal,liste_contraintes_diff,prediction.get_val_fixes())!=True:
            Phi_estimate=Phi_class(n, p, "aleatoire2", 0, prediction)
    return Phi_estimate

def compute_difference(Phi_DM,Phi_estimate,n,Print):
    if Print:  
        print("Phi_estimate \n"+ str(Phi_estimate))
        print("Phi_DM \n"+str(Phi_DM))
        print("Est-ce la même que Phi_DM? -- "+str((Phi_estimate==Phi_DM).all())+" --")
    difference=0
    if not (Phi_estimate == Phi_DM).all():
        for ligne in range(n):
            for column in range(n):
                difference+=abs(Phi_estimate[ligne,column]-Phi_DM[ligne,column])
    if Print:
        print("La différence moyenne pour chaque valeur Phi[k,l] est "+str(round(difference/(n*n),2)))
    return round(difference/(n*n),2)

def build_resultats(Phi_DM,Phi_estimate,heuristiques,difference):
    res={}
    res["Nb questions"]=heuristiques.get_nb_questions() 
    res["Erreur moyenne"]=copy.deepcopy(difference)
    return res

def main():
    # ----------- Parametres ---------------
    # -- pour Phi 
    liste_criteres=["math","phys","litt"] #liste_criteres= ["math","phys","litt","angl"] #liste_criteres= ["math","phys","litt","angl","ndls"] #liste_criteres= ["math","phys","litt","angl","ndls","hist","geo"]
    p=3 # Nombre de niveaux discrets des valeurs de Phi
    k=7 # Nombre de Phi(k,l) non nuls (doit etre < n**2)
    n=len(liste_criteres) # Nombre de critères
    #test git

    # -- pour les questions
    q_type="Sequences_plus_difficiles" 
    #q_type="Classement_sequences"
    nb_sequences=3 #Nombre de séquences par question

    # -- pour la génération aléatoire/systématique de solutions:
    nb_Phi_seuil=1000 #Qd estimate_nb_Phi_possibles < ce seuil, génération systématique des solutions
    nb_Phi_max=500 #Nombre de solutions admissibles utilisées pour choisir la meilleure question
    nb_it_max=50000 #Nombre d'itérations maximales pour la recherche aléatoire de solutions admissibles
    
    # -- pour la précision attendue (cf arret de l'heuristique)
    nb_quest_exact=0 #Nb de questions que l'on accepte pour trouver la solution exacte
    max_biais=math.ceil(p/2) #<p #Biais max que l'on autorise dans les Phi_possibles pour l'arret de l'heuristique
    max_nb_biais=n**2//3 # < n**2 #Nb max de valeurs non fixées que l'on autorise pour l'arrêt de l'heuristique
    
    # -- pour l'valuation de la performance:
    n_DM=20 # nb de Phi_DM à générer

    #-- print details?
    Print=False #True si on veut afficher les détails de toutes les questions 
    
    # ---------- Construction contexte ------
    prob=Contexte(liste_criteres,nb_sequences)
    dico_criteres=prob.get_dico_criteres()
    print("\n"+str(dico_criteres))
    liste_sequences_diff_possibles=prob.get_liste_seq_diff_possibles()

    Phi_DMs=[]
    resultats_heuristiques=[] # Liste de dictionnaires, contenant le Phi_DM, le Phi_estimate, la différence et le nb de questions, obtenus avec l'heuristique
    resultats_random=[]# Liste de dictionnaires, contenant le Phi_DM, le Phi_estimate, la différence et le nb de questions, obtenus avec le random

    for i in range(n_DM):

        # Create Phi_DM
        Phi_DM=Phi_class(n,p,"AI",k)
        Phi_DMs.append(Phi_DM)
        print("\n Phi_DM"+str(i)+" = \n"+str(Phi_DM.get_Phi()))

        # ------------ Initialiser contraintes ---------
        liste_contraintes_equal=[]
        liste_contraintes_diff=[]

        # --------- Poser les questions initiales ----------
        prediction_init,liste_contraintes_equal_init,liste_contraintes_diff_init=poser_quest_init(n,p,Phi_DM,dico_criteres,liste_criteres,liste_sequences_diff_possibles,liste_contraintes_equal,liste_contraintes_diff,Print)
    
        # --------- Poser les questions selon l'heuristique -----
        if not Print:
            print("2a--- Heuristique ")
        heuristique=Heuristique(n,p,prediction_init,liste_contraintes_equal_init,liste_contraintes_diff_init,prob,q_type,nb_quest_exact,max_nb_biais,max_biais,nb_Phi_seuil,nb_Phi_max,nb_it_max,Phi_DM,"heuristique",Print)
        Phi_possibles_heur=heuristique.get_Phi_possibles()
        print("Nombre solutions admissibles après la Q"+str(heuristique.get_nb_questions())+": "+ str(len(Phi_possibles_heur)))
        if len(Phi_possibles_heur)>0:
            Phi_estimate_heur=find_estimate(n,p,heuristique.get_stockage_all_Phi(),Phi_possibles_heur,heuristique.get_prediction(),heuristique.get_contraintes_equal(),heuristique.get_contraintes_diff())
            difference_heur=compute_difference(Phi_DM.get_Phi(),Phi_estimate_heur,n,Print)
        else:
            print("Aucune solution trouvée....")
        resultats_heuristiques.append(build_resultats(Phi_DM.get_Phi(),Phi_estimate_heur,heuristique,difference_heur))

        # --------- Poser les questions selon Random -----
        if not Print:
            print("2b--- Random ")
        random=Heuristique(n,p,prediction_init,liste_contraintes_equal_init,liste_contraintes_diff_init,prob,q_type,nb_quest_exact,max_nb_biais,max_biais,nb_Phi_seuil,nb_Phi_max,nb_it_max,Phi_DM,"random",Print)
        Phi_possibles_rand=random.get_Phi_possibles()
        print("Nombre solutions admissibles après la Q"+str(random.get_nb_questions())+": "+ str(len(Phi_possibles_rand)))
        if len(Phi_possibles_rand)>0:
            Phi_estimate_rand=find_estimate(n,p,random.get_stockage_all_Phi(),Phi_possibles_rand,random.get_prediction(),random.get_contraintes_equal(),random.get_contraintes_diff())
            difference_rand=compute_difference(Phi_DM.get_Phi(),Phi_estimate_rand,n,Print)
        else:
            print("Aucune solution trouvée....")
        resultats_random.append(build_resultats(Phi_DM.get_Phi(),Phi_estimate_rand,random,difference_rand))

    # --- Comparaison des performances
    print("\n --------- Comparaison performances --------")
    print("Condition arrêt: précision avec biais < "+str(max_biais)+", pour moins de " + str(max_nb_biais)+" valeurs (sauf si sol exacte en moins de "+str(nb_quest_exact)+" questions)")
        
    print("\n ---> Résultats heuristiques")
    df_heuristiques = pd.DataFrame(resultats_heuristiques)
    print(df_heuristiques)
    print("Nb_questions moyen sur "+str(n_DM)+" instances:"+str(round(df_heuristiques["Nb questions"].mean(),2)))
    print("Erreur moyenne sur "+str(n_DM)+" instances:"+str(round(df_heuristiques["Erreur moyenne"].mean(),2)))

    print("\n ---> Résultats random")
    df_random = pd.DataFrame(resultats_random)
    print(df_random)
    print("Nb_questions moyen sur "+str(n_DM)+" instances :"+str(round(df_random["Nb questions"].mean(),2)))
    print("Erreur moyenne sur "+str(n_DM)+" instances :"+str(round(df_random["Erreur moyenne"].mean(),2))+"\n")


if __name__ == '__main__':
    main()



"""  ---- Pour 1 Phi_DM
    # ------------ Construction Phi_DM -----------
    #Phi_DM=Phi_class(n,p,"AI",k)
    #print("\n Phi_DM = \n"+str(Phi_DM.get_Phi()))

    # ------------ Initialiser contraintes ---------
    liste_contraintes_equal=[]
    liste_contraintes_diff=[]

    # --------- Poser les questions initiales ----------
    prediction_init,liste_contraintes_equal_init,liste_contraintes_diff_init=poser_quest_init(n,p,Phi_DM,dico_criteres,liste_criteres,liste_sequences_diff_possibles,liste_contraintes_equal,liste_contraintes_diff)
    print("--- Vérification : contraintes avec Phi_DM --- "+str(Phi_DM.check_contraintes(liste_contraintes_equal,liste_contraintes_diff,prediction_init.get_val_fixes())))

    # --------- Poser les questions selon l'heuristique -----
    heuristique=Heuristique(n,p,prediction_init,liste_contraintes_equal_init,liste_contraintes_diff_init,prob,q_type,nb_quest_exact,max_nb_biais,max_biais,nb_Phi_seuil,nb_Phi_max,nb_it_max,Phi_DM,"heuristique",Print)
    Phi_possibles_heur=heuristique.get_Phi_possibles()
    print("Nombre solutions admissibles après la Q"+str(heuristique.get_nb_questions())+": "+ str(len(Phi_possibles_heur)))

    print('\n\n ---------- Résultat ---------- ')
    if len(Phi_possibles_heur)>0:
        Phi_estimate=find_estimate(n,p,heuristique.get_stockage_all_Phi(),Phi_possibles_heur,heuristique.get_prediction(),liste_contraintes_equal,liste_contraintes_diff)
        difference=compute_difference(Phi_DM.get_Phi(),Phi_estimate,n,Print)
    else:
        print("Aucune solution trouvée....")"""