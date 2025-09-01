from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def renderPage(request):
    return render(request, 'page.html')


def generateNumber(request):
    random_number = request.session.get('random_number')

    if not random_number:
        request.session['random_number'] = 105
        response = {'random_number': 105, 'title': 'Es la primera vez que se genera el numero'}
    else:
        response = {'random_number': random_number, 'title': 'Es el numero obtenido en la lectura de sesion'}

    return JsonResponse(response)

    

