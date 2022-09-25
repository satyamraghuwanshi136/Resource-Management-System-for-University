

from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.decorators import permission_required, login_required

# Create your views here.


def loginAuth(request):

    if request.user.is_authenticated:
        return redirect(reverse('Administration:Dashboard'))

    if request.method == 'POST':

        Form = LoginForm(request.POST)

        if Form.is_valid():

            if User.objects.filter(username=Form.cleaned_data['Username']).count() > 0:

                if User.objects.filter(username=Form.cleaned_data['Username']).first().is_superuser == 1:
                    
                    user = authenticate(request, username=Form.cleaned_data['Username'], password=Form.cleaned_data['Password'])
                    if user is not None:
                        login(request, user)
                        return redirect(reverse('Administration:Dashboard'))
                    else:
                        return render(request, 'Authentication/Login.html', {'Form': Form, 'Message': 'Wrong credentials, try again.', 'Visiblity': 'visible'})
                else:
                    return render(request, 'Authentication/Login.html', {'Form': Form, 'Message': str(Form.cleaned_data['Username']) + ' is not allowed.', 'Visiblity': 'visible'})
            else:
                return render(request, 'Authentication/Login.html', {'Form': Form, 'Message': 'Username does not exist.', 'Visiblity': 'visible'})

    Form = LoginForm()

    return render(request, 'Authentication/Login.html', {'Form': Form, 'Message': '', 'Visiblity': 'invisible'})


def logoutAuth(request):

    logout(request)
    return redirect(reverse('Authentication:Login'))
