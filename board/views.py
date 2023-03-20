import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse

from chatgpt.models import Lesson
from common_library import web_paging
from .models import *
from control.models import *
from django.db.models import Count, Q


def get_board_set_from_board_group(request, board_group_id):
    try:
        board_group = BoardGroup.objects.get(
            id=board_group_id
        )
    except BoardGroup.DoesNotExist:
        raise Http404

    board_set = board_group.board_set.all().values('name', 'url')

    return HttpResponse(json.dumps({'board_set': list(board_set)}), 'application/json')


def home(request):
    recent_post_set = Post.objects.active().order_by(
        '-id'
    )[:6]

    liked_ordered_post_set = Post.objects.active().annotate(
        reply_count=Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count=Count('likes', distinct=True),
    ).order_by(
        '-like_count',
        '-reply_count',
        '-id',
    )[:6]

    tag_set = Tag.objects.all()

    announce_set = Announce.objects.order_by(
        '-created_at'
    )[:5]

    lesson = Lesson.objects.last()

    context = {
        'recent_post_set': recent_post_set,
        'liked_ordered_post_set': liked_ordered_post_set,
        'tag_set': tag_set,
        'announce_set': announce_set,
        'lesson': lesson,
    }

    return render(request, 'board/home.html', context)


# 게시글 목록 (게시판)
def board(request, board_url):
    q = Q()

    board_obj = None
    tag_board = None

    # page:
    # 1 게시판 페이지
    # 2 태그 페이지
    # 3 검색 페이지
    page = 1

    search = request.GET.get('search')

    # 태그 페이지
    if board_url[0] == '_':
        page = 2
        tag_option = board_url[1:]

    # 검색 페이지
    if board_url == 'search':
        page = 3

    if search:
        tag_id_list = Tag.objects.filter(
            tag_name__icontains=search
        ).values_list(
            'id', flat=True
        )

        q = q & Q(title__icontains=search) | Q(body__icontains=search) | Q(tag_set__in=tag_id_list)

    # 게시판 선택
    if page == 1:
        board_obj = get_object_or_404(Board, url=board_url)
        posts = board_obj.post_set.filter(q).annotate(
            reply_count=Count('replys', distinct=True) + Count('rereply', distinct=True),
            like_count=Count('likes', distinct=True),
        ).order_by(
            '-created_at'
        )
    # 태그 검색
    elif page == 2:
        tag_board = get_object_or_404(Tag, tag_name=tag_option)
        posts = tag_board.post_set.filter(q).annotate(
            reply_count=Count('replys', distinct=True) + Count('rereply', distinct=True),
            like_count=Count('likes', distinct=True),
        ).order_by(
            '-created_at'
        )
    # 전체 검색
    elif page == 3:
        posts = Post.objects.active().filter(q).annotate(
            reply_count=Count('replys', distinct=True) + Count('rereply', distinct=True),
            like_count=Count('likes', distinct=True),
        ).order_by(
            '-created_at'
        )

    paging_obj = web_paging(request, posts, 10, 5)

    context = {
        'posts': paging_obj.get('page_posts'),
        'page_range': paging_obj.get('page_range'),
        'board': board_obj,
        'tag_board': tag_board,
    }

    return render(request, 'board/board.html', context)


# 자세한 글 보기
def post_detail(request, board_url, pk):
    qs = Post.objects.active().filter(
        board__url=board_url
    ).select_related(
        'board'
    ).order_by(
        '-id'
    )

    prev_post = qs.filter(id__lt=pk).first()
    next_post = qs.filter(id__gt=pk).order_by('id').first()

    qs = qs.annotate(
        reply_count=Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count=Count('likes', distinct=True),
    )

    post = get_object_or_404(qs, board__url=board_url, pk=pk)

    if request.user.is_authenticated:
        like_check = Like.objects.filter(author=request.user, post=post).exists()
    else:
        like_check = False

    context = {
        'like_check': like_check,
        'qs': qs,
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
    }

    return render(request, 'board/post.html', context)


# 댓글 작성
@login_required(login_url='/')
def reply_write(request, board_url, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, board__url=board_url, pk=pk)
        if request.POST.get('reply_body'):
            Reply.objects.create(post=post, author=request.user, body=request.POST.get('reply_body'))

    return HttpResponseRedirect(reverse('board:post', args=[board_url, pk]))


# 답글 작성
@login_required(login_url='/')
def rereply_write(request, board_url, pk):
    reply = get_object_or_404(Reply, id=pk)
    if request.method == 'POST' and request.POST.get('rereply'):
        rereply = Rereply()
        rereply.reply = reply
        rereply.author = request.user
        rereply.body = request.POST.get('rereply')
        rereply.save()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, reply.post.id]))


# 댓글 삭제
@login_required(login_url='/')
def reply_delete(request, board_url, pk):
    reply = get_object_or_404(Reply, id=pk)
    post_id = reply.post.id
    if reply.author == request.user or request.user.is_superuser:
        reply.delete()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, post_id]))


# 답글 삭제
@login_required(login_url='/')
def rereply_delete(request, board_url, pk):
    rereply = get_object_or_404(Rereply, id=pk)
    post_id = rereply.post.id
    if rereply.author == request.user or request.user.is_superuser:
        rereply.delete()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, post_id]))


# 좋아요 추가 삭제
@login_required(login_url='/')
def like(request, board_url, pk):
    post = get_object_or_404(Post, id=pk)
    qs = Like.objects.filter(author=request.user, post=post)
    if qs.exists():
        qs.delete()
    else:
        Like.objects.create(author=request.user, post=post)
    return HttpResponseRedirect(reverse('board:post', args=[board_url, pk]))
