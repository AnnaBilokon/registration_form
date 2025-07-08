from django.shortcuts import render
from .forms import UserForm, ProfileForm
from django.contrib import messages


def index(request):
    return render(request, 'basic_app/index.djhtml')


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
