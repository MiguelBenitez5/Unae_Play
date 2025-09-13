from django.shortcuts import render

#funciones en comun que se utilizan en varias aplicaciones

def is_session_active(request):
    if not request.session.get('access'):
        return False
    return True

def rennder_homepage(request):
    return render(request, 'base.html')


