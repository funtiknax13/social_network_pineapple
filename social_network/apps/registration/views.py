from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
#import django.contrib.auth


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('account:user_account'))
    else:
        return render(request, 'registration/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            form.add_error('email', "Пользователь с таким E-MAIL уже зарегестрирован!")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        if form.is_valid():
            ins = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password, email=email)
            user.profile.avatar = 'images/avatar/standart.jpg'
            ins.email = email
            ins.first_name = first_name
            ins.last_name = last_name
            ins.save()
            form.save_m2m()
            messages.success(request, 'Вы успешно зарегестрировались!')
            login(request, user)
            return redirect('/')
    else:
        form = UserRegisterForm()

    context = {'form':form}
    return render(request, 'registration/reg.html', context)
