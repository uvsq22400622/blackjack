import tkinter as tk
import random as rd

def quit_game(event):
    """Ferme la fenêtre principale."""
    racine.destroy()

def play(event):
    """Supprime les widgets de démarrage et lance la partie."""
    label_demarrage.destroy()
    bouton_quitter.destroy()
    bouton_demarrer.destroy()
    partie(100)  # Initialise le joueur avec 100 jetons

def carte(paquet: list, n: int) -> list:
    """Génère un nombre n de cartes du paquet."""
    main = []
    for _ in range(n):
        carte_choisie = rd.choice(paquet)
        main.append(carte_choisie)
    return main

def valeur(main: list) -> int:
    """Renvoie la valeur des cartes dans une main."""
    valeur_totale = 0
    nb_as = 0
    for carte_choisie in main:
        rang = carte_choisie.split(" de ")[0]
        valeur_totale += rangs[rang]
        if rang == "As":
            nb_as += 1
    while valeur_totale > 21 and nb_as != 0:
        valeur_totale -= 10
        nb_as -= 1
    return valeur_totale

def partie(jeton: int):
    """Permet de jouer une partie en misant."""
    main_joueur = carte(paquet, 2)
    main_croupier = carte(paquet, 1)

    label_joueur = tk.Label(racine, text=f"Votre main : {main_joueur} (Valeur: {valeur(main_joueur)})")
    label_joueur.pack()
    label_croupier = tk.Label(racine, text=f"Carte visible du croupier : {main_croupier} (Valeur : {valeur(main_croupier)})")
    label_croupier.pack()

    label_mise = tk.Label(racine, text=f"Votre solde de jetons est de {jeton}. Combien voulez-vous miser pour cette partie?")
    label_mise.pack()
    entry_mise = tk.Entry(racine)
    entry_mise.pack()

    def valider_mise():
        """Valide la mise de l'utilisateur."""
        nonlocal jeton  # Permet de modifier la variable jeton de la fonction partie
        try:
            mise_utilisateur = int(entry_mise.get())
            if 0 < mise_utilisateur <= jeton:
                # Logique du jeu ici (tirer, rester, etc.)
                print(f"Mise acceptée : {mise_utilisateur}") #test
                label_mise.destroy()
                entry_mise.destroy()
                bouton_valider.destroy()

            else:
                label_erreur = tk.Label(racine, text="Votre mise n'est pas valide, veuillez entrer un montant valide!")
                label_erreur.pack()

        except ValueError:
            label_erreur = tk.Label(racine, text="Veuillez entrer un nombre entier!")
            label_erreur.pack()

    bouton_valider = tk.Button(racine, text="Valider la mise", command=valider_mise)
    bouton_valider.pack()

rangs = {"As": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Valet": 10, "Dame": 10, "Roi": 10}
couleurs = ["Coeur", "Trèfle", "Carreau", "Pique"]
paquet = [f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]

# Création du menu du jeu
racine = tk.Tk()
racine.title("Blackjack")

label_demarrage = tk.Label(racine, text="Blackjack !", padx=20, pady=20, font=("helvetica", "30"))
label_demarrage.grid(row=0, column=0, columnspan=2)

bouton_demarrer = tk.Button(racine, text="Play", font=("helvetica", "30"), width=50)
bouton_demarrer.bind("<Button-1>", play)
bouton_demarrer.grid(row=1, column=0)

bouton_quitter = tk.Button(racine, text="Quit", font=("helvetica", "30"), width=50)
bouton_quitter.bind("<Button-1>", quit_game)
bouton_quitter.grid(row=2, column=0)

racine.mainloop()