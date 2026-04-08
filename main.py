import os
import time
from pymongo import MongoClient
import random

#initialisation de la bdd
client = MongoClient("mongodb://localhost:27017/")
db = client["test"]

personnages = list(db["personnages"].find())
monstres = list(db["monstres"].find())

score = []

def afficher_header(texte: str):
    print("-" * 60)
    print(texte.center(60))
    print("-" * 60)


def afficher_meilleurs_scores():
    # Récupérer les 3 meilleurs scores triés par manches décroissant
    meilleurs = ...

    # Afficher le tableau des meilleurs scores
    afficher_header("! Meilleurs Scores !")
    print(f"{'Rang':<6} {'Équipe':<20} {'Manches':<10}")
    print("-" * 40)
    for i in range(len(meilleurs)):
        s = meilleurs[i]
        rang = i + 1
        print(f"{rang:<6} {s['equipe']:<20} {s['manches']:<10}")


def afficher_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        afficher_header("Jeu de Combat")

        print("1. Demarrer une nouvelle partie")
        print("2. Afficher les 3 meilleurs scores")
        print("3. Quitter le jeu")
        

        choix = input("\nEntrez votre choix: ").strip()


        print("choix : " + "-" + choix + "-")
        if choix == "1":
            afficher_header("Nouvelle Partie !")
            break

        elif choix == "2":
            afficher_meilleurs_scores()
            input("\nAppuyez sur Entrée pour revenir au menu...")

        elif choix == "3":
            print("Au revoir !")
            time.sleep(1)
            exit()

        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.\n")
            input("Appuyez sur Entrée pour réessayer...")

def choix():
    print("Choisissez vos 3 personnages !")
    personnages_choisis = []

    for i in range(3):
        while True:
            numero = input(f"Personnage {i + 1}/3 : ")

            # Vérifier que c'est bien un nombre entier
            if not numero.isdigit():
                print("Veuillez entrer un numéro valide.")
                continue

            numero = int(numero)

            # Vérifier que le numéro est bon
            if numero < 1 or numero > 10:
                print("Numéro hors plage. Choisissez entre 1 et 10.")
                continue

            # Vérifier que le personnage n'est pas déjà choisi
            if numero in personnages_choisis:
                print("Ce personnage est déjà sélectionné. Choisissez-en un autre.")
                continue

            # ajout du choix si c'est bon
            personnages_choisis.append(numero)
            break
        #retourner la liste des perso choisis
    return personnages_choisis

def creer_equipe():
    #choisir un nom d'équipe
    nom_equipe = input("Choisir un nom d'équipe : ")
    #afficher les differents perso
    print(f"{'  ID':<5} {'  Nom':<20} {'  PV':<10} {'Attaque':<10} {'Defense':<10}")
    print("-" * 60)
    i = 1
    for p in personnages:
        print(f"- {i:<5} {p['nom']:<20} {p['pv']:<10} {p['attaque']:<10} {p['defense']:<10}")
        i += 1

    #choisir 3 perso
    indices = choix()

    # Construire l'équipe
    equipe = [dict(personnages[i - 1]) for i in indices]

    # Afficher l'équipe
    print(f"\nÉquipe « {nom_equipe} » constituée !")
    for p in equipe:
        print(f"- {p['nom']:<10} | PV: {p['pv']:<10} | Attaque: {p['attaque']:<10} | Defense: {p['defense']:<10}")

    # Retourner l'équipe
    return {"nom": nom_equipe, "personnages": equipe}

    
def random_monstres():
    # Choisir aléatoirement
    monstre = random.randint(0, len(monstres) - 1)

    # Retourner monstre choisi
    return monstres[monstre]

def filtrer_vivant(personnages_equipe):
    vivants = []
    for p in personnages_equipe:
        if p["pv"] > 0:
            vivants.append(p)
    return vivants


