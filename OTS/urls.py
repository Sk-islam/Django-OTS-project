from django.urls import path
from OTS.views import *
app_name = 'OTS'

urlpatterns = [
    path('',Welcome,name='welcome'),
    path('new-candidate',CandidateRegistrationForm,name='registrationForm'),
    path('store_candidate',CandidateRegistration,name='storecandidate'),
    path('login',loginView,name='login'),
    path('home',candidateHome,name='home'),
    path('test_paper',testPaper,name='testPaper'),
    path('calculate_result',calculateTestResult,name='calculateTest'),
    path('test_history',testResultHistory,name='testHistory'),
    path('result',showTestResult,name='result'),
    path('logout',logoutView,name='logout'),
    
]
