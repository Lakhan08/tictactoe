# game/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Player, Game 

def home(request):
    players = Player.objects.all()  # Fetch all players from the database
    return render(request, 'game/home.html', {'players': players})

def new_game(request):
    if request.method == 'POST':
        player_x_name = request.POST.get('player_x_name')
        player_o_name = request.POST.get('player_o_name', '')

        if not player_x_name:
            return HttpResponseBadRequest("Player X is required.")

        # Find or create Player X
        player_x, created_x = Player.objects.get_or_create(name=player_x_name)

        # Find or create Player O, or set to None if AI is chosen
        if player_o_name:
            player_o, created_o = Player.objects.get_or_create(name=player_o_name)
        else:
            player_o = None  # AI

        # Create the game
        game = Game.objects.create(player_x=player_x, player_o=player_o)
        return redirect('game_detail', game_id=game.id)
    else:
        return redirect('home')

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    return render(request, 'game/game_detail.html', {'game': game})

def check_winner(board, player):
    """Check if the given player has won the game."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)



def make_move(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        position = int(request.POST.get('position'))

        # Ensure the move is valid and the game is still active
        if game.is_active and game.board[position] == '-':
            board = list(game.board)
            board[position] = game.current_turn
            game.board = ''.join(board)

            # Check for a winner or a draw
            if check_winner(game.board, game.current_turn):
                game.winner = game.current_turn
                game.is_active = False
            elif '-' not in game.board:
                game.is_active = False  # It's a draw
            else:
                # Switch turns
                game.current_turn = 'O' if game.current_turn == 'X' else 'X'

            game.save()

        return redirect('game_detail', game_id=game.id)

def leaderboard(request):
    players = Player.objects.order_by('-wins')[:10]
    return render(request, 'game/leaderboard.html', {'players': players})
