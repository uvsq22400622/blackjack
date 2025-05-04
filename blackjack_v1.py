import tkinter as tk
import random as rd

# ------- Fonctions ---------------
rangs = {"As": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
         "7": 7, "8": 8, "9": 9, "10": 10, "Valet": 10, "Dame": 10, "Roi": 10}
couleurs = ['♠', '♥', '♦', '♣']
couleurs_cartes = {"♠": "black", "♣": "black", "♥": "red", "♦": "red"}
paquet = [f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

mise_utilisateur = 0
jeton = 100

game_over = False
doubler_mise = False
abandon = False
split = False
mise = 0
boutons = []
#tour_actuel = 0
#label_choix = None
bouton_tirer = None
bouton_rester = None
bouton_splitter = None
bouton_doubler = None
bouton_abandonner = None
bouton_nv_manche = None
bouton_nv_partie = None

def carte(paquet: list, n: int) -> list:
    main = []
    for _ in range(n):
        carte = rd.choice(paquet)
        paquet.remove(carte)
        main.append(carte)
    return main

def quitter():
    racine.destroy()

def play():
    frame_cadre_gris.grid_forget()
    frame_boutons.grid_forget()
    label_credits.grid_forget()
    label_decoration.grid_forget()
    commencer_partie()

def nouvelle_partie():
    global mise,jeton, bouton_quit, label_fin_de_jeu, bouton_nv_partie
    jeton = 100
    mise = 0
    bouton_quit.grid_forget()
    label_fin_de_jeu.grid_forget()
    bouton_nv_partie.grid_forget()
    commencer_partie()

def commencer_partie():
    global label_jetons, label_mise, bouton_valider, label_fin_de_jeu, bouton_quit, bouton_nv_partie

    if jeton <= 0:
        label_fin_de_jeu = tk.Label(racine, text="Vous n'avez plus de jeton, le jeu est terminé", font=("helvetica", 14))
        label_fin_de_jeu.grid(row=1, column=0, columnspan=2, pady=20)
        bouton_quit = tk.Button(racine, text="Quit", font=("Arial", 20), width=20, command=quitter)
        bouton_quit.grid(row=2, column=0, columnspan=2, pady=10)
        bouton_nv_partie = tk.Button(racine, text="Nouvelle Partie", command=nouvelle_partie, fg="white", bg="gray22")
        bouton_nv_partie.grid(row=3,column=0,columnspan=3)
        return

    # Cadre principal de la partie
    cadre_mise = tk.Frame(racine, bg="gray22", bd=2, padx=10, pady=10)
    cadre_mise.grid(row=1, column=1, columnspan=2, pady=(20, 10), sticky="n")

    label_jetons = tk.Label(cadre_mise, text=f"Vous avez {jeton} jetons.", font=("helvetica", 14), fg="white", bg="gray22")
    label_jetons.grid(row=0, column=0, columnspan=3, pady=5)

    label_mise = tk.Label(cadre_mise, text="Combien voulez-vous miser ?", fg="white", bg="gray22")
    label_mise.grid(row=1, column=0, columnspan=3, pady=5)

    valeurs_mise = [1, 5, 10, 25, 50, 100]
    for i, val in enumerate(valeurs_mise):
        bouton_mise = tk.Button(cadre_mise, text=f"Miser {val} €", font=("Arial", 10), width=12,
                                command=lambda v=val: ajouter_mise(v))
        bouton_mise.grid(row=2 + i // 2, column=i % 2, padx=5, pady=5)
        boutons.append(bouton_mise)

    bouton_valider = tk.Button(cadre_mise, text="Valider la mise", font=("Arial", 12), command=valider_mise)
    bouton_valider.grid(row=5, column=0, columnspan=3, pady=10)

def ajouter_mise(montant):
    global mise
    mise += montant
    label_mise.config(text=f"Mise actuelle : {mise} €")

def valider_mise():
   global boutons, jeton, mise
   #grise boutons_mise
   for bouton_mise in boutons:
       bouton_mise.config(state="disabled")
   if mise >0 and mise <= jeton :
       mise_soumise()
   else:
       mise = 0
       label_mise.config(text=f"Mise actuelle : {mise} €")
       quit()

def mise_soumise():
    global mise_utilisateur, jeton, bouton_valider , label_mise, mise

    mise_utilisateur = mise
    jeton -= mise_utilisateur
    label_jetons.config(text=f"Vous avez {jeton} jetons.", font=("helvetica",14))
    label_mise.config(text=f"Mise acceptée : {mise_utilisateur}")
    bouton_valider.config(state="disabled")
    #fonction pour ditribuer les cartes
    mains_joueurs()
    print(f"Mise acceptée : {mise_utilisateur} Jetons : {jeton}")   

def mains_joueurs():
    global main_joueur, main_croupier, paquet, label_joueur, label_croupier, cadre_joueurs, cadre_joueur, cadre_resultat
 
    main_joueur=carte(paquet,2) #Création de la main initiale du joueur.
    main_croupier=carte(paquet,1) #Création de la main initiale du croupier.

    if valeur(main_joueur)==21:
        blackjack()

    cadre_resultat = tk.Frame(racine,bd=2, padx=10, pady=10, bg="aquamarine4")
    cadre_resultat.grid(row=0, column=0, columnspan=4)

    cadre_joueurs = tk.Frame(racine, bg="gray22",bd=2, padx=10, pady=10)
    cadre_joueurs.grid(row=1, column=0, columnspan=1, pady=(20, 10), sticky="n")

    cadre_croupier = tk.Frame(cadre_joueurs,bg="gray22", bd=2, padx=10, pady=10)
    cadre_croupier.grid(row=1, column=0, columnspan=2)
    
    label_croupier = tk.Label(cadre_croupier, text=f"Main du croupier : {main_croupier} = ({valeur(main_croupier)})",bg="gray22",
                              fg="white",font=("Arial", 10))
    label_croupier.grid(row=2, column=0, columnspan=2)

    #affichage stylisé de la main du joueur:
    cadre_joueur = tk.Frame(cadre_joueurs, bg="gray22", bd=2, padx=10, pady=10)
    cadre_joueur.grid(row=2,column=0,columnspan=2)
    
    affichage_main_joueur()

    choix()

def affichage_main_joueur():
    global cadre_joueur, couleurs_cartes

    # supression => pas empiler
    for widget in cadre_joueur.winfo_children():
        widget.destroy()

    # titre des cartes
    titre_label = tk.Label(cadre_joueur, text=f"Votre main = ({valeur(main_joueur)})",
                           bg="gray22", fg="white", font=("Arial", 10))
    titre_label.grid(row=0, column=0, columnspan=len(main_joueur), pady=(0, 10))

    # Affichage stylisé des cartes
    for i, carte_txt in enumerate(main_joueur):
        rang, couleur = carte_txt.split(" de ")
        symbole = couleur.strip()[0]  # ♠ ♥ ♦ ♣
        couleur_texte = couleurs_cartes.get(symbole, "black")

        carte_label = tk.Label(cadre_joueur, text=f"{rang}\n{symbole}",
                               bg="ivory", fg=couleur_texte,
                               font=("Courier", 10, "bold"),
                               relief="raised", bd=3,
                               width=6, height=3)
        carte_label.grid(row=1, column=i, padx=5)

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

def choix():
    global bouton_tirer, bouton_rester, main_joueur, mise_utilisateur, jeton, bouton_doubler, bouton_splitter, bouton_abandonner #label_choix

    #if label_choix:
    #    label_choix.grid_forget()
    if bouton_tirer and bouton_tirer.winfo_exists(): 
        bouton_tirer.grid_forget()
        bouton_tirer = None
    if bouton_rester and bouton_rester.winfo_exists():
        bouton_rester.grid_forget()
        bouton_rester = None
    if bouton_doubler and bouton_doubler.winfo_exists():
        bouton_doubler.grid_forget()
        bouton_doubler = None
    if bouton_splitter and bouton_splitter.winfo_exists():
        bouton_splitter.grid_forget()
        bouton_splitter = None
    if bouton_abandonner and bouton_abandonner.winfo_exists():
        bouton_abandonner.grid_forget()
        bouton_abandonner = None

    #label_choix = tk.Label(cadre_joueurs, text="Voulez-vous tirer ou rester? ")
    #label_choix.grid(row=3, column=0, columnspan= 2)

    bouton_tirer = tk.Button(cadre_joueur, text="Tirer", command=tirer)
    bouton_tirer.grid(row=4,column=1)

    bouton_rester = tk.Button(cadre_joueur, text="Rester", command=rester)
    bouton_rester.grid(row=4, column=0)

    bouton_abandonner = tk.Button(cadre_joueur, text="Abandonner", command=abandonner)
    bouton_abandonner.grid(row=5,column=0)

    if mise_utilisateur * 2 <= jeton:
        bouton_doubler = tk.Button(cadre_joueur, text="Doubler votre mise", command=doubler)
        bouton_doubler.grid(row=5, column=1) 
    
    if len(main_joueur) == 2 and rangs[main_joueur[0].split(" de ")[0]] == rangs[main_joueur[1].split(" de ")[0]] and jeton>=mise_utilisateur:
            bouton_splitter = tk.Button(cadre_joueur, text="Split", command=splitter)
            bouton_splitter.grid(row=6, column=0, columnspan= 2)

def tirer():
    global main_joueur, game_over, paquet, doubler_mise, label_main_joueur_1, label_main_joueur_2, split, main_actuelle, main_joueur_1, main_joueur_2
    """Rajoute une carte au joueur"""
    if doubler_mise:
        main_joueur.extend(carte(paquet, 1))
        affichage_main_joueur()
        doubler_mise = False
        game_over = True
        croupier()
        resultat()
    elif split:
        if main_actuelle == 1:
            main_joueur_1.extend(carte(paquet,1))
            label_main_joueur_1.config(text=f"Votre première main : {main_joueur_1} (Valeur: {valeur(main_joueur_1)})")
            if valeur(main_joueur_1)>=21:
                main_actuelle = 2
            jouer_main_split()
        elif main_actuelle == 2:
            main_joueur_2.extend(carte(paquet,1))
            label_main_joueur_2.config(text=f"Votre seconde main : {main_joueur_2} (Valeur: {valeur(main_joueur_2)})")
            if valeur(main_joueur_2)>=21:
                game_over = True
                croupier()
                resultat_split()
            else:
                jouer_main_split()

    elif not game_over:
        main_joueur.extend(carte(paquet, 1))
        affichage_main_joueur()
        if valeur(main_joueur) > 21:
            game_over= True
            croupier()
            resultat()
        if valeur(main_joueur) == 21:
            game_over= True
            croupier()
            resultat()
        else:
            choix()

def rester():
    """Le joueur ne tire pas et passe son tour"""
    global game_over, split, main_actuelle
    if split:
        if main_actuelle == 1:
            main_actuelle = 2
            jouer_main_split()
        elif main_actuelle == 2:
            game_over = True
            croupier()
            resultat_split()
    else:      
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
    global jeton, mise_utilisateur, bouton_nv_manche

    message(f"Blackjack ! Vous gagnez {int(mise_utilisateur * 2.5)} jetons.")
    jeton+=int(mise_utilisateur * 2.5)

    bouton_tirer.grid_forget()
    bouton_rester.grid_forget()
    print("blackjack !")

    bouton_nv_manche = tk.Button(racine, text="Nouvelle Manche", command=nouvelle_manche, fg="white", bg="gray22")
    bouton_nv_manche.grid(row=3,column=0,columnspan=3)

def resultat():
    """Renvoie les résultats du tour de jeu"""
    global jeton, abandon, bouton_nv_manche #, label_choix

    #label_choix.grid_forget()

    if abandon:
        message(f"Vous abandonnez, vous perdez la moitié de votre mise.")
        jeton+=mise_utilisateur // 2

    if valeur(main_joueur) > 21:
        message(f"Dust ! Vous perdez votre mise")
        jeton-=mise_utilisateur

    elif valeur(main_croupier)>21:
        message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
        jeton+=mise_utilisateur*2

    elif valeur(main_croupier)>valeur(main_joueur):
        message(f"Perdu! Vous perdez {mise_utilisateur} jetons.")
        jeton-=mise_utilisateur

    elif valeur(main_joueur)>valeur(main_croupier):
        message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
        jeton+=mise_utilisateur*2

    elif valeur(main_joueur)==valeur(main_croupier):
        message("Egalité! Vous récuperez votre mise")
        jeton+=mise_utilisateur
    elif valeur(main_joueur)==21:
        blackjack()
    
    
    if bouton_nv_manche is None:
            bouton_nv_manche = tk.Button(racine, text="Nouvelle Manche", command=nouvelle_manche, fg="white", bg="gray22")
            bouton_nv_manche.grid(row=8,column=0,columnspan=3)
            print("Bouton Nouvelle Manche créé et affiché.")
    else:
        bouton_nv_manche.grid(row=8, column=0, columnspan=3)
        print("Bouton Nouvelle Manche déjà existant, réaffiché.")
   

def message(message):
    """Affiche le résultat de la manche et désactive les boutons d'action."""
    global label_resultat

    label_resultat = tk.Label(cadre_resultat, text=message, font=("helvetica", "16"),fg="white", bg="gray22")
    label_resultat.grid()

    if bouton_tirer and bouton_tirer.winfo_exists():
        bouton_tirer.config(state="disabled")
    if bouton_rester and bouton_rester.winfo_exists():
        bouton_rester.config(state="disabled")
    if bouton_splitter and bouton_splitter.winfo_exists():
        bouton_splitter.config(state="disabled")
    if bouton_doubler and bouton_doubler.winfo_exists():
        bouton_doubler.config(state="disabled")
    if bouton_abandonner and bouton_abandonner.winfo_exists():
        bouton_abandonner.config(state="disabled")

def nouvelle_manche():
    """Réinitialise le jeu, démarre une nouvelle partie."""
    global main_joueur, main_croupier, game_over, mise_utilisateur, doubler_mise, paquet, mise, abandon, split, main_actuelle

    game_over = False
    abandon = False
    split = False

    main_joueur=[]
    main_croupier=[]

    mise_utilisateur=0
    main_actuelle = 0

    doubler_mise = False
    paquet = [f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]
    mise = 0
    for widget in racine.winfo_children(): #supprime tout les widgets
        widget.grid_forget()

    commencer_partie()

#---------Abandonner------------

def abandonner():
    global abandon, game_over
    abandon=True
    game_over=True
    resultat()

#---------Doubler-------------

def doubler():
    global mise_utilisateur, jeton, doubler_mise
    doubler_mise = True
    mise_utilisateur *= 2
    label_mise.config(text=f"Votre mise est maintenant de {mise_utilisateur}.")
    label_jetons.config(text=f"Vous avez {jeton-mise_utilisateur} jetons.")
    tirer()

#---------Splitter-------------

def splitter():
    global main_joueur, main_joueur_1, main_joueur_2, split, main_actuelle, jeton, mise_utilisateur

    split = True
    main_actuelle = 1

    main_joueur_1 = [main_joueur[0]]
    main_joueur_2 = [main_joueur[1]]

    main_joueur_1.extend(carte(paquet, 1))
    main_joueur_2.extend(carte(paquet, 1))

    jeton-=mise_utilisateur

    jouer_main_split()
    
def jouer_main_split():
    global main_actuelle, main_joueur_1, main_joueur_2, label_main_joueur_1, label_main_joueur_2, cadre_joueur

    cadre_split = tk.Frame(racine, bg="gray22",bd=2, padx=10, pady=10)
    cadre_split.grid(row=2, column=0, columnspan=2, pady=(20, 10), sticky="s")
    
    if main_actuelle == 1:
        label_main_joueur_1 = tk.Label(cadre_split, text=f"Votre première main : {main_joueur_1}, (Valeur: {valeur(main_joueur_1)})",bg="gray22",fg="white",font=("Arial", 10))
        label_main_joueur_1.grid()
    elif main_actuelle == 2:
        label_main_joueur_2 = tk.Label(cadre_split, text=f"Votre seconde main : {main_joueur_2}, (Valeur: {valeur(main_joueur_2)})",bg="gray22",fg="white",font=("Arial", 10))
        label_main_joueur_2.grid()
    
    choix()

def resultat_split():
    global jeton

    for resultat in [valeur(main_joueur_1), valeur(main_joueur_2)]:
        if resultat > 21:
            message(f"Dust ! Vous perdez votre mise")
            jeton-=mise_utilisateur

        elif valeur(main_croupier)>21:
            message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
            jeton+=mise_utilisateur*2

        elif valeur(main_croupier)>resultat:
            message(f"Perdu! Vous perdez {mise_utilisateur} jetons.")
            jeton-=mise_utilisateur

        elif resultat>valeur(main_croupier):
            message(f"Victoire! Vous gagnez {mise_utilisateur} jetons.")
            jeton+=mise_utilisateur*2

        elif resultat==valeur(main_croupier):
            message("Egalité! Vous récuperez votre mise")
            jeton+=mise_utilisateur
    
    bouton_nv_manche = tk.Button(racine, text="Nouvelle Manche", command=nouvelle_manche)
    bouton_nv_manche.grid(row=3,column=0,columnspan=3)

# ------- Fenêtre principale -------
racine = tk.Tk()
racine.title("Blackjack")
racine.geometry('800x500')
racine.configure(bg="aquamarine4")

# Ligne 0 : Titre
frame_cadre_gris = tk.Frame(racine, bg="gray22", bd=2, padx=10, pady=10)
frame_cadre_gris.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

label_demarrage = tk.Label(frame_cadre_gris, text="Blackjack", padx=20, pady=20, font=("Courier", 30, "bold"),
    bg="snow4",fg="white")
label_demarrage.grid(row=0, column=0)

label_decoration = tk.Label(racine, bg="aquamarine4", text="♠ ♥ ♦ ♣", fg="gray22",font = ("Courier", "30", "bold"))
label_decoration.grid(row=1,column=0,columnspan=2)

# artificielle
racine.grid_columnconfigure(0, weight=1)
racine.grid_columnconfigure(1, weight=1)

# Ligne 1 : Boutons "Play" et "Quit"
frame_boutons = tk.Frame(racine, bg="aquamarine4")
frame_boutons.grid(row=2, column=0, columnspan=2)

bouton_demarrer = tk.Button(frame_boutons, text="Play", font=("Arial", 20, "bold"), width=20, fg="white", bg="gray22", command=play)
bouton_demarrer.grid(row=0, column=0, padx=10, pady=5)

bouton_quitter = tk.Button(frame_boutons, text="Quit", font=("Arial", 20, "bold"), width=20, fg="white", bg="gray22", command=quit)
bouton_quitter.grid(row=1, column=0, padx=10, pady=5)

# Ligne 2 : Crédits
label_credits = tk.Label(racine, text="Sophie, Laura, Fanilo, Yacine", font=("Arial", 10), bg="aquamarine4", fg="white")
label_credits.grid(row=3, column=0, columnspan=2, pady=20, sticky="s")

racine.mainloop()
