from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def help(request):
    return render(request, 'help.html')


def signin(request):
    return render(request, 'signin.html')
