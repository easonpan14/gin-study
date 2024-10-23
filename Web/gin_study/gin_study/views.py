from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils.db import login_check, register_and_login

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = login_check(account, password)
        
        if user.uID != 0:
            # 登錄成功，傳遞 success 變量到前端
            return render(request, 'home.html', {'success': True})
        else:
            # 登錄失敗，傳遞 error 信息到前端
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = register_and_login(name, account, password)
        
        if user.uID != 0:
            # 註冊成功，重定向到登錄頁面
            return redirect('login')
        else:
            # 註冊失敗，重新渲染頁面並顯示錯誤信息
            return render(request, 'register.html', {'error': 'Registration failed'})
    
    return render(request, 'register.html')

def analysis_view(request):
    return render(request, 'analysis.html')

def emo_view(request):
    return render(request, 'emo.html')
