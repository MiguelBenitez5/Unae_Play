from django.shortcuts import render

# Create your views here.

def is_session_active(request):
    if not request.session.get('access'):
        return False
    return True

def rennder_homepage(request):
    return render(request, 'base.html')


