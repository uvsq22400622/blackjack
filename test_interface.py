import tkinter as tk
import random as rd

# ------- Fonctions ---------------
rangs = {"As": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
         "7": 7, "8": 8, "9": 9, "10": 10, "Valet": 10, "Dame": 10, "Roi": 10}
couleurs = ['♠', '♥', '♦', '♣']
paquet = [f"{rang} de {couleur}" for rang in rangs for couleur in couleurs]
mise_utilisateur = 0
jeton = 100
game_over = False
doubler_mise = False
mise = 0
boutons = []

def carte(paquet: list, n: int) -> list:
    main = []
    for _ in range(n):
        carte = rd.choice(paquet)
        paquet.remove(carte)
        main.append(carte)
    return main

def quit():
    racine.destroy()

def play():
    frame_cadre_gris.grid_forget()
    frame_boutons.grid_forget()
    commencer_partie()

def commencer_partie():
    global label_jetons, label_mise, bouton_valider

    if jeton <= 0:
        label_fin_de_jeu = tk.Label(racine, text="Vous n'avez plus de jeton, le jeu est terminé", font=("helvetica", 14))
        label_fin_de_jeu.grid(row=1, column=0, columnspan=2, pady=20)
        bouton_quit = tk.Button(racine, text="Quit", font=("Arial", 20), width=20, command=quit)
        bouton_quit.grid(row=2, column=0, columnspan=2, pady=10)
        return

    # Cadre principal de la partie
    cadre_mise = tk.Frame(racine, bg="gray22", bd=2, padx=10, pady=10)
    cadre_mise.grid(row=1, column=0, columnspan=2, pady=(20, 10), sticky="n")

    label_jetons = tk.Label(cadre_mise, text=f"Vous avez {jeton} jetons.", font=("helvetica", 14), fg="white", bg="gray22")
    label_jetons.grid(row=0, column=0, columnspan=3, pady=5)

    label_mise = tk.Label(cadre_mise, text="Combien voulez-vous miser ?", fg="white", bg="gray22")
    label_mise.grid(row=1, column=0, columnspan=3, pady=5)

    valeurs_mise = [1, 5, 10, 25, 50, 100]
    for i, val in enumerate(valeurs_mise):
        bouton_mise = tk.Button(cadre_mise, text=f"Miser {val} €", font=("Arial", 10), width=12,
                                command=lambda v=val: ajouter_mise(v))
        bouton_mise.grid(row=2 + i // 3, column=i % 3, padx=5, pady=5)
        boutons.append(bouton_mise)

    bouton_valider = tk.Button(cadre_mise, text="Valider la mise", font=("Arial", 12), command=valider_mise)
    bouton_valider.grid(row=4, column=0, columnspan=3, pady=10)

def ajouter_mise(val):
    global mise
    mise += val
    print(f"Mise actuelle : {mise} €") 

def valider_mise():
    print("Mise validée :", mise) 

# ------- Fenêtre principale -------
racine = tk.Tk()
racine.title("Blackjack")
racine.geometry('600x600')
racine.configure(bg="aquamarine4")

# Ligne 0 : Titre
frame_cadre_gris = tk.Frame(racine, bg="gray22", bd=2, padx=10, pady=10)
frame_cadre_gris.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

label_demarrage = tk.Label(frame_cadre_gris, text="Blackjack", padx=20, pady=20, font=("Courier", 30, "bold"),
    bg="snow4",fg="white")
label_demarrage.grid(row=0, column=0)

# artificielle
racine.grid_columnconfigure(0, weight=1)
racine.grid_columnconfigure(1, weight=1)

# Ligne 1 : Boutons "Play" et "Quit"
frame_boutons = tk.Frame(racine, bg="aquamarine4")
frame_boutons.grid(row=1, column=0, columnspan=2)

bouton_demarrer = tk.Button(frame_boutons, text="Play", font=("Arial", 20, "bold"), width=20, fg="white", bg="gray22", command=play)
bouton_demarrer.grid(row=0, column=0, padx=10, pady=5)

bouton_quitter = tk.Button(frame_boutons, text="Quit", font=("Arial", 20, "bold"), width=20, fg="white", bg="gray22", command=quit)
bouton_quitter.grid(row=1, column=0, padx=10, pady=5)

# Ligne 2 : Crédits
label_credits = tk.Label(racine, text="Sophie, Laura, Fanilo, Yacine", font=("Arial", 10), bg="aquamarine4", fg="white")
label_credits.grid(row=2, column=0, columnspan=2, pady=20)

racine.mainloop()
