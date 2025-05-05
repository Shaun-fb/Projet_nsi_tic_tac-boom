# -*- coding: utf-8 -*-
"""
Created on Sat May  3 18:46:53 2025

@author: yanni
"""

import threading
import random
import mysql.connector
import time

# Connexion à la base de données
ma_base = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="jeu_python"
)
curseur = ma_base.cursor()


# Fonction d'inscription
def inscription_joueur(pseudo, motdepasse):
    # Vérifier si le pseudo existe déjà
    curseur.execute("SELECT * FROM joueur WHERE pseudo = %s", (pseudo,))
    if curseur.fetchone() is None:  # Si le pseudo n'existe pas, l'inscrire
        curseur.execute("INSERT INTO joueur (pseudo, motdepasse) VALUES (%s, %s)", (pseudo, motdepasse))
        ma_base.commit()
        print(f" Nouveau joueur inscrit : {pseudo}")
    else:
        print(" Ce pseudo est déjà pris. Veuillez en choisir un autre.")


# Fonction de connexion
def connection(pseudo, motdepasse):
    curseur.execute("SELECT * FROM joueur WHERE pseudo = %s AND motdepasse = %s", (pseudo, motdepasse))
    return curseur.fetchone() is not None

# Classe Joueur
class Joueur:
    def __init__(self, pseudo, motdepasse):
        self.pseudo = pseudo
        self.motdepasse = motdepasse
        self.points = 0

    def __str__(self):
        return f"{self.pseudo} - {self.points} points"

# Dictionnaire sans doublons
mots_jeux = {
    "jeu", "console", "manette", "écran", "son", "musique", "effet",
    "ambiance", "menu", "option", "sauvegarde", "déconnexion", "installation",
    "patch", "test", "création", "programmation", "erreur", "débogage", "carte",
    "zone", "niveau", "mission", "objectif", "boss", "ennemis", "monstres",
    "personnage", "armes", "bouclier", "épée", "hache", "arc", "flèche", "lance",
    "pouvoir", "sort", "magie", "compétence", "attaque", "défense", "vitesse", 
    "saut", "course", "combat", "fuir", "tirer", "cibler", "franchir", "collecter",
    "inventaire", "potion", "santé", "vie", "régénération", "recharge", "batterie",
    "objet", "clé", "monnaie", "argent", "magasin", "boutique", "évolution", "progression",
    "amélioration", "récompense", "succès", "équipement", "vêtements", "casque",
    "gants", "bottes", "armure", "combinaison", "pack", "bonus", "contenu", "édition",
    "version", "téléchargement", "vidéo", "image", "graphisme", "animation", "simulation",
    "exploration", "histoire", "narration", "dialogue", "scénario", "cinématique",
    "suspense", "intrigue", "décision", "choix", "fin", "début", "moyen", "équilibre",
    "difficulté", "défi", "challenge", "réaction", "temps", "chronomètre", "compteur",
    "pause", "limite", "sélection", "choisir", "modifier", "valider", "enregistrer",
    "reprendre", "quitter", "continuer", "commencer", "redémarrer", "retour", "terminer",
    "terminé", "progresser", "échouer", "réussir", "victoire", "défaite", "avancer",
    "reculer", "bouger", "sauter", "plonger", "courir", "ramper", "escalader", "descendre",
    "monter", "lancer", "attraper", "cacher", "trouver", "créer", "modder", "construire",
    "détruire", "fusionner", "casser", "réparer", "forger", "fabriquer", "découvrir",
    "explorer", "chasser", "capturer", "éliminer", "sauver", "protéger", "détruire",
    "enchaîner", "combo", "énigme", "puzzle", "résoudre", "labyrinthe", "piège",
    "évasion", "cachette", "sortie", "voie", "chemin", "route", "secteur", "quartier",
    "terrain", "obstacle", "verrou", "tâche", "récompense", "guerrier", "mage", "archer",
    "soigneur", "voleur", "assassin", "chasseur", "rôdeur", "combat", "dégâts", "dommages",
    "énergie", "récupérer", "médailles", "compétition", "match", "tournoi", "champion",
    "équipe", "coéquipier", "rival", "entraide", "collaboration", "classement", "record",
    "soluce", "guide", "statistiques", "profil", "paramètre", "interface", "réglage",
    "améliorer", "rétablir", "gérer", "activer", "désactiver", "changer", "arrêter",
    "poursuivre", "mode", "joueur", "multijoueur", "coop", "matchmaking", "continent",
    "île", "région", "ville", "ruines", "forêt", "désert", "montagne", "océan", "rivière",
    "lac", "flotte", "mer", "caverne", "dungeon", "château", "village", "arène",
    "battlefield", "salle", "prison", "abri", "cachette", "forteresse", "base", "contrôle",
    "détection", "surveillance", "exploitation", "aide", "abonnement", "compte",
    "accès", "connexion", "inscription", "sortie", "plan", "localisation", "surveiller",
    "échange", "amélioration", "activité", "avatar", "personnalisation", "recharger",
    "acheter", "vendre", "revendre", "parcours", "mission", "objectifs", "carte",
    "explorateur", "guerrier", "mage", "combattant", "soldat", "entraînement", "rôle",
    "action", "passer", "attirer", "piéger", "objectif", "lancer", "survie", "élimination",
    "maîtrise", "technique", "boss", "chef", "rival", "voyage", "téléportation", "moteur",
    "graphisme", "design", "réseau", "vision", "sélection", "glisser", "cliquer",
    "interagir", "se connecter", "déconnexion", "emplacement", "partage", "accéder",
    "enregistrer", "fermer", "quitter", "changer"
}

