from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
def login_view(request):
    return render(request, 'login.html')
def analysis_view(request):
    return render(request, 'analysis.html')
def emo_view(request):
    return render(request, 'emo.html')