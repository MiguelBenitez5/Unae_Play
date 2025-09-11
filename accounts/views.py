from django.shortcuts import render
from globals.views import is_session_active
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser

# Create your views here.

def render_reg(request):
    if is_session_active(request):
        return redirect('homepage')
    
    if request.method == 'POST':
        if not request.POST.get('checkbox'):
            messages.error(request,'Debe aceptar los terminos y condiciones para registrarse')
            return redirect('register')
        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = CustomUser(username=username, email=email)
            user.set_password(password)
            try:
                user.full_clean()
                user.save()
                messages.success(request, f'Bienvenido {username}, ahora ingresa y empieza a jugar')
                return redirect("login")
            except Exception as e:
                messages.error(request, e.message_dict)



    return render(request, 'accounts/register.html')


def render_login(request):
    if is_session_active(request):
        return redirect('homepage')
    return render(request, 'login')
