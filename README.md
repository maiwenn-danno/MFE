# MFE

# Pour lancer l'algo, lancer le fichier Main, en mettant à jour les paramètres suivants:

# ---- pour le contexte
# liste_criteres - ex: ["math","phys","litt"]
# p : Nombre de niveaux discrets des valeurs de Phi
# k : Nombre de Phi_DM(k,l) non nuls (doit etre < n**2)

# ---- pour les questions
# q_type : type de question de l'heuristique : "Sequences_plus_difficiles" ou "Classement_sequences"
# nb_sequences : Nombre de séquences par question

# ---- pour la génération aléatoire/systématique de solutions:
# nb_Phi_seuil: Qd estimate_nb_Phi_possibles < ce seuil, génération systématique des solutions
# nb_Phi_max: Nb max de solutions admissibles générées aléatoirement
# nb_it_max: Nombre d'itérations maximales pour la recherche aléatoire de solutions admissibles

# ---- pour la précision attendue (cf arret de l'heuristique)
# nb_quest_exact : Nb de questions que l'on accepte pour trouver la solution exacte
# max_biais : <p, biais max que l'on autorise dans les Phi_possibles pour l'arret de l'heuristique
# max_nb_biais: < n**2, Nb max de valeurs non fixées que l'on autorise pour l'arrêt de l'heuristique

# ---- pour l'évaluation de la performance:
# n_DM : nb de Phi_DM à générer

# ---- pour la console
# Print: True si on veut les détails des questions des heuristiques, False si on veut juste les caractéristiques macros (nb questions et erreur)
