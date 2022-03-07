import json

from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest

from .forms import SignupForm
from .models import User


def login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        context = json.dumps({})

        if user is None:
            context = json.dumps({'error': '🚫 아이디 혹은 비밀번호 오류 🚫'})
            return HttpResponseBadRequest(context, 'application/json')

        auth.login(request, user)
        return HttpResponse(context, 'application/json')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def signup(request):
    if request.method == 'POST':
        sign_up_form = SignupForm(request.POST, request.FILES)

        if sign_up_form.is_valid():
            user = User.objects.create_user(
                username=sign_up_form.cleaned_data['username'],
                password=sign_up_form.cleaned_data['password'],
                nickname=sign_up_form.cleaned_data['nickname'],
                email=sign_up_form.cleaned_data['email'],
                user_img=sign_up_form.cleaned_data['user_img'],
            )
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')
        else:
            context = {
                'sign_up_form': sign_up_form,
            }
            return render(request, 'accounts/signup.html', context)
    else:
        sign_up_form = SignupForm()
        context = {
            'sign_up_form': sign_up_form,
        }
        return render(request, 'accounts/signup.html', context)
