from django import forms
from django.forms.widgets import ClearableFileInput
from .models import *


class MyClearableFileInput(ClearableFileInput):
    initial_text = '현재 사진'
    input_text = '사진 바꾸기'
    clear_checkbox_label = '지우기'


class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'nickname', 'email', 'user_img',)
        labels = {
            'username': '',
            'password': '',
            'nickname': '',
            'user_img': '프로필사진(선택)',
            'email': ''
        }
        help_texts = {
            'username': '',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '아이디(2글자이상)',
                'style': 'text-align:center',
                'required': True,
                'minlength': 2,
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
                'style': 'text-align:center',
                'required': True,
                'minlength': 2,
            }),
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '닉네임(2글자이상)',
                'style': 'text-align:center',
                'required': True,
                'minlength': 2,
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '✉이메일',
                'style': 'text-align:center',
                'required': True,
            }),
            'user_img': forms.FileInput(attrs={
                'style': '',
                'class': 'form-control',
            })
        }
        error_messages = {
            'username': {
                'unique': "중복된 아이디가 존재합니다!",
            },
            'nickname': {
                'unique': "중복된 닉네임이 존재합니다!",
            },
        }
