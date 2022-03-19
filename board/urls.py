from django.urls import path
from .views import *

app_name = 'board'

urlpatterns = [
    path('', home, name='home'),
    path('<str:board_url>', board, name='board'),
    path('<str:board_url>/<int:pk>', post_detail, name='post'),
    path('<str:board_url>/<int:pk>/reply', reply_write, name='reply'),
    path('<str:board_url>/<int:pk>/rereply', rereply_write, name='rereply'),
    path('<str:board_url>/<int:pk>/reply_del', reply_delete, name='reply_delete'),
    path('<str:board_url>/<int:pk>/rereply_del', rereply_delete, name='rereply_delete'),
    path('<str:board_url>/<int:pk>/like', like, name='like'),
    path('board-group/<int:board_group_id>/constant', get_board_set_from_board_group, name='get_board_set_from_board_group'),
]