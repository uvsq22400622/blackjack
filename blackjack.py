# but du jeu battre le croupier sans dépasser 21, si 21 dépassé = on perd (le joueur "brûle")
# valeur des cartes : de 2 à 9, du 10 au roi = 10 points et l'as = 1 ou 11 points (choix du joueur)
#   == liste, dictionnaire soit un conteneur associant les cartes à des points
# déroulement : première carte distribué visible pour j et c, deuxième carte visible pour le j et non le c
#           soit blackjack = victoire 
#           sinon plusieurs choix : "carte" qui lui rajoute une carte, conserver sa mise, 
#doubler sa mise seulement si on rajoute une carte ensuite ou abandonner (à voir) 
#   == itérations  
#pour le c : il tire des cartes jusqu'à atteindre au moins 17 ou plus (d'autres conditions)
# + interface graphique, tenter les mises 
#règles possibles à ajouter: Abandonner, Doubler, Splitter 
#règles:https://www.mundijeux.fr/multijoueur/blackjack/regles/#:~:text=Splitter%20.,possible%20de%20faire%20%E2%80%9CBlackjack%E2%80%9D.

import random as rd
import tkinter as tk

rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=["Coeur", "Trèfle", "Carreau", "Pique"]
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

def carte(paquet, n):
    """génère un nombre n de cartes du paquet"""
    main=[]
    for i in range (n):
        carte=rd.choice(paquet)
        main.append(carte)
    return(main)

def valeur(main):
    """renvoie la valeur des cartes dans une main"""
    valeur=0
    nb_as=0
    for carte in main:
        rang=carte.split(" de ")[0]
        valeur+=rangs[rang]
        if rang=="As":
            nb_as+=1
    while valeur>21 and nb_as!=0:
        valeur-=10
        nb_as-=1
    return(valeur)


def partie(jeton):

    main_joueur=carte(paquet,2)
    main_croupier=carte(paquet,1)

    print(f"Votre main : {main_joueur} (Valeur: {valeur(main_joueur)})")
    print(f"Carte visible du croupier : {main_croupier} (Valeur: {valeur(main_croupier)})")

    mise=int(input(f"Votre solde de jeton est de {jeton}. Combien voulez-vous miser pour cette partie? "))
    while mise<=0 or mise>jeton:
        print("Votre mise n'est pas valide, veuillez entrer un montant valide!")
        mise=int(input("Quelle est votre nouvelle mise? "))

    if valeur(main_joueur)==21:
        print("Blackjack!")
        return(jeton+int(mise*1.5))
    
    while valeur(main_joueur)<21:
        choix=input("Voulez-vous tirer ou rester? ")
        if choix=="Tirer":
            main_joueur.extend(carte(paquet,1))
            print(f"Nouvelle main : {main_joueur} (Valeur: {valeur(main_joueur)})")
        elif choix=="Rester":
            pass

        while valeur(main_croupier)<16:
            main_croupier.extend(carte(paquet,1))
        print(f"Main du croupier : {main_croupier} (Valeur: {valeur(main_croupier)})")

        if valeur(main_joueur)>21:
            print("Dust!")
            return(jeton-mise)
        elif valeur(main_croupier)>21:
            print("Gagné!")
            return(jeton+mise)
        elif valeur(main_croupier)>valeur(main_joueur):
            print("Perdu!")
            return(jeton-mise)
        elif valeur(main_joueur)>valeur(main_croupier):
            print("Gagné!")
            return(jeton+mise)
        elif valeur(main_joueur)==valeur(main_croupier):
            print("Egalité!")
            return(jeton)

def jouer():
    print("Bienvenue au Blackjack!")
    jeton=200
    while jeton>0:
        jeton=partie(jeton)
        if jeton<=0:
            print("Vous n'avez plus de jetons!")
            break
        nouvelle_partie=input("Voulez-vous jouer encore un fois? ")
        if nouvelle_partie!="Oui":
            print("Merci d'avoir joué!")
            break

racine = tk.Tk()
racine.title("Blackjack")

canvas = tk.Canvas(racine, text="Le jeu démarre", bg="white", height=400, width=400) #voir par défaut taille fenêtre
canvas.grid(row=0,column=0)

bouton_demarrer= tk.Button(racine, text="Démarrer", command= )
canvas.grid(row=1,column=0)
bouton_tirer=tk.Button(racine, text="Tirer")
bouton_rester=tk.Button(racine, text="Rester")
bouton_miser=tk.Button(racine, text="Miser")

racine.mainloop()