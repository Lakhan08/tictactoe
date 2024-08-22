# game/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def make_rows(board):
    """Split the board string into rows for display."""
    return [board[i:i+3] for i in range(0, len(board), 3)]
