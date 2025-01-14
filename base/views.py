from django.shortcuts import render, HttpResponse, redirect
from base import datahandler as data
from django.contrib import messages
from datetime import datetime

def userDashboard(request):
    context = {}
    userId = "5IrgYvcmWSG1VQlh3S1z"
    #userDetails = data.getUserDetails(userId)
    context['userDetails'] = userId

    if request.method == 'POST':
        fromDate = request.POST['fromDate']
        toDate = request.POST['toDate']
        newFromDate = datetime.strptime(fromDate, "%Y-%m-%d").date()
        newToDate = datetime.strptime(toDate, "%Y-%m-%d").date()

        attendanceDetails = data.getAttendance(userId, newFromDate, newToDate)
        if attendanceDetails is None:
            messages.error(request, "Some Error occured! Please try again.")
            return render(request, 'user.html')
        context['attendance'] = attendanceDetails['attendance']
        context['positivePercent'] = attendanceDetails['positivePercent']
        context['negativePercent'] = attendanceDetails['negativePercent']
        return render(request, 'user.html', context)

    attendanceDetails = data.getAttendance(userId)

    if attendanceDetails is None:
        messages.error(request, "Some Error occured! Please try again.")
        return render(request, 'user.html')
    context['attendance'] = attendanceDetails['attendance']
    context['positivePercent'] = attendanceDetails['positivePercent']
    context['negativePercent'] = attendanceDetails['negativePercent']
    return render(request, 'user.html', context)


def adminDashboard(request):
        return render(request, 'admin.html')

def land(request):
    return render(request,'index.html')
