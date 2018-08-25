from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse



def index(request):

    return render(request,'exam_practice/index.html')

def register(request):
    if request.method == 'POST':
        form_errors = User.objects.validate(request.POST)

    if len(form_errors) > 0:
        for error in form_errors:
            messages.error(request,error)
    else:
        User.objects.register(request.POST)
        messages.success(request,'You have successfully registered')

    return redirect('loginreg:index')

def login(request):
    if request.method == 'POST':
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request,'Invalid Login Credentials')

        else:
            request.session['logged_user'] = user.id
            return redirect('trips:index')

    return redirect('loginreg:index')

# def travels(request):
#     if 'logged_user' not in request.session:
#         return redirect('/')
#
#
#
#     return render(request,'exam_practice/travels.html',context)

def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('loginreg:index')
