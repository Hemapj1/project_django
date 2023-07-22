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

# def verdictpage(request, problem_id):
#     if request.method == 'POST':
       
#        return HttpResponse('hello')

import subprocess

def run_code(user_code, language, test_input):
    # The function to execute user's code and get the output
    if language == "cpp":
        compile_cmd = ["g++", "-x", "c++", "-o", "executable", "-"]
        execute_cmd = ["./executable"]
    elif language == "C":
        compile_cmd = ["gcc", "-x", "c", "-o", "executable", "-"]
        execute_cmd = ["./executable"]
    elif language == "Python3":
        compile_cmd = None  # Python doesn't need compilation
        execute_cmd = ["python3", "-"]
    elif language == "Python2":
        compile_cmd = None  # Python doesn't need compilation
        execute_cmd = ["python2", "-"]
    elif language == "Java":
        compile_cmd = ["javac", "-", "-d", "."]
        execute_cmd = ["java", "Main"]

    if compile_cmd:
        compile_process = subprocess.run(compile_cmd, input=user_code.encode(), stderr=subprocess.PIPE)
        if compile_process.returncode != 0:
            return "Compilation Error", compile_process.stderr.decode("utf-8")

    execute_process = subprocess.run(execute_cmd, input=test_input.encode(), stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, timeout=5)
    if execute_process.returncode != 0:
        return "Runtime Error", execute_process.stderr.decode("utf-8")
    
    return "Accepted", execute_process.stdout.decode("utf-8")

def verdictpage(request, problem_id):
    if request.method == 'POST':
        problem = Problems.objects.get(id=problem_id)
        testcases = Testcases.objects.filter(problem_id=problem_id)

        
        
        
        user_code = request.POST.get('code')
        user_code = user_code.replace('\r\n', '\n').strip()

        language = request.POST['selected_language']
        submission = Submissions(user=request.user, problem=problem, submission_time=datetime.now(),
                                language=language, user_code=user_code)
        submission.save()

        verdict = "Wrong Answer"
        user_stdout = ""
        user_stderr = ""
        run_time = 0

        for testcase in testcases:
            test_input = testcase.input.replace('\r\n', '\n').strip()
            expected_output = testcase.output.replace('\r\n', '\n').strip()

            start_time = time()
            current_verdict, output = run_code(user_code, language, test_input)
            run_time = time() - start_time

            if current_verdict == "Compilation Error" or current_verdict == "Runtime Error":
                verdict = current_verdict
                user_stderr = output
                break

            user_stdout = output.strip()

            if user_stdout == expected_output:
                verdict = "Accepted"
            else:
                verdict = "Wrong Answer"
                break

        user = User.objects.get(username=request.user)
        if verdict == "Accepted":
            score = 0
            if problem.difficulty == "Easy":
                score = 10
                user.easy_solve_count += 1
            elif problem.difficulty == "Medium":
                score = 30
                user.medium_solve_count += 1
            else:
                score = 50
                user.tough_solve_count += 1

            user.total_score += score
            user.total_solve_count += 1
            user.save()

        submission.verdict = verdict
        submission.user_stdout = user_stdout
        submission.user_stderr = user_stderr
        submission.run_time = run_time
        submission.save()

        context = {'verdict': verdict}
        return render(request, 'verdictpage.html', context)
