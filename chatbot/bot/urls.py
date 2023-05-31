from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="bot-home"),
    path('bot-page/', views.botpage, name='bot-page'),
]
