from .models import Board, BoardGroup


def nav_board(request):
    return {
        'nav_board': Board.objects.filter(board_group=None),
        'nav_group': BoardGroup.objects.order_by('-created_at')
    }
