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
#exemple interface graphique https://github.com/m4xy07/Blackjack-With-UI

import random as rd
import tkinter as tk

#Création d'un paquet de carte.
rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=["Coeur", "Trèfle", "Carreau", "Pique"]
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

#Création d'une fonction qui permet de générer des cartes.
def carte(paquet:list, n:int)->list:
    """génère un nombre n de cartes du paquet"""
    main=[] #Les cartes générées sont stokées dans une liste.
    for i in range (n):
        carte=rd.choice(paquet) #La fonction choice permet de faire un choix aléatoire de carte dans le paquet.
        main.append(carte)
    return(main)

#Création d'une fonction qui permet de calculer la valeur des cartes d'une main. 
def valeur(main:list)->int:
    """renvoie la valeur des cartes dans une main"""
    valeur=0
    nb_as=0 #La valeur des as est gérée de telle sorte que lorsque la valeur de la main dépasse 21 les as comptent 1.
    for carte in main:
        rang=carte.split(" de ")[0] #Permet de stocker dans la variable uniquement le rang de la carte, soit la clé dans le dictionnaire rangs.
        valeur+=rangs[rang]
        if rang=="As":
            nb_as+=1
    while valeur>21 and nb_as!=0:
        valeur-=10
        nb_as-=1
    return(valeur)

#Création d'une fonction qui permet de joueur une partie
def partie(jeton:int)->int:
    """permet de jouer une partie en misant, renvoie le nombre de jeton à la fin de la partie"""

    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    print(f"Votre main : {main_joueur} (Valeur: {valeur(main_joueur)})")
    print(f"Carte visible du croupier : {main_croupier} (Valeur: {valeur(main_croupier)})")

    #Création de la mise.
    mise=int(input(f"Votre solde de jeton est de {jeton}. Combien voulez-vous miser pour cette partie? "))
    while mise<=0 or mise>jeton:
        print("Votre mise n'est pas valide, veuillez entrer un montant valide!")
        mise=int(input("Quelle est votre nouvelle mise? "))

    #Vérification blackjack.
    if valeur(main_joueur)==21:
        print("Blackjack!")
        return(jeton+int(mise*1.5))
    
    while valeur(main_joueur)<21: 
        #Permet au joueur de choisir ses actions.
        choix=input("Voulez-vous tirer ou rester? ")
        if choix=="Tirer":
            main_joueur.extend(carte(paquet,1))
            print(f"Nouvelle main : {main_joueur} (Valeur: {valeur(main_joueur)})")
        elif choix=="Rester":
            pass
        elif choix=="Abandonner":
            print(f"Vous avez abandonné la partie. Vous perdez la moitié de votre mise.")
            jeton-=mise // 2 
            print(f"Solde de jeton : {jeton}")
            return jeton

        #Doubler sa mise 
def doubler():
    global mise, jeton
    if mise * 2 <= jeton:
        mise *= 2
        print(f"Votre mise est maintenant de {mise}.")
        tirer()
    else:
        print("Vous n'avez pas assez de jetons pour doubler.")
        #Actions du croupier.
        while valeur(main_croupier)<16:
            main_croupier.extend(carte(paquet,1))
        print(f"Main du croupier : {main_croupier} (Valeur: {valeur(main_croupier)})")

        #Résultat et gestion de la mise.
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

#Création d'une fonction pour lancer le jeu et jouer.
def jouer():
    """permet de gérer le jeu et les parties"""
    print("Bienvenue au Blackjack!")
    jeton=200 #Solde initial de jeton par défaut.
    while jeton>0:
        jeton=partie(jeton)
        if jeton<=0:
            print("Vous n'avez plus de jetons!")
            break
        nouvelle_partie=input("Voulez-vous jouer encore un fois? ")
        if nouvelle_partie!="Oui":
            print("Merci d'avoir joué!")
            break

#Création d'une interface graphique
racine = tk.Tk()
racine.title("Blackjack")

menu_blackjack=tk.Menu(racine) #barre de menu

menu_démarrer=tk.Menu(menu_blackjack) 
menu_quitter=tk.Menu(menu_blackjack)





canvas = tk.Canvas(racine, bg="white", height=500, width=500)
label_demarrage = tk.Label(racine, text="Voulez-vous jouer ?", padx=20, pady=20, font = ("helvetica", "30"))
bouton_demarrer= tk.Button(racine, text="Démarrer", font = ("helvetica", "30"), command= lambda: affichage("C'est parti !"))

bouton_demarrer.grid(row=1,column=0)
label_demarrage.grid(row=0, column=0, columnspan=2)
canvas.grid()


#canvas.grid(row=1,column=0)
#bouton_tirer=tk.Button(racine, text="Tirer", command=)
#bouton_rester=tk.Button(racine, text="Rester")
#bouton_miser=tk.Button(racine, text="Miser")
#TEST
racine.mainloop()
