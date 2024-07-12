# les fonction importé
import tkinter as tk
import random
from tkinter import messagebox

# Constants
ROWS = 8 #numero de ligne
COLS = 8 # numero de colonnes
CELL_SIZE = 100  # demention des carrés colorés

# liste des colors de notre jeu
COLORS = ["red", "green", "blue", "yellow", "orange"]

# tableau des coleurs choisis aléatoirement avec la bibliothèque RANDOM
board = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

# tableau des couleurs choisis par le joueur
selected_candies = []

# Score
score = 0

def select_candy(row, col):
    candy_color = board[row][col]
    selected_candies.append((row, col))

    if len(selected_candies) >= 2:
        # Check if candies are adjacent
        if abs(selected_candies[-1][0] - selected_candies[-2][0]) + abs(selected_candies[-1][1] - selected_candies[-2][1]) == 1:
            swap_candies()
        else:
            selected_candies.pop(0)

    draw_board()

def swap_candies():
    row1, col1 = selected_candies[-2]
    row2, col2 = selected_candies[-1]
    board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

    if not find_matches():
        # 
        board[row1][col1], board[row2][col2] = board[row2][col2], board[row1][col1]

    selected_candies.clear()
    handle_matches()

# fonction pour verifier si les carrés sont identiques
def find_matches():
    matched_candies = set()
    for row in range(ROWS):
        for col in range(COLS):
            candy = board[row][col]
            if candy == "":
                continue

            # verifier l'alignement horizontal
            if col + 2 < COLS and board[row][col + 1] == candy and board[row][col + 2] == candy:
                matched_candies.update([(row, col), (row, col + 1), (row, col + 2)])

            # verifier l'alignement vertical
            if row + 2 < ROWS and board[row + 1][col] == candy and board[row + 2][col] == candy:
                matched_candies.update([(row, col), (row + 1, col), (row + 2, col)])

    return matched_candies

# cette fonction est récursive, elle permet de supprimer des couleur allignés remplire le vide et redissiner le tableau
def handle_matches():
    matched_candies = find_matches()
    if matched_candies:
        remove_matches(matched_candies)
        refill_board()
        handle_matches()  # fonction récursive 
    draw_board()

# fonction pour supprimer
def remove_matches(matched_candies):
    global score
    for row, col in matched_candies:
        board[row][col] = ""
        score += 30

# fonction pour remplir les vide aléatoirement 
def refill_board():
    for col in range(COLS):

        empty_cells = [row for row in range(ROWS) if board[row][col] == ""]
        if not empty_cells:
            continue

        for row in range(empty_cells[0] - 1, -1, -1):
            board[empty_cells.pop()][col] = board[row][col]
            board[row][col] = ""

        for row in empty_cells:
            board[row][col] = random.choice(COLORS)


# la fonction qui affiche nos couleurs sous forme des carrés dans la zone CANVAS
def draw_board():
    canvas.delete("all")

    for row in range(ROWS):
        for col in range(COLS):
            x1, y1 = col * CELL_SIZE, row * CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            color = board[row][col]
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)

    for row, col in selected_candies:
        x1, y1 = col * CELL_SIZE, row * CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        canvas.create_rectangle(x1, y1, x2, y2, outline="black", width=2)

    score_label.config(text=f"Score: {score}")

def click(event):
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    select_candy(row, col)

# Quiter mode pleine ecran
def fs_exit(event):
    confirmer = messagebox.askokcancel(title="Quit the Game", message='Are you sure you want to exit the game?')
    if confirmer:
        root.destroy()

# Initialisation de la fenetre Principale
root = tk.Tk()
root.title("match it")
root.attributes('-fullscreen', True)
root.bind("<Escape>", fs_exit)

canvas = tk.Canvas(root, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg='white')
canvas.pack(side=tk.RIGHT, padx=120)

btn = tk.Button(root, text="START THE GAME", bg="blue", fg="white", font=("Helvetica", 22), width=300, command=draw_board)
btn.pack(side=tk.LEFT, padx=50, pady=50)

score_label = tk.Label(root, textvariable=f"Score: {score}", font=("Helvetica", 10), fg="black", bg="red")
score_label.pack(side=tk.LEFT, padx=20, pady=20)

canvas.bind("<Button-1>", click)

# Lancer  la fenetre principale
root.mainloop()