def choisir_personnage(personnages_equipe):
    #verifier les vivants
    vivants = filtrer_vivant(personnages_equipe)

    #afficher les vivant
    print("\nPersonnages vivants :")
    i = 1
    for p in vivants:
        print(f"{i}. {p['nom']:>10} -> {p['pv']:>3} PV | attaque : {p['attaque']:>3} | defense : {p['defense']:>3}")
        i += 1

    #choisir l'attaquant
    while True:
        time.sleep(0.5)
        choix = input("Choisissez quel personnage attaque : ")

        #verifier si l'input et bon
        if not choix.isdigit():
            print("Veuillez entrer un numéro valide.")
            continue

        choix = int(choix)

        if choix < 1 or choix > len(vivants):
            print("veuillez choisir parmis les choix possible.")
            continue

        return vivants[choix - 1]


def attaque_personnages(personnage, monstre):
    #chance de reussir l'attaque
    chance_reussite = random.randint(1, 4)

    #attaque rater
    if chance_reussite == 4:
        print(f"NOOOONN ! {personnage['nom']} a raté son attaque !")
        time.sleep(1)

    #attaque reussite
    else:
        degats = max(0, personnage["attaque"] - monstre["defense"])
        monstre["pv"] -= degats

        print(f"{personnage['nom']} attaque {monstre['nom']} -> -{degats} PV ({max(0, monstre['pv'])} PV restants)")
        time.sleep(1)


def attaque_monstres(monstre, personnages_equipe):
    #filtrer les perso vivants
    vivants = filtrer_vivant(personnages_equipe)

    # Choisir une cible aléatoire parmi les vivants
    personnages = random.choice(vivants)

    #chance que le monstre reussice
    chance_reussite = random.randint(1,4)
    
    if chance_reussite == 4 :
        print(f"{monstre['nom']} a rater son attaque !")
        time.sleep(1)
    else :
        # Calculer et infliger les dégâts (minimum 1)
        degats = max(0, monstre["attaque"] - personnages["defense"])
        personnages["pv"] = personnages["pv"] - degats
        print(f"{monstre['nom']} attaque {personnages['nom']} -> -{degats} PV ({max(0, personnages['pv'])} PV restants)")
        time.sleep(1)


def lancement_manche(manche):
    #choix du monstre random
    monstre = random_monstres()

    #afficher le monstre a affronter
    afficher_header(f"Manche {manche}")
    print(f"\nVous allez affronter {monstre['nom']}")
    time.sleep(0.5)
    print(f"{monstre['nom']} | PV: {monstre['pv']} | ATK: {monstre['attaque']} | DEF: {monstre['defense']}")
    time.sleep(0.5)
    print("Que la force soit avec vous !")
    time.sleep(1)
    #retourner le monstre
    return monstre


def lancer_vagues(equipe):
    personnages_equipe = equipe["personnages"]
    manche = 1
    # Boucle de la manche
    while True:
        monstre = lancement_manche(manche)
        while True:
            # Choix du personnage qui attaque
            print("\n[ Attaques de votre équipe ]")
            personnage = choisir_personnage(personnages_equipe)
            attaque_personnages(personnage, monstre)  

            # Si le monstre meurt prochaine manche
            if monstre["pv"] <= 0:
                
                print(f"\n! {monstre['nom']} est vaincu ! Manche {manche} terminée.")
                manche += 1
                input("\nAppuyez sur Entrée pour la prochaine manche...")
                break

            # Riposte du monstre
            print("\n[ Riposte du monstre ]")
            attaque_monstres(monstre, personnages_equipe)

            # Si un personnage meurt l'enlever des choix
            for p in personnages_equipe:
                if p["pv"] <= 0 :
                    print(f"{p['nom']} est mort !")

            # Si tout le monde meurt terminer_combat()
            if all(p["pv"] <= 0 for p in personnages_equipe):
                return terminer_combat(equipe, manche)


def terminer_combat(equipe, manche):
    print(f"\nPartie terminée ! Vous avez survécu {manche} manche(s).")
    db["scores"].insert_one({"equipe": equipe["nom"], "manches": manche})


def main():
    # Afficher le menu
    afficher_menu()

    # Créer mon équipe
    equipe = creer_equipe()

    # Démarrer les vagues de combat
    lancer_vagues(equipe)

main()

