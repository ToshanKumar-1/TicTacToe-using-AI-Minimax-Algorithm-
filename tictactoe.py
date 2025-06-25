import tkinter as tk
from functools import partial
from tkinter import messagebox
from playsound import playsound
import random
import threading

# Initialize
window = tk.Tk()
window.title("Tic Tac Toe - AI (Minimax)")
window.configure(bg="#1e1e1e")

buttons = [[None for _ in range(3)] for _ in range(3)]
board = [["" for _ in range(3)] for _ in range(3)]
player_score = 0
ai_score = 0
difficulty = tk.StringVar(value="Hard")

# Sound helper (non-blocking)
def play_sound(file):
    threading.Thread(target=playsound, args=(file,), daemon=True).start()

# Game logic
def is_winner(player):
    for row in board:
        if all(cell == player for cell in row): return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)): return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)): return True
    return False

def is_full():
    return all(cell != "" for row in board for cell in row)

def minimax(is_max):
    if is_winner("O"): return 1
    if is_winner("X"): return -1
    if is_full(): return 0

    if is_max:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    best = max(best, minimax(False))
                    board[i][j] = ""
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    best = min(best, minimax(True))
                    board[i][j] = ""
        return best

def best_move():
    level = difficulty.get()
    empty = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]

    if level == "Easy":
        return random.choice(empty)
    if level == "Medium" and random.random() < 0.5:
        return random.choice(empty)

    move = (-1, -1)
    best_score = -float("inf")
    for i, j in empty:
        board[i][j] = "O"
        score = minimax(False)
        board[i][j] = ""
        if score > best_score:
            best_score = score
            move = (i, j)
    return move

def update_score_label():
    score_label.config(text=f"You: {player_score}   AI: {ai_score}")

def reset_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state="normal", bg="#333", fg="white")
    update_score_label()

def click(i, j):
    global player_score, ai_score

    if board[i][j] == "" and not is_winner("X") and not is_winner("O"):
        board[i][j] = "X"
        buttons[i][j].config(text="X", state="disabled", disabledforeground="cyan")
        buttons[i][j].config(bg="#004d4d")  # Animation effect
        play_sound("click.mp3")

        if is_winner("X"):
            player_score += 1
            messagebox.showinfo("Game Over", "You Win!")
            reset_game()
            return

        if is_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            reset_game()
            return

        ai_i, ai_j = best_move()
        board[ai_i][ai_j] = "O"
        buttons[ai_i][ai_j].config(text="O", state="disabled", disabledforeground="orange")
        buttons[ai_i][ai_j].config(bg="#4d0000")
        play_sound("click.mp3")

        if is_winner("O"):
            ai_score += 1
            messagebox.showinfo("Game Over", "AI Wins!")
            reset_game()
        elif is_full():
            messagebox.showinfo("Game Over", "It's a Draw!")
            reset_game()

# Grid
for i in range(3):
    for j in range(3):
        btn = tk.Button(window, text="", width=10, height=4, bg="#333", fg="white",
                        activebackground="#444", font=("Helvetica", 20),
                        command=partial(click, i, j))
        btn.grid(row=i, column=j, padx=5, pady=5)
        buttons[i][j] = btn

# Score Label
score_label = tk.Label(window, text="You: 0   AI: 0", bg="#1e1e1e", fg="white", font=("Helvetica", 16))
score_label.grid(row=3, column=0, columnspan=3, pady=10)

# Reset Button
reset_btn = tk.Button(window, text="Reset", command=reset_game, font=("Helvetica", 14),
                      bg="#555", fg="white", width=10)
reset_btn.grid(row=4, column=0, columnspan=3, pady=5)

# Difficulty
difficulty_label = tk.Label(window, text="Difficulty:", bg="#1e1e1e", fg="white", font=("Helvetica", 14))
difficulty_label.grid(row=5, column=0, pady=5)

difficulty_menu = tk.OptionMenu(window, difficulty, "Easy", "Medium", "Hard")
difficulty_menu.config(bg="#555", fg="white", font=("Helvetica", 12), width=10)
difficulty_menu.grid(row=5, column=1, columnspan=2, pady=5)

# Run App
window.mainloop()
