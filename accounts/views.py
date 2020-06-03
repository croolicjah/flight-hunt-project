from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth


class SignUp(View):
    def get(self, request, *args, **kwargs):
        #  <view logic>

        return render(request, 'accounts/signup.html')

    def post(self, request, *args, **kwargs):
        if request.POST['password'] == request.POST['password-confirm']:
            try:
                user = User.objects.get(username=request.POST['user'])
                return render(request, 'accounts/signup.html', {'error': 'Użytkownik ' + str(user) + ' już istnieje!'})
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['user'])
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/signup.html', {'error': 'Nieudane potwierdzenie hasła!!!'})


class Login(View):
    def get(self, request):
        #  <view logic>

        return render(request, 'accounts/login.html')


    def post(self, request, *args, **kwargs):
        user = auth.authenticate(username=request.POST['user'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Login lub hasło są niepoprawne!!!'})


class Logout(View):
    def post(self, request, *args, **kwargs):
        auth.logout(request)
        return redirect('home')
