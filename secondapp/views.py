from code import compile_command
import time
from urllib.parse import urlencode
from django.urls import reverse 
import datetime
import os
import subprocess
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from datetime import datetime
from mainproject import settings
from .models import Problems,Testcases
from django.contrib.auth.models import User
from firstapp.models import Submissions
def homepage(request):
    if request.method == 'GET':
        selected_problem_id = request.GET.get('problem')
        if selected_problem_id:
            return redirect('description', problem_id=selected_problem_id)
    
    problems = Problems.objects.all()
    context = {'problems': problems}
    return render(request, 'homepage.html', context)




def descriptionpage(request, problem_id):
    if request.method == 'POST':
        selected_language = request.POST.get('language')
        code = request.POST.get('code')
        userinput = request.POST.get('input')
        return redirect('verdict', problem_id=problem_id,selected_language=selected_language,code=code,userinput=userinput)
    
    problem = get_object_or_404(Problems, id=problem_id)
    context = {
        'ProblemName': problem.problemname,
        'Problemstatement': problem.problemstatement,
        'problem_id':problem.id,
    }
    return render(request, 'descriptionpage.html', context)

def verdictpage(request, problem_id):
    if request.method == 'POST':
       
       return HttpResponse('hello')


