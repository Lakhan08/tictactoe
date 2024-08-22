# game/models.py
from django.db import models
import random

class Player(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Game(models.Model):
    player_x = models.ForeignKey(Player, related_name='player_x', on_delete=models.CASCADE)
    player_o = models.ForeignKey(Player, related_name='player_o', on_delete=models.CASCADE, null=True, blank=True)
    board = models.CharField(max_length=9, default="---------")  # 3x3 grid stored as a string
    current_turn = models.CharField(max_length=1, default="X")   # X or O
    is_active = models.BooleanField(default=True)
    winner = models.CharField(max_length=1, null=True, blank=True)

    def make_move(self, position):
        if self.is_active and self.board[position] == "-":
            board_list = list(self.board)
            board_list[position] = self.current_turn
            self.board = "".join(board_list)
            self.check_winner()
            self.current_turn = "O" if self.current_turn == "X" else "X"
            self.save()

            if self.current_turn == "O" and self.player_o is None:  # AI's turn
                self.make_ai_move()

    def make_ai_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == "-"]
        if available_moves:
            move = random.choice(available_moves)
            self.make_move(move)

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != "-":
                self.winner = self.board[combo[0]]
                self.is_active = False
                self.update_player_scores()
                break
        if "-" not in self.board and self.winner is None:
            self.is_active = False
            self.winner = "Draw"
            self.update_player_scores()

    def update_player_scores(self):
        if self.winner == "X":
            self.player_x.wins += 1
            if self.player_o:
                self.player_o.losses += 1
        elif self.winner == "O":
            if self.player_o:
                self.player_o.wins += 1
            self.player_x.losses += 1
        else:
            self.player_x.draws += 1
            if self.player_o:
                self.player_o.draws += 1
        self.player_x.save()
        if self.player_o:
            self.player_o.save()
