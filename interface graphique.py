import tkinter as tk
import random as rd

def quit(event):
    """Ferme la fenêtre principale."""
    racine.destroy()

def play(event):
    """Supprime les widgets"""
    label_demarrage.destroy()
    bouton_quitter.destroy()
    bouton_demarrer.destroy()
    partie(100) #initialise le joueur à 100 jetons

def carte(paquet:list, n:int)->list:
    """génère un nombre n de cartes du paquet"""
    main = [] #Les cartes générées sont stokées dans une liste.
    for _ in range (n):
        carte = rd.choice(paquet) #La fonction choice permet de faire un choix aléatoire de carte dans le paquet.
        main.append(carte)
    return main
    
def valeur(main:list)->int:
    """renvoie la valeur des cartes dans une main"""
    valeur = 0
    nb_as = 0 #La valeur des as est gérée de telle sorte que lorsque la valeur de la main dépasse 21 les as comptent 1.
    for carte in main:
        rang = carte.split(" de ")[0] #Permet de stocker dans la variable uniquement le rang de la carte, soit la clé dans le dictionnaire rangs.
        valeur += rangs[rang]
        if rang == "As":
            nb_as += 1
    while valeur > 21 and nb_as != 0:
        valeur -= 10
        nb_as -= 1
    return(valeur)

def partie(jeton:int)->int:
    """permet de jouer une partie en misant, renvoie le nombre de jeton à la fin de la partie"""

    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    label_joueur=tk.Label(racine,text=f"Votre main : {main_joueur}(Valeur: {valeur(main_joueur)})")
    label_joueur.pack()
    label_croupier=tk.Label(racine,text=f"Carte visible du croupier : {main_croupier} (Valeur : {valeur(main_croupier)})")
    label_croupier.pack()
       
    

#Création du menu du jeu
racine = tk.Tk()
racine.title("Blackjack")

label_demarrage = tk.Label(racine, text="Blackjack !", padx=20, pady=20, font = ("helvetica", "30"))
label_demarrage.grid(row=0,column=0,columnspan=2)

bouton_demarrer= tk.Button(racine, text="Play", font = ("helvetica", "30"), width=50)
bouton_demarrer.bind("<Button-1>",play)
bouton_demarrer.grid(row=1,column=0)

bouton_quitter= tk.Button(racine, text="Quit", font = ("helvetica", "30"), width=50)
bouton_quitter.bind("<Button-1>", quit)
bouton_quitter.grid(row=2,column=0)




rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=["Coeur", "Trèfle", "Carreau", "Pique"]
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

racine.mainloop()

