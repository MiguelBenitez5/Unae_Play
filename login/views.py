from django.shortcuts import render

# Create your views here.

def renderReg(request):
    return render(request, 'login/register.html')


def renderLogin(request):
    return render(request, 'login/login.html')
