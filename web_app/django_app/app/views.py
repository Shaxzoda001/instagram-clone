from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, UserLoginForm
import requests


class HomePageVew(View):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return HttpResponseRedirect('login')
        headers = {
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.get('http://127.0.0.2:8008/auth/token/verify', headers=headers)

        if response.status_code == 200:
            return HttpResponse("You are logged in and can access this page")
        elif response.status_code == 401:
            response = HttpResponseRedirect('/login/')
            response.delete_cookie('access_token')
            return response
        else:
            return HttpResponse("Noma'lum xato yuz berdi", status=500)


class LoginPageVew(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8008/auth/login'
            data = {
                "username_or_email": form.cleaned_data['username_or_email'],
                "password": form.cleaned_data['password']
            }
            response = requests.post(url, json=data)
            if response.json()["status_code"] == 200:
                access_token = response.json()['access_token']
                response = redirect('home')
                response.set_cookie('access_toke', access_token, httponly=True)
                return response
            else:
                messages_error(request, "Invalid login")
        else:
            return render(request, 'login.html')


class RegisterPageVew(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            url = 'http://127.0.0.2:8008/auth/register'
            data = {
                "username": form.cleaned_data['username'],
                "email": form.cleaned_data['email'],
                "password": form.cleaned_data['password'],
            }
            response = requests.post(url, json=data)
            if response.json()["status_code"] == 201:
                return HttpResponse("User registered successfully!")
            else:
                return HttpResponse(f"Error: {response.json()['detail']}")
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})



