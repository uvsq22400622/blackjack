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
import random as rd
import tkinter as tk

racine = tk.Tk()
racine.title("Blackjack")

canvas = tk.Canvas(racine, text="Le jeu démarre")


cartes = {"2":2, "3":3, "4":4, "5":5, "6":6,"7":7,"8":8, "9":9, "10": 10, "Valet":10, "Dame":10, "Roi":10,
          "as" : 1 or 11}