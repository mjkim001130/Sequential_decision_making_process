import numpy as np
import random
import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = np.zeros((3, 3), dtype=int)
        self.current_player = 1

    def is_valid_move(self, x, y):
        return self.board[x, y] == 0

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x, y] = player
            self.current_player = -player
            return True
        return False

    def check_winner(self):
        for i in range(3):
            if abs(sum(self.board[i, :])) == 3:
                return np.sign(sum(self.board[i, :]))
            if abs(sum(self.board[:, i])) == 3:
                return np.sign(sum(self.board[:, i]))
        diag1 = sum([self.board[i, i] for i in range(3)])
        diag2 = sum([self.board[i, 2 - i] for i in range(3)])
        if abs(diag1) == 3:
            return np.sign(diag1)
        if abs(diag2) == 3:
            return np.sign(diag2)
        if not any(0 in row for row in self.board):
            return 0  
        return None

class SimpleAgent:
    def __init__(self, player):
        self.player = player

    def get_move(self, game):
        possible_moves = [(i, j) for i in range(3) for j in range(3) if game.is_valid_move(i, j)]
        
        for move in possible_moves:
            x, y = move
            game.board[x, y] = self.player
            if game.check_winner() == self.player:
                game.board[x, y] = 0 
                return move
            game.board[x, y] = 0
        
        opponent = -self.player
        for move in possible_moves:
            x, y = move
            game.board[x, y] = opponent
            if game.check_winner() == opponent:
                game.board[x, y] = 0
                return move
            game.board[x, y] = 0 
        
        if (1, 1) in possible_moves:
            return (1, 1)
        
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for corner in corners:
            if corner in possible_moves:
                return corner
        
        return random.choice(possible_moves)

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.game = TicTacToe()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.agent = SimpleAgent(player=-1)

        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(master, text='', font=('normal', 40), width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if self.game.make_move(row, col, 1):
            self.buttons[row][col].config(text='X')
            self.check_game_over()
            if self.game.check_winner() is None:
                self.agent_move()

    def agent_move(self):
        move = self.agent.get_move(self.game)
        self.game.make_move(move[0], move[1], -1)
        self.buttons[move[0]][move[1]].config(text='O')
        self.check_game_over()

    def check_game_over(self):
        winner = self.game.check_winner()
        if winner is not None:
            if winner == 1:
                messagebox.showinfo("Game Over", "You win!")
            elif winner == -1:
                messagebox.showinfo("Game Over", "You lose!")
            else:
                messagebox.showinfo("Game Over", "It's a draw!")
            self.master.quit()

def main():
    root = tk.Tk()
    root.title("Tic-Tac-Toe")
    TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()