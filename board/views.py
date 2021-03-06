from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

from .models import *
from control.models import *
from django.db.models import Count

from django.core.paginator import Paginator

# 첫 화면
def home(request):
    # 최근 포스트
    recent_posts = Post.objects.order_by('-created_at')[:6]

    # 많이 보일 게시판의 글
    main_posts = Post.objects.annotate(
        reply_count = Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count = Count('likes', distinct=True),
    ).order_by('-like_count', '-reply_count')[:6]

    all_tags = Tag.objects.all()

    all_announce = Announce.objects.order_by('-created_at')[:5]

    context = {
        'recent_posts': recent_posts,
        'main_posts': main_posts,
        'all_tags': all_tags,
        'all_announce': all_announce,
    }

    return render(request, 'board/home.html', context)

# 게시글 목록 (게시판)
def board(request, board_url):

    board = get_object_or_404(Board, url=board_url)
    posts = board.post_set.annotate(
        reply_count = Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count = Count('likes', distinct=True),
    ).order_by('-created_at')

    #페이지네이션 만들기
    posts = Paginator(posts, 10)

    page = request.GET.get('page')

    #페이지 보이게 하는 숫자 구간
    page_numbers_range = 5

    #최대 녀석이 있을 경우 최대 까지만 보이도록 하기 위해서!
    max_index = len(posts.page_range)

    #페이지가 0일 경우 1로 변경 current_page에 넣기
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = posts.page_range[start_index:end_index]

    posts = posts.get_page(page) #페이지네이션 만들기

    context = {
        "page_range":page_range,
        'board':board,
        'posts':posts,
    }

    return render(request, 'board/board.html', context)

# 자세한 글 보기
def post_detail(request, board_url, pk):
    qs = Post.objects.filter(board_id__url=board_url).annotate(
        reply_count = Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count = Count('likes', distinct=True),
    ).order_by('-created_at')

    post = get_object_or_404(qs, board_id__url=board_url, pk=pk)

    if request.user.is_authenticated:
        like_check = Like.objects.filter(author=request.user, post_id=post).exists()
    else:
        like_check = False

    context = {
        'like_check':like_check,
        'qs':qs,
        'post':post,
    }

    return render(request, 'board/post.html', context)

# 댓글 작성
def reply_write(request, board_url, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, board_id__url=board_url, pk=pk)
        if request.POST.get('reply_body'):
            Reply.objects.create(post_id=post, author=request.user, body=request.POST.get('reply_body'))

    return HttpResponseRedirect(reverse('board:post', args=[board_url, pk]))

# 답글 작성
def rereply_write(request, board_url, pk):
    reply = get_object_or_404(Reply, id=pk)
    if request.method == 'POST' and request.user.is_authenticated and request.POST.get('rereply'):
        rereply = Rereply()
        rereply.reply_id = reply
        rereply.author = request.user
        rereply.body = request.POST.get('rereply')
        rereply.save()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, reply.post_id.id]))

# 댓글 삭제
def reply_delete(request, board_url, pk):
    if request.user.is_authenticated:
        reply = get_object_or_404(Reply, id=pk)
        post_id = reply.post_id.id
        if reply.author == request.user or request.user.is_superuser:
            reply.delete()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, post_id]))

# 답글 삭제
def rereply_delete(request, board_url, pk):
    if request.user.is_authenticated:
        rereply = get_object_or_404(Rereply, id=pk)
        post_id = rereply.post_id.id
        if rereply.author == request.user or request.user.is_superuser:
            rereply.delete()
    return HttpResponseRedirect(reverse('board:post', args=[board_url, post_id]))

# 좋아요 추가 삭제
def like(request, board_url, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user.is_authenticated:
        qs = Like.objects.filter(author=request.user, post_id=post)
        if qs.exists():
            qs.delete()
        else:
            Like.objects.create(author=request.user, post_id=post)
    return HttpResponseRedirect(reverse('board:post', args=[board_url, pk]))

def tag_board(request, tag_name):
    tag_board = get_object_or_404(Tag, tag_name=tag_name)
    posts = tag_board.post_set.annotate(
        reply_count = Count('replys', distinct=True) + Count('rereply', distinct=True),
        like_count = Count('likes', distinct=True),
    ).order_by('-created_at')

    #페이지네이션 만들기
    posts = Paginator(posts, 10)

    page = request.GET.get('page')

    #페이지 보이게 하는 숫자 구간
    page_numbers_range = 5

    #최대 녀석이 있을 경우 최대 까지만 보이도록 하기 위해서!
    max_index = len(posts.page_range)

    #페이지가 0일 경우 1로 변경 current_page에 넣기
    current_page = int(page) if page else 1
    start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range

    if end_index >= max_index:
        end_index = max_index

    page_range = posts.page_range[start_index:end_index]

    posts = posts.get_page(page) #페이지네이션 만들기

    context = {
        "page_range":page_range,
        'tag_board':tag_board,
        'posts':posts,
    }
    return render(request, 'board/board.html', context)
