import tkinter as tk

#-------Fenetre + boutons--------
racine = tk.Tk()

racine.title("Blackjack")
racine.geometry('360x450')
racine.configure(bg = "aquamarine4")

frame_cadre_rouge = tk.Frame(racine, bg="gray22", bd=2, padx=10, pady=10)
frame_cadre_rouge.pack(padx=20, pady=(20,10))

label_demarrage = tk.Label(frame_cadre_rouge, text="Blackjack", padx=20, pady=20, font = ("Courier", "30", "bold"), bg="snow4", fg="white")
label_demarrage.pack(pady=5)

#bd créer une bordure de 2 pixels d'epaisseur, relief = effet visuel

frame = tk.Frame(racine, bg="aquamarine4") #conteneur pour centrer les boutons
frame.pack(expand=True) #centre verticalement

bouton_demarrer= tk.Button(frame, text="Play", font = ("Arial", "20", "bold"), width=20, fg="white", bg="gray22")
bouton_demarrer.pack(pady=5)

bouton_quitter= tk.Button(frame, text="Quit", font = ("Arial", "20", "bold"), width=20, fg="white", bg="gray22")
bouton_quitter.pack(pady=5)

label_credits = tk.Label(racine, text="Sophie, Laura, Fanilo, Yacine", font=("Arial",10), bg="aquamarine4", fg="white")
label_credits.pack(side="bottom", pady=10)

racine.mainloop()
