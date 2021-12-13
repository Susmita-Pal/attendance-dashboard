import firebase_admin
from django.shortcuts import render, HttpResponse, redirect
from firebase_admin import credentials, firestore
from base import datahandler
from django.contrib import messages
from base import datahandler,views
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from accounts.models import UserAccount, AdminAccount
# import hashlib
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from datetime import datetime, timedelta
from firebase_admin import auth
import pyrebase

config = {
  "apiKey": "AIzaSyBexJb_2s5P3z96b75fU2jhZA8MQAMyuHQ",
  "authDomain": "mukhamapp.firebaseapp.com",
  "databaseURL": "https://mukhamapp-default-rtdb.firebaseio.com",
  "storageBucket": "mukhamapp.appspot.com"
}

firebase = pyrebase.initialize_app(config)


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
            return redirect('userLogin')
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
    else:
        email=request.POST['email']
        pwd=request.POST['password']
        #add in the authentication of the firestore
        if auth.sign_in_with_email_and_password(email,pwd):
            docs = datahandler.db.collection("Users").where('email', '==', email).stream()
            for doc in docs:
                uid=doc.id
                print(f'{doc.id}')
            ud=datahandler.getUserDetails(email)
            request.session['userEmail']=ud
            request.session['userId']=uid
            return redirect('dashboardUser')
            #return render(request, 'user.html', {'userDetails':ud,'uid':uid})
        else:
            return render(request,'userlogin.html',{'messages':'the email and password did not match'})


def dashboardUser(request):
    if request.method=='GET':
        if request.session.get('userEmail') is not None:
            return render(request, 'user.html',{'userDetails':request.session.get('userEmail'),'uid':request.session.get('userId')})
        else:
            return redirect('userLogin')
    else:
        fromDate=request.POST['fromDate']
        toDate=request.POST['toDate']
        p=datahandler.getPercentageAttendance(fromDate,toDate,request.session.get('userId'))
        print("Present days ",p['p'])
        print("Absent days ", p['a'])
        print("Total days ", p['total_days'])
        return render(request, 'user.html',{'attendance':p['attendance'],'userDetails':request.session.get('userEmail'),'uid':request.session.get('userId'),'positivePercent':p['p']*100/p['total_days'], 'negativePercent':p['a']*100/p['total_days']})

def dashboardAdmin(request):
    if request.method=='GET':
        if request.session.get('adminEmail') is not None:
            return render(request, 'admin2.html',{'adminDetails':request.session.get('adminEmail'),'uid':request.session.get('adminId')})
        else:
            return render(request,'adminlogin.html')
    else:
        fromDate=request.POST['fromDate']
        toDate=request.POST['toDate']
        attendance=datahandler.getDashboardAdmin(fromDate,toDate)
        return render(request, 'admin2.html',
                      {'attendance':attendance,'adminDetails': request.session.get('adminEmail'), 'uid': request.session.get('adminId')})

def adminLogin(request):
    if request.method=='GET':
        return render(request,'adminlogin.html')
    else:
        email = request.POST['email']
        pwd = request.POST['password']
        # add in the authentication of the firestore
        if email == pwd:
            docs = datahandler.db.collection("Users").where('email', '==', email).stream()
            for doc in docs:
                uid = doc.id
                print(f'{doc.id}')
            ud = datahandler.getUserDetails(email)
            request.session['adminEmail'] = ud
            request.session['adminId'] = uid
            return redirect('dashboardAdmin')
            # return render(request, 'user.html', {'userDetails':ud,'uid':uid})
        else:
            return render(request, 'adminlogin.html', {'messages': 'the email and password did not match'})

    datahandler.getDashboardAdmin()
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
