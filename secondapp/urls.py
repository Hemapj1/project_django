from django.urls import path
from secondapp import views

urlpatterns = [
    path('home/',views.homepage,name='home'), 
    path('home/<int:problem_id>/', views.descriptionpage, name='description'),
    path('verdict/<int:problem_id>/', views.verdictpage, name='verdict'),
]



