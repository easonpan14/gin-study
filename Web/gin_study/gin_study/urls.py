from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('analysis/', views.analysis_view, name='analysis'),  # 修正這裡
    path('emo/', views.emo_view, name='emo'),
]
