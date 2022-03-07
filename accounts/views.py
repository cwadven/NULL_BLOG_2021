import json

from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SignupForm
from .models import User


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return HttpResponse(json.dumps({'works': True}), 'application/json')
        else:
            return HttpResponse(json.dumps({'works': False, 'error_message': '아이디 혹은 비밀번호 오류'}), 'application/json')


def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method == 'POST':
        signup = SignupForm(request.POST, request.FILES)
        if signup.is_valid():
            user = User.objects.create_user(
                username=signup.cleaned_data['username'],
                password=signup.cleaned_data['password'],
                nickname=signup.cleaned_data['nickname'],
                email=signup.cleaned_data['email'],
                user_img=signup.cleaned_data['user_img'],
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')
        else:
            context = {
                'signup': signup,
            }
            return render(request, 'accounts/signup.html', context)
    else:
        signup = SignupForm()
        context = {
            'signup': signup,
        }
        return render(request, 'accounts/signup.html', context)
