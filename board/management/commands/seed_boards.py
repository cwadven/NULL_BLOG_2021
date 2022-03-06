from django.core.management.base import BaseCommand
from django_seed import Seed
from board.models import *
from accounts.models import *
from control.models import *
import random

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--number", default=1)

    def handle(self, *args, **kwargs):
        number = kwargs.get("number")
        seeder = Seed.seeder()
        all_users = User.objects.all()
        all_boards = Board.objects.all()
        all_posts = Post.objects.all()
        all_replys = Reply.objects.all()
        # seeder.add_entity(Board, int(number), {
        #     'url' : lambda x: seeder.faker.domain_word(),
        #     'name' : lambda x: seeder.faker.domain_word(),
        #     'board_img':None,
        #     'attribute':0,
        # })
        # seeder.add_entity(Post, int(number), {
        #     'def_tag' : None,
        #     'post_img' : None,
        #     'board' : lambda x: random.choice(all_boards),
        #     'author' : lambda x: random.choice(all_users),
        # })
        # seeder.add_entity(Reply, int(number), {
        #     'post_id' : lambda x: random.choice(all_posts),
        #     'author' : lambda x: random.choice(all_users),
        # })
        seeder.add_entity(Rereply, int(number), {
            'post': lambda x: random.choice(all_posts),
            'reply': lambda x: random.choice(all_replys),
            'author': lambda x: random.choice(all_users),
        })
        # seeder.add_entity(Tag, int(number), {
        #     'tag_name' : lambda x: seeder.faker.user_name(),
        # })
        seeder.add_entity(Announce, int(number))
        seeder.execute()
