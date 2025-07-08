from django.shortcuts import render
from .forms import UserForm, ProfileForm

from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'basic_app/index.djhtml')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('basic_app:index'))


def special(request):
    return HttpResponse('You are logged in!')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)  # Hash password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()

            messages.success(request, 'Registration successful!')
            return render(request, 'basic_app/register.djhtml', {
                'user_form': UserForm(),
                'profile_form': ProfileForm(),
                'registered': True
            })
    else:
        user_form = UserForm()
        profile_form = ProfileForm()

    return render(request, 'basic_app/register.djhtml', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': False
    })


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('basic_app:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print('Someone try to login and failed.')
            print(f'Username: {username} and password: {password}')
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'basic_app/user_login.djhtml', {})
