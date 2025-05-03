# -*- coding: utf-8 -*-
"""
Created on Sat May  3 21:18:00 2025

@author: yanni
"""

import mysql.connector

# Connexion à la base de données MySQL
ma_base = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

curseur = ma_base.cursor()

# Créer la base de données
curseur.execute("CREATE DATABASE IF NOT EXISTS jeu_python")

# Sélectionner la base de données
curseur.execute("USE jeu_python")

# Créer la table 'joueur'
curseur.execute("""
    CREATE TABLE IF NOT EXISTS joueur (
        id INT AUTO_INCREMENT PRIMARY KEY,
        pseudo VARCHAR(100) NOT NULL UNIQUE,
        motdepasse VARCHAR(255) NOT NULL
    )
""")

# Fermer la connexion
ma_base.commit()
curseur.close()
ma_base.close()

print("Base de données et table créées avec succès !")