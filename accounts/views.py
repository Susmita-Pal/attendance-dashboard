from django.shortcuts import render, HttpResponse, redirect
from base import datahandler
from django.contrib import messages
from base import datahandler
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from accounts.models import UserAccount, AdminAccount
# import hashlib

#forget pwd
def forgotPassword(request):
    if request.method=='GET':
        return render(request,'resetPwd.html')
    else:
        email=request.POST['email']
        link=datahandler.reset_password(email)
        print(link)
        return render(request,'resetPwd.html',{'link':link})

#register
def userRegister(request):
    if request.method=='POST':
        empId=request.POST['empId']
        email=request.POST['email']
        fname=request.POST['fname']
        pwd=request.POST['pwd']
        cpwd=request.POST['cpwd']
        faceId=request.POST['faceId']
        school=request.POST['school']
        if pwd==cpwd:
            data={1:{'EmpId':empId,'email':email,'fullName':fname,'faceId':faceId,'school':school},2:{'pwd':pwd}}
            print(data)
            datahandler.setUserRegistration(data)
            return render(request,'userlogin.html')
        else:
            return render(request,'userRegister.html',{'comment':"The passwords don't match!!!"})

    else:
        return render(request,'userRegister.html')

#admin register
def adminRegister():
    pass
#Login
#def userLogin(request):
#    if request.method=='GET':
#        return render(request, 'userlogin.html')
#    else:
#        email=request.POST['email']
#        pwd=request.POST['password']
#        try:
#            #authenticate
#            datahandler.getUserDetails(email,pwd)

def userLogin(request):
    if request.method=='GET':
        return render(request,'userlogin.html')



def adminLogin(request):
    return render(request, 'adminlogin.html')


# Logout
def userLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('userLogin')
    else:
        return redirect('userLogin')


def adminLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('adminLogin')
    else:
        return redirect('adminLogin')
