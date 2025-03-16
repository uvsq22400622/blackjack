import tkinter as tk
import random as rd

# --------- Paquet de cartes ----------
rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=["Coeur", "Trèfle", "Carreau", "Pique"]
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]
mise_utilisateur = 0
jeton = 100
game_over =False

def carte(paquet:list, n:int)->list:
    """génère un nombre n de cartes du paquet"""
    main = [] #Les cartes générées sont stokées dans une liste.
    for _ in range (n):
        carte = rd.choice(paquet) #La fonction choice permet de faire un choix aléatoire de carte dans le paquet.
        main.append(carte)
    return main

# --------- Déroulement de la partie ---------

def commencer_partie():
    """permet de jouer une partie en misant, renvoie le nombre de jeton à la fin de la partie"""
    global label_jetons, label_mise, entry_mise, bouton_valider, label_erreur, label_mise_acceptée
    

    label_jetons = tk.Label(racine, text=f"Vous avez {jeton} jetons.", font=("helvetica",14))
    label_jetons.pack()

    label_mise = tk.Label(racine, text = "Combien voulez vous miser ? :")
    label_mise.pack()

    entry_mise = tk.Entry(racine)
    entry_mise.pack()

    bouton_valider = tk.Button(racine, text="Valider la mise", command=mise_soumise)
    bouton_valider.pack()

def valider_mise(jeton:int,mise:int)-> str | None:
    """Valide la mise de l'utilisateur."""
    if mise > jeton:
        return "Votre mise est supérieure à votre nombre de jetons disponibles"
    elif mise <= 0:
        return "Veuillez entrer une mise positive"
    else:
        return None       

def mise_soumise():
    global mise_utilisateur, jeton, entry_mise, bouton_valider, label_erreur, label_mise_acceptée
    
    mise = int(entry_mise.get())
    message_erreur = valider_mise(jeton, mise)

    if message_erreur:
        label_erreur.config(text=message_erreur)
        label_erreur.pack()
        label_mise_acceptée.pack_forget()
    else:
        mise_utilisateur = mise
        jeton -= mise_utilisateur
        label_erreur.pack_forget() #cache le message d'erreur
        label_mise_acceptée.config(text=f"Mise acceptée : {mise_utilisateur}")
        label_mise_acceptée.pack()
        entry_mise.destroy()
        bouton_valider.destroy()
        #fonction pour ditribuer les cartes
        mains_joueurs()
        print(f"Mise acceptée : {mise_utilisateur} Jetons : {jeton}")

def mains_joueurs():
    global main_joueur, main_croupier, paquet

    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    label_joueur = tk.Label(racine, text=f"Votre main : {main_joueur}, (Valeur: {valeur(main_joueur)})")
    label_joueur.pack()

    label_croupier = tk.Label(racine, text=f"Main du croupier : {main_croupier}, (Valeur : {valeur(main_croupier)})")
    label_croupier.pack()
    
    label_choix = tk.Label(racine, text="Voulez-vous tirer ou rester? ")
    label_choix.pack()
    bouton_tirer = tk.Button(racine, text="Tirer", command=tirer)
    bouton_tirer.pack()

    bouton_rester = tk.Button(racine, text="Rester", command=rester)
    bouton_rester.pack()

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

def play(event):
    """Supprime les widgets"""
    label_demarrage.destroy()
    bouton_quitter.destroy()
    bouton_demarrer.destroy()
    commencer_partie()

def quit(event):
    """Ferme la fenêtre principale."""
    racine.destroy()

def tirer():
    global main_joueur, game_over, paquet, label_joueur
    """Rajoute une carte au joueur"""
    if not game_over:
        main_joueur.extend(carte(paquet, 1))
        label_joueur.config(text=f"Votre main : {main_joueur} (Valeur:{valeur(main_joueur)})")
    if valeur(main_joueur) > 21:
        game_over = True
        return"Dust !, vous perdez votre mise"
    elif valeur(main_joueur) == 21 :
        game_over = True

def rester():
    """Le joueur ne tire pas et passe son tour"""
    global game_over
    if not game_over:
        game_over = True
        label_reste = tk.Label(racine, text="Le joueur reste.")
        label_reste.pack()

#Création du fenetre du jeu :
racine = tk.Tk()
racine.title("Blackjack")

label_demarrage = tk.Label(racine, text="Blackjack !", padx=20, pady=20, font = ("helvetica", "30"))
label_demarrage.pack()

bouton_demarrer= tk.Button(racine, text="Play", font = ("helvetica", "30"), width=50)
bouton_demarrer.bind("<Button-1>",play)
bouton_demarrer.pack()
bouton_quitter= tk.Button(racine, text="Quit", font = ("helvetica", "30"), width=50)
bouton_quitter.bind("<Button-1>", quit)
bouton_quitter.pack()
#------MISE-------
label_jetons = tk.Label(racine, text=f"Vous avez {jeton} jetons.", font=("helvetica",14))


label_mise = tk.Label(racine, text = "Combien voulez vous miser ? ", font=("helvetica",14))

    
entry_mise = tk.Entry(racine)

    
bouton_valider = tk.Button(racine, text="Valider la mise", command=mise_soumise)




#-----en cas d'erreur-----
label_erreur = tk.Label(racine, text="", fg="red")
label_mise_acceptée = tk.Label(racine, text="", fg="green")

racine.mainloop()