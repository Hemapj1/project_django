from django.urls import path
from firstapp import views

urlpatterns = [
    path('',views.loginpage,name='login'), 
    path('register/', views.registerpage, name='register'),
]
