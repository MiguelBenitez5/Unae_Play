from django.shortcuts import render
from globals.utils import is_session_active
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate

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
            try:
                age = int(request.POST.get('age'))
            except TypeError:
                messages.error(request, 'La edad debe ser un numero entero valido')
                return render(request, 'accounts/register.html') 
            if age < 3 or age > 120:
                messages.error(request, 'Debes tener mas de 3 años y menos de 120 para ingresar al sitio web')
                return render(request, 'accounts/register.html') 
            user = CustomUser(username=username, email=email, age=age)
            user.set_password(password)
            try:
                user.full_clean()
                user.save()
                messages.success(request, f'Bienvenido {username}, ahora ingresa y empieza a jugar')
                return redirect("login")
            except Exception as e:
                for message in e.message_dict.values():
                    for error in message:
                        messages.error(request, error)

    return render(request, 'accounts/register.html')


def render_login(request):
    if is_session_active(request):
        return redirect('homepage')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)

        if user:
            #revisar
            user_id = user.id
            request.session['access'] = True
            request.session['user_id'] = user_id
            return redirect('homepage')
        else: 
            messages.error(request, 'Correo electronico o contraseña incorrecta')

    return render(request, 'accounts/login.html')

def logout(request):
    request.session.flush()
    return redirect('homepage')


