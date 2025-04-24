import tkinter as tk
import random as rd
 
# --------- Paquet de cartes ----------
rangs={"As":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Valet":10, "Dame":10, "Roi":10}
couleurs=['♠', '♥', '♦', '♣']
paquet=[f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]
mise_utilisateur = 0
jeton = 100
game_over =False
doubler_mise = False
abandon = False
mise = 0
#liste des boutons_mise:
boutons = []
label_choix = None
bouton_tirer = None
bouton_rester = None
bouton_split = None
bouton_doubler = None
bouton_abandonner = None


def carte(paquet:list, n:int)->list:
    """génère un nombre n de cartes du paquet"""
    main = [] #Les cartes générées sont stokées dans une liste.
    for _ in range (n):
        carte = rd.choice(paquet) #La fonction choice permet de faire un choix aléatoire de carte dans le paquet.
        paquet.remove(carte)
        main.append(carte)
    return main
 
# --------- Déroulement de la partie ---------
 
def commencer_partie():
   """permet de jouer une partie en misant, renvoie le nombre de jeton à la fin de la partie"""
   global label_jetons, label_mise, entry_mise, bouton_valider, label_erreur, label_mise_acceptée, game_over

   if jeton<=0:
      label_fin_de_jeu=tk.Label(racine, text="Vous n'avez plus de jeton le jeu est terminé", font=("helvetica",14))
      label_fin_de_jeu.pack()
      bouton_quitter= tk.Button(racine, text="Quit", font = ("helvetica", "30"), width=20, command=quit)
      bouton_quitter.pack()

   else:
       game_over= False

       label_jetons = tk.Label(racine, text=f"Vous avez {jeton} jetons.", font=("helvetica",14))
       label_jetons.pack()

       label_mise = tk.Label(racine, text = "Combien voulez vous miser ? :")
       label_mise.pack()

       valeurs_mise= [1,5,10,25,50,100]

       for val in valeurs_mise:
           bouton_mise = tk.Button(racine, text=f"Miser {val} €", font=("Arial", 10),command=lambda v=val: ajouter_mise(v))
           bouton_mise.pack()
           boutons.append(bouton_mise)

       bouton_valider = tk.Button(racine, text="Valider la mise", command=valider_mise)
       bouton_valider.pack()

def ajouter_mise(montant):
    global mise
    mise += montant
    label_mise.config(text=f"Mise actuelle : {mise} €")
def valider_mise():
   global boutons, jeton, mise
   #grise boutons_mise
   for bouton_mise in boutons:
       bouton_mise.config(state="disabled")
   if mise <= jeton:
       mise_soumise()
   else:
       mise = 0
       label_mise.config(text=f"Mise actuelle : {mise} €")


def mise_soumise():
    global mise_utilisateur, jeton, bouton_valider , label_mise_acceptée, mise

    mise_utilisateur = mise
    jeton -= mise_utilisateur
    label_jetons.config(text=f"Vous avez {jeton} jetons.", font=("helvetica",14))
    label_mise_acceptée.config(text=f"Mise acceptée : {mise_utilisateur}")
    label_mise_acceptée.pack()
    bouton_valider.config(state="disabled")
    #fonction pour ditribuer les cartes
    mains_joueurs()
    print(f"Mise acceptée : {mise_utilisateur} Jetons : {jeton}")    

def mains_joueurs():
    global main_joueur, main_croupier, paquet, label_joueur, label_croupier
 
    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    if valeur(main_joueur)==21:
        blackjack()

    label_joueur = tk.Label(racine, text=f"Votre main : {main_joueur}, (Valeur: {valeur(main_joueur)})")
    label_joueur.pack()

    label_croupier = tk.Label(racine, text=f"Main du croupier : {main_croupier}, (Valeur : {valeur(main_croupier)})")
    label_croupier.pack()

    choix()

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

def play():
    """Supprime les widgets"""
    label_demarrage.destroy()
    bouton_quitter.destroy()
    bouton_demarrer.destroy()
    commencer_partie()

def quit():
    """Ferme la fenêtre principale."""
    racine.destroy()

def choix():
    global label_choix, bouton_tirer, bouton_rester, main_joueur, mise_utilisateur, jeton, bouton_doubler, bouton_split,bouton_abandonner

    if label_choix:
        label_choix.pack_forget()
    if bouton_tirer:
        bouton_tirer.pack_forget()
    if bouton_rester:
        bouton_rester.pack_forget()
    if bouton_doubler:
        bouton_doubler.pack_forget()
    if bouton_split:
        bouton_split.pack_forget()
    if bouton_abandonner:
        bouton_abandonner.pack_forget()

    label_choix = tk.Label(racine, text="Voulez-vous tirer ou rester? ")
    label_choix.pack()

    bouton_tirer = tk.Button(racine, text="Tirer", command=tirer)
    bouton_tirer.pack()

    bouton_rester = tk.Button(racine, text="Rester", command=rester)
    bouton_rester.pack()

    bouton_abandonner = tk.Button(racine, text="Abandonner", command=abandonner)
    bouton_abandonner.pack()

    if len(main_joueur) == 2 and main_joueur[0].split(" de ")[0] == main_joueur[1].split(" de ")[0]:
        bouton_split = tk.Button(racine, text="Split", command=partie_split)
        bouton_split.pack()

    if mise_utilisateur * 2 <= jeton:
        bouton_doubler = tk.Button(racine, text="Doubler votre mise", command=doubler)
        bouton_doubler.pack()    

def tirer():
    global main_joueur, game_over, paquet, label_joueur
    """Rajoute une carte au joueur"""
    if doubler:
        main_joueur.extend(carte(paquet, 1))
        label_joueur.config(text=f"Votre main : {main_joueur} (Valeur:{valeur(main_joueur)})")
        game_over = True
        croupier()
        resultat()

    elif not game_over and not valeur(main_joueur)>21:
        main_joueur.extend(carte(paquet, 1))
        label_joueur.config(text=f"Votre main : {main_joueur} (Valeur:{valeur(main_joueur)})")
        choix()

    elif valeur(main_joueur)>21:
        game_over= True
        croupier()
        resultat()

def rester():
    """Le joueur ne tire pas et passe son tour"""
    global game_over
    if not game_over:
        game_over=True
    croupier()
    resultat()

def croupier():
    """Définie le tour de jeu du croupier"""
    global game_over
    while valeur(main_croupier) < 17:
        main_croupier.extend(carte(paquet, 1))
        label_croupier.config(text=f"Main du croupier : {main_croupier}, (Valeur : {valeur(main_croupier)})")
    game_over = True

def blackjack():
    """Execute si blackjack"""
    global jeton

    message(f"Blackjack ! Vous gagnez {int(mise_utilisateur * 1.5)} jetons.")
    jeton+=int(mise_utilisateur * 1.5)

    bouton_tirer.pack_forget()
    bouton_rester.pack_forget()

    bouton_nv_manche = tk.Button(racine, text="Nouvelle Manche", command=nouvelle_manche)
    bouton_nv_manche.pack()

def resultat():
    """Renvoie les résultats du tour de jeu"""
    global jeton, abandon

    if abandon:
        message(f"Vous abandonnez, vous perdez la moitié de votre mise.")
        jeton+=mise_utilisateur // 2

    if valeur(main_joueur) > 21:
        message(f"Dust ! Vous perdez votre mise")
        jeton-=mise_utilisateur

    elif valeur(main_croupier)>21:
        message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
        jeton+=mise_utilisateur

    elif valeur(main_croupier)>valeur(main_joueur):
        message(f"Perdu! Vous perdez {mise_utilisateur} jetons.")

    elif valeur(main_joueur)>valeur(main_croupier):
        message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
        jeton+=mise_utilisateur

    elif valeur(main_joueur)==valeur(main_croupier):
        message("Egalité! Vous récuperez votre mise")
        jeton+=mise_utilisateur

    bouton_nv_manche = tk.Button(racine, text="Nouvelle Manche", command=nouvelle_manche)
    bouton_nv_manche.pack()

def message(message):
    """Affiche le résultat de la manche et désactive les boutons d'action."""
    global label_resultat
    label_resultat = tk.Label(racine, text=message, font=("helvetica", "16"))
    label_resultat.pack()

    if bouton_tirer:
        bouton_tirer.config(state="disabled")
    if bouton_rester:
        bouton_rester.config(state="disabled")
    if bouton_split:
        bouton_split.config(state="disabled")
    if bouton_doubler:
        bouton_doubler.config(state="disabled")
    if bouton_abandonner:
        bouton_abandonner.config(state="disabled")

def nouvelle_manche():
    """Réinitialise le jeu, démarre une nouvelle partie."""
    global main_joueur, main_croupier, game_over, mise_utilisateur, doubler_mise, paquet, mise

    game_over =False
    main_joueur=[]
    main_croupier=[]
    mise_utilisateur=0
    doubler_mise = False
    paquet = [f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]
    mise = 0
    for widget in racine.winfo_children(): #supprime tout les widgets
        widget.pack_forget()

    commencer_partie()

def abandonner():
    global abandon, game_over
    abandon=True
    game_over=True
    resultat()



#-------Doubler la mise----------

def doubler():
    global mise_utilisateur, jeton, doubler_mise
    doubler_mise = True
    mise_utilisateur *= 2
    label_mise.config(text=f"Votre mise est maintenant de {mise_utilisateur}.")
    label_jetons.config(text=f"Vous avez {jeton-mise_utilisateur} jetons.")
    tirer()

#------- Multijoueur-------------

# Liste des joueurs et gestion des tours
joueurs = []
tour_actuel = 0

def initialiser_joueurs(nb_joueurs):
    """Initialise les joueurs avec 100 jetons chacun."""
    global joueurs, tour_actuel
    joueurs = [{"nom": f"Joueur {i+1}", "jetons": 100, "main": [], "mise": 0} for i in range(nb_joueurs)]
    tour_actuel = 0
    commencer_tour()

def commencer_tour():
    """Démarre le tour du joueur actuel."""
    global tour_actuel
    joueur = joueurs[tour_actuel]
    label_joueur_actuel.config(text=f"{joueur['nom']} (Jetons : {joueur['jetons']})")
    commencer_partie()

def joueur_suivant():
    """Passe au tour du joueur suivant ou au croupier si tous les joueurs ont joué."""
    global tour_actuel, joueurs
    tour_actuel += 1
    if tour_actuel < len(joueurs):
        commencer_tour()
    else:
        croupier()
        afficher_resultats()

def afficher_resultats():
    """Affiche les résultats de la manche pour tous les joueurs."""
    for joueur in joueurs:
        valeur_main = valeur(joueur["main"])
        valeur_croupier = valeur(main_croupier)

        if valeur_main > 21:
            message(f"{joueur['nom']} a dépassé 21. Perdu.")
        elif valeur_croupier > 21 or valeur_main > valeur_croupier:
            joueur["jetons"] += joueur["mise"] * 2
            message(f"{joueur['nom']} a gagné {joueur['mise']} jetons.")
        elif valeur_main == valeur_croupier:
            joueur["jetons"] += joueur["mise"]
            message(f"{joueur['nom']} récupère sa mise (égalité).")
        else:
            message(f"{joueur['nom']} a perdu sa mise.")

    nouvelle_manche()
#-------Fenetre + boutons--------

racine = tk.Tk()
racine.title("Blackjack")
racine.geometry('500x500')

label_demarrage = tk.Label(racine, text="Blackjack !", padx=20, pady=20, font = ("helvetica", "30"))
label_demarrage.pack()

bouton_demarrer= tk.Button(racine, text="Play", font = ("helvetica", "30"), width=20, command=play)
bouton_demarrer.pack()

bouton_quitter= tk.Button(racine, text="Quit", font = ("helvetica", "30"), width=20, command=quit)
bouton_quitter.pack()


label_mise_acceptée = tk.Label(racine, text="", fg="green")


racine.mainloop()


# Création des labels pour afficher les mains
label_main_joueur = tk.Label(racine, text="Votre main : ", font=("Helvetica", 14))
label_main_joueur.grid(row=1, column=0, sticky="w")

label_main_croupier = tk.Label(racine, text="Main du croupier : ", font=("Helvetica", 14))
label_main_croupier.grid(row=2, column=0, sticky="w")

label_resultat = tk.Label(racine, text="", font=("Helvetica", 14))
label_resultat.grid(row=3, column=0, sticky="w")

# Boutons pour actions du joueur
bouton_tirer = tk.Button(racine, text="Tirer", command=tirer)
bouton_tirer.grid(row=4, column=0)

bouton_rester = tk.Button(racine, text="Rester", command=rester)
bouton_rester.grid(row=4, column=1)

 
 # à faire qui ne compte pas dans la note
 #interface oppérationnel /
 #ajout des nouvelles fonctions + bouttons
 
 #----------Nouvelles fonctions, autres pour la note --------
 # multijoueur 
 # gsetion des as, positionnement
 # graphisme avancée, image ( perfectionner l'interface graphique)
 #fonctions : les cotes de la main = strategie qui informe le joueur sur comment jouer la partie
 #           l'assurance : mise secondaire
