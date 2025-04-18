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

    # Vérification possibilité de splitter
if len(main_joueur) == 2 and main_joueur[0].split(" de ")[0] == main_joueur[1].split(" de ")[0]:
    choix_split = input("Vos deux cartes ont la même valeur. Voulez-vous splitter ? [Oui, Non] ").capitalize()
    if choix_split == "Oui":
        jeton = splitter(main_joueur, paquet, mise, jeton)
        return jeton

    
   while valeur(main_joueur) < 21:
    # Permet au joueur de choisir ses actions.
    choix = input("Que voulez-vous faire ? [Tirer, Rester, Abandonner] ").capitalize()

    if choix == "Tirer":
        main_joueur.extend(carte(paquet, 1))
        print(f"Nouvelle main : {main_joueur} (Valeur: {valeur(main_joueur)})")
    elif choix == "Rester":
        break
    elif choix == "Abandonner":
        jeton = abandonner(jeton, mise)
        return jeton
    else:
        print("Choix invalide, veuillez réessayer.")


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

# Fonction Abandonner 

def abandonner(jeton, mise):
    """Permet au joueur d'abandonner la partie et de perdre la moitié de sa mise."""
    print("Vous avez abandonné la partie. Vous perdez la moitié de votre mise.")
    jeton -= mise // 2
    print(f"Solde de jetons : {jeton}")
    return jeton

# Fonction Splitter

def splitter(main_joueur, paquet, mise, jeton):
    """Permet de splitter la main si les deux cartes initiales sont de même valeur."""
    if len(main_joueur) == 2 and main_joueur[0].split(" de ")[0] == main_joueur[1].split(" de ")[0]:
        print("Vous choisissez de splitter votre main.")
        
        # Création de deux mains séparées.
        main_split_1 = [main_joueur[0], *carte(paquet, 1)]
        main_split_2 = [main_joueur[1], *carte(paquet, 1)]

        print(f"Main 1 : {main_split_1} (Valeur: {valeur(main_split_1)})")
        print(f"Main 2 : {main_split_2} (Valeur: {valeur(main_split_2)})")

        # Gérer les deux mains séparément (par exemple en utilisant une boucle ou des appels séparés).
        mise_split = mise  # Mise pour chaque main.
        jeton = partie_split(main_split_1, paquet, mise_split, jeton)
        jeton = partie_split(main_split_2, paquet, mise_split, jeton)

    else:
        print("Vous ne pouvez pas splitter cette main.")
    return jeton

def partie_split(main_split, paquet, mise, jeton):
    """Joue une main split de manière indépendante."""
    print(f"Vous jouez une main split : {main_split} (Valeur: {valeur(main_split)})")
    while valeur(main_split) < 21:
        choix = input("Que voulez-vous faire avec cette main ? [Tirer, Rester] ").capitalize()
        if choix == "Tirer":
            main_split.extend(carte(paquet, 1))
            print(f"Nouvelle main : {main_split} (Valeur: {valeur(main_split)})")
            if valeur(main_split) > 21:
                print("Vous avez dépassé 21. Vous perdez cette main !")
                return jeton - mise
        elif choix == "Rester":
            break
    return jeton

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

# à resoudre :
# fonction tirer/rester
## !!!!! ses fonctions existent déjà tester le code pour voir le problème
#def tirer():
#    global main_joueur, paquet, label_main_joueur
#    main_joueur.extend(carte(paquet, 1))
#    valeur_joueur = valeur(main_joueur)
#   label_main_joueur.config(text=f"Votre main : {main_joueur} (Valeur: {valeur_joueur})")
#    
#    if valeur_joueur > 21:
#        label_resultat.config(text="Bust! Vous avez perdu.")
#        bouton_tirer.config(state="disabled")
#        bouton_rester.config(state="disabled")
#    elif valeur_joueur == 21:
#        label_resultat.config(text="Blackjack! Vous avez gagné.")
#        bouton_tirer.config(state="disabled")
#        bouton_rester.config(state="disabled")

#def rester():
#    global main_croupier, label_main_croupier, label_resultat
#    while valeur(main_croupier) < 17:
#        main_croupier.extend(carte(paquet, 1))
#    label_main_croupier.config(text=f"Main du croupier : {main_croupier} (Valeur: {valeur(main_croupier)})")
#    
#    if valeur(main_croupier) > 21 or valeur(main_joueur) > valeur(main_croupier):
#        label_resultat.config(text="Félicitations, vous avez gagné!")
#    elif valeur(main_croupier) > valeur(main_joueur):
#        label_resultat.config(text="Désolé, vous avez perdu.")
#    else:
#        label_resultat.config(text="Égalité!")
#    
#    bouton_tirer.config(state="disabled")
#    bouton_rester.config(state="disabled")


def splitter(main_joueur, paquet, jeton):
    global jeton_apres_split1, mains_joueur
    """Permet de splitter la main si les deux cartes initiales sont de même valeur."""        
    # Création de deux mains séparées.
    main_split_1 = [main_joueur[0], *carte(paquet, 1)]
    main_split_2 = [main_joueur[1], *carte(paquet, 1)]
    mains_joueur = [main_split_1, main_split_2]
    print(f"Main 1 : {main_split_1} (Valeur: {valeur(main_split_1)})")
    print(f"Main 2 : {main_split_2} (Valeur: {valeur(main_split_2)})")
    
    # Gérer les deux mains séparément
    jeton_apres_split1 = partie_split(main_split_1, mise_utilisateur, jeton, 1)
    jeton_apres_split2 = partie_split(main_split_2, mise_utilisateur, jeton, jeton_apres_split1)

    return jeton_apres_split2 #censé restourner le nombre de jetons après avoir joué les deux mains


#def partie_split(main_split, jeton):
    global label_main_split
    """Joue une main split de manière indépendante."""
    label_main_split = tk.Label(racine, text=f"Vous jouez une main split : {main_split} (Valeur: {valeur(main_split)})")
    label_main_split.pack()

    jeton_apres_split = split_tirer(main_split, jeton)
    print(f'jetons après split: {jeton_apres_split}')
    return jeton_apres_split

#def split_tirer(main_split, jeton):
    global label_main_split, game_over
    """Rajoute une carte au joueur"""
    if not game_over and valeur(main_joueur)<21:
        nouvelle_carte = carte(paquet, 1)[0]
        main_split.append(nouvelle_carte)
        label_main_split.config(text=f"Nouvelle main : {main_split} (Valeur: {valeur(main_split)})")
    if valeur(main_joueur)==21:
        blackjack()
    elif valeur(main_joueur)>21:
        game_over= True
        croupier()
        resultat()
    pass

#def split_rester():
    global main_split
    label_split_rester = tk.Label(racine, text=f"Vous restez avec la main split. (Valeur: {valeur(main_split)}).")
    label_split_rester.pack()
    pass



if len(main_joueur) == 2 and main_joueur[0].split(" de ")[0] == main_joueur[1].split(" de ")[0]:
        label_split = tk.Label(racine, text="Vous choisissez de splitter votre main.")
        label_split.pack()
        bouton_split = tk.Button(racine, text="Split", command=partie_split)
        bouton_split.pack()
    else:
        message("Vous ne pouvez pas splitter cette main.")

    if mise_utilisateur * 2 <= jeton:
        bouton_doubler = tk.Button(racine, text="Doubler votre mise", command=doubler)
        bouton_doubler.pack()
    else:
        message("Vous n'avez pas assez de jetons pour doubler.")    