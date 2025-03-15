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
    global jeton
    
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


def fin_partie():
    racine.destroy()
    end = tk.Tk()
    label_end = tk.Label(end,text="Lost !", font = ("helvetica", "30"), width=50)
    label_end.pack()
    end.mainloop()

def end_round(message):
    """Affiche le résultat de la manche et désactive les boutons d'action."""
    global label_resultat
    label_resultat = tk.Label(racine, text=message, font=("helvetica", "16"))
    label_resultat.pack()


def partie(jeton:int)->int:
    """permet de jouer une partie en misant, renvoie le nombre de jeton à la fin de la partie"""

    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    label_joueur=tk.Label(racine,text=f"Votre main : {main_joueur}(Valeur: {valeur(main_joueur)})")
    label_joueur.pack()
    label_croupier=tk.Label(racine,text=f"Carte visible du croupier : {main_croupier} (Valeur : {valeur(main_croupier)})")
    label_croupier.pack()

    label_choix = tk.Label(racine, text="Voulez-vous tirer ou rester? ")
    label_choix.pack()
    bouton_tirer = tk.Button(racine, text="Tirer", command=tirer)
    bouton_tirer.pack()

    bouton_rester = tk.Button(racine, text="Rester", command=rester)
    bouton_rester.pack()
    verif_blackjack()


    def verif_blackjack():
        """Verifie si le joueur ou le croupier a un blackjack initial."""
        global jeton, mise_utilisateur
        joueur_v = valeur(main_joueur)
        croupier_v = valeur(main_croupier)

        if joueur_v == 21 and valeur(main_croupier + carte(paquet, 1)) == 21:
            game_over = True
            end_round("Blackjack pour vous et le croupier ! Égalité.")
            jetons += mise_utilisateur
        elif joueur_v == 21:
            game_over = True
            end_round(f"Blackjack ! Vous gagnez {mise_utilisateur * 1.5} jetons.")
            jetons += mise_utilisateur + (mise_utilisateur * 1.5)
        elif croupier_v == 11 and valeur(main_croupier + carte(paquet,1)) == 21:
            game_over = True
            
            end_round("Blackjack pour le croupier ! Vous perdez votre mise.")

    

    #fonction pour la mise de base
    def valider_mise():
        """Valide la mise de l'utilisateur."""
        mise_utilisateur = int(entry_mise.get())
        if mise_utilisateur>jeton:
            label_erreur = tk.Label(racine, text="Votre mise n'est pas valide, veuillez entrer un montant valide!")
            label_erreur.pack()
        else:
            print(f"Mise acceptée : {mise_utilisateur}") #test
            label_mise.destroy()
            entry_mise.destroy()
            bouton_valider.destroy()

        #Vérification blackjack.
        
            
    bouton_valider = tk.Button(racine, text="Valider la mise", command=valider_mise)
    bouton_valider.pack()
        
    def tirer():
        """Rajoute une carte au joueur"""
        nonlocal main_joueur
        main_joueur.extend(carte(paquet,1))
        label_joueur.config(text=f"Votre main : {main_joueur} (Valeur:{valeur(main_joueur)})")
        label_joueur.pack()
        

    def rester():
        """Le joueur ne tire pas et passe son tour"""
        label_reste = tk.Label(racine, text="Le joueur reste.")
        label_reste.pack()
    
    #rajouter le bouton abandonner, ....

jeton = 0
mise_utilisateur = 0
game_over = False



#Création du menu du jeu
racine = tk.Tk()
racine.title("Blackjack")

label_demarrage = tk.Label(racine, text="Blackjack !", padx=20, pady=20, font = ("helvetica", "30"))
label_demarrage.grid(row=0,column=0,columnspan=2)
#modifier la fenêtre, rajouter des images cartes, + credit

bouton_demarrer= tk.Button(racine, text="Play", font = ("helvetica", "30"), width=50)
bouton_demarrer.bind("<Button-1>",play)
bouton_demarrer.grid(row=1,column=0)

bouton_quitter= tk.Button(racine, text="Quit", font = ("helvetica", "30"), width=50)
bouton_quitter.bind("<Button-1>", quit)
bouton_quitter.grid(row=2,column=0)

bouton_abandonner = tk.Button(racine, text="Surrender", font = ("helvetica", "20"), width=50)
bouton_abandonner.bind("<Button-1>")


rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=["Coeur", "Trèfle", "Carreau", "Pique"]
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

racine.mainloop()

#while valeur(main_croupier)<16:
#            main_croupier.extend(carte(paquet,1))
#        label_croupier.config(text=f"Carte visible du croupier : {main_croupier} (Valeur : {valeur(main_croupier)})")
#        if valeur(main_joueur)==21:
#            label_winner = tk.Label(racine, text=f"Blackjack! Vous avez {jeton+int(mise_utilisateur*1.5)} jetons !")
#            label_winner.pack()
#        elif valeur(main_croupier)==21:
#           label_croupier_winner = tk.Label(racine, text=f"Le croupier a gagné !")
#          label_croupier_winner.pack()
#        elif valeur(main_joueur)>21:
#            label_dust = tk.Label(racine, text=f"Dust!, Vos jetons :{mise_utilisateur}")
#            label_dust.pack()
#        elif valeur(main_croupier)>21:
#            label_winner = tk.Label(racine, text=f"Blackjack! Vous avez {jeton+int(mise_utilisateur*1.5)} jetons !")
#            label_winner.pack()
#        elif valeur(main_croupier)>valeur(main_joueur):
#            label_loser = tk.Label(racine, text=f"Perdu ! Vous avez {jeton+int(mise_utilisateur*1.5)} jetons !")
#            #modif à faire du res
#            label_loser.pack()
#        elif valeur(main_joueur)>valeur(main_croupier):
#            label_winner = tk.Label(racine, text=f"Blackjack! Vous avez {jeton+int(mise_utilisateur*1.5)} jetons !")
#            label_winner.pack()
#        elif valeur(main_joueur)==valeur(main_croupier):
#            label_equality = tk.Label(racine, text=f"Egalité ! Vous avez {jeton} jetons !")
#            label_equality.pack()