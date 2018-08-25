from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import Trip
from ..exam_practice.models import User

def index(request):
    if 'logged_user' not in request.session:
        messages.error(request, 'You must be signed in!')
        return redirect('loginreg:index')

    me= User.objects.get(id=request.session['logged_user'])
    mytrips = Trip.objects.filter(planner=me) | Trip.objects.filter(joiner=me)
    other_trips= Trip.objects.exclude(id__in=mytrips)

    context = {
        'user' : me,
        'trips' : mytrips,
        'othertrips' : other_trips
        }


    return render(request,'trips/index.html',context)

def home(request):
    if 'logged_user' not in request.session:
        return redirect('loginreg:index')


    return redirect('trips:index')

def add(request):
    if 'logged_user' not in request.session:
        return redirect('loginreg:index')

    return render(request,'trips/add.html')

def entertrip(request):
    if 'logged_user' not in request.session:
        messages.error('You must be signed-in to enter information')
        return redirect('loginreg:index')

    if request.POST:
        errors = Trip.objects.tripvalidate(request.POST)
        if errors:
            for error in errors:
                messages.error(request,error)
            return redirect('trips:add')
        else:
            Trip.objects.create(new_destination=request.POST['new_destination'],new_description=request.POST['new_description'],trip_start=request.POST['trip_start'],trip_end=request.POST['trip_end'],planner=User.objects.get(id=request.session['logged_user']))


    return redirect('trips:index')

def join(request,id):
    if 'logged_user' not in request.session:
        messages.error(request, "You must be signed-in")
        return redirect('loginreg:index')

    me = User.objects.get(id=request.session['logged_user'])
    trip= Trip.objects.get(id=id)
    trip.joiner.add(me)
    trip.save()


    return redirect('trips:index')

def show(request,id):
    if 'logged_user' not in request.session:
        messages.error(request, "You must be signed-in")
        return redirect('loginreg:index')

    context = {
        'trip' : Trip.objects.get(id=id)
    }

    return render(request,'trips/show.html', context)
