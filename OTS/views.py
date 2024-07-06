from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from OTS.models import *
from .models import Quistion
import random

def Welcome(request):
    print("welcome page")
    template = loader.get_template('welcome.html')
    return HttpResponse(template.render())
def CandidateRegistrationForm(request):
    res = render(request,'registration_form.html')
    return res
    
def CandidateRegistration(request):
    if request.method=='POST':
        username = request.POST['username']
        #check if the use already exists
        if (len(Candidate.objects.filter(username = username))):
            userStatus = 1
        else:
            candidate = Candidate()
            candidate.username=username
            candidate.password=request.POST['password']
            candidate.name=request.POST['name']
            candidate.save()
            userStatus = 2
    else:
        userStatus=3
    context ={
            'userStatus':userStatus
        }
    return render(request,'registration.html',context)
        
            
    
def loginView(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        candidate = Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError = "Invalid username or password"
            res = render(request,'login.html',{"loginError":loginError})
        else:
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name
            res = HttpResponseRedirect('home')
    else:      
       res = render(request,'login.html')
    return res
            
    
def candidateHome(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    else:
        res = render(request,'home.html')
    return res
        
        
def testPaper(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
        
    n=int(request.GET['n'])   
    question_pool=list(Quistion.objects.all())
    random.shuffle(question_pool)
    question_list=question_pool[:n]
    context={"questions":question_list}
    res = render(request,'test_paper.html',context)
    return res
    
     
def calculateTestResult(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
    total_attemp = 0
    total_right = 0
    total_wrong = 0
    qid_list = []
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(int(request.POST[k]))
    for n in qid_list:
        question = Quistion.objects.get(qid=n)
        try:
            if question.ans == request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attemp+=1
        except:
            pass
    points=(total_right-total_wrong)/len(qid_list)*10
    #store result in result table
    result = Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt = total_attemp
    result.right = total_right
    result.wrong = total_wrong
    result.points = points
    result.save()
    
    #update candidate table
    candidate = Candidate.objects.get(username=request.session['username'])
    candidate.test_attempt+=1
    candidate.points=(candidate.points*(candidate.test_attempt-1)+points)/candidate.test_attempt
    candidate.save()
    return HttpResponseRedirect('result')
               
def testResultHistory(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
        
    candidate = Candidate.objects.filter(username = request.session['username'])
    results = Result.objects.filter(username_id=candidate[0].username)
    context = {"results":results,"candidate":candidate[0]}
    res = render(request,'candidate_history.html',context)
    return res
    
def showTestResult(request):
    if 'name' not in request.session.keys():
        res = HttpResponseRedirect('login')
        
    # fetch latest result from result table
    #result = Result.objects.filter(resultid=Result.objects.latest('result').result,username_id=request.session['username'])
    latest_result = Result.objects.latest('result')
    result = Result.objects.filter(result=latest_result.result, username_id=request.session['username'])
    context = {"result": result}
    res = render(request, 'show_result.html', context)
    return res
     
def logoutView(request):
    if 'name' in request.session.keys():
        del request.session['username']
        del request.session['name']
    return HttpResponseRedirect('login')