# Fonction pour choisir une syllabe
def choisir_syllabe():
    mot = random.choice(list(mots_jeux))
    if len(mot) < 3:
        return mot
    return mot[random.randint(0, len(mot)-2):random.randint(1, len(mot))]

# Timer global avec durée aléatoire entre 120 et 192 secondes
def timer(duration):
    time.sleep(duration)
    print(" BOOM ! Temps écoulé ! Fin de la partie.")
    exit()

# Fonction principale du jeu
def jouer(joueurs):
    syllabe = choisir_syllabe()
    print(f" Syllabe à utiliser : '{syllabe}'")
    mots_utilisés = set()
    joueur_actuel_index = 0

    # Lancer le timer dans un thread séparé avec une durée aléatoire entre 120 et 192 secondes
    duree_jeu = random.randint(120, 192)
    print(f" La partie dure {duree_jeu} secondes.")
    threading.Thread(target=timer, args=(duree_jeu,), daemon=True).start()

    while True:
        joueur_actuel = joueurs[joueur_actuel_index]
        print(f"\nAu tour de {joueur_actuel.pseudo} - Points : {joueur_actuel.points}")
        mot = input(f"{joueur_actuel.pseudo}, entrez un mot contenant '{syllabe}': ").strip().lower()

        if syllabe in mot and mot in mots_jeux and mot not in mots_utilisés:
            print(" Mot valide ! +1 point")
            joueur_actuel.points += 1
            mots_utilisés.add(mot)
            syllabe = choisir_syllabe()  # Changer la syllabe uniquement après un mot valide
            print(f" Nouvelle syllabe : '{syllabe}'")
        else:
            print(" Mot invalide ou déjà utilisé.")

        # Changer de joueur
        joueur_actuel_index = (joueur_actuel_index + 1) % len(joueurs)

# Exemple d'utilisation
if __name__ == "__main__":
    print(" Bienvenue dans le jeu du Tic-Tac-Boom !")

    joueurs = []
    # Permet de gérer jusqu'à 14 joueurs
    for i in range(14):
        pseudo = input(f"Entrez le pseudo du joueur {i+1} : ")
        motdepasse = input("Mot de passe : ")

        if not connection(pseudo, motdepasse):
            print("Utilisateur non trouvé. Création d'un nouveau compte.")
            inscription_joueur(pseudo, motdepasse)

        joueurs.append(Joueur(pseudo, motdepasse))

    jouer(joueurs)

