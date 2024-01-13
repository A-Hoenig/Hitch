from django.shortcuts import render, HttpResponse, get_object_or_404, reverse
from rides.models import CustomUser, Vehicle
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rides.forms import UserForm, VehicleForm

# Create your views here.
def rides(request):
    context = {
        "username": request.user
    }
    return render(request, 'rides/rides.html', context)


def hitches(request):
    context = {
        "username": request.user
    }
    return render(request, 'rides/hitches.html', context)


def about(request):
    context = {
        "username": request.user
    }
    return render(request, 'rides/about.html', context)

@login_required
def profile(request):
    form = UserForm()
    if request.method == "POST":
        if form.is_valid:
            form = UserForm(request.POST)
            form.save()
            return redirect('user_profile')
    else:
        form = UserForm()

    context = {
            "username": request.user,
            "form": form,
    }
    return render(request, 'rides/user_profile.html', context)

@login_required
def vehicles(request):
    form = VehicleForm()
    
    if request.method == "POST":
        if form.is_valid:
            form = VehicleForm(request.POST)
            form.save()
            return redirect('rides/vehicles.html')
    else:
        form = VehicleForm()
        vehicles = Vehicle.objects.filter(owner=request.user)
    context = {
            "username": request.user,
            "form": form,
            "vehicles": vehicles,
        }

    return render(request, 'rides/vehicles.html', context)
