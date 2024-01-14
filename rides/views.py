from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect
from django.views.generic import ListView
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
    filter_value = request.GET.get('status')
    
    if request.method == "POST":
        if form.is_valid:
            if 'save' in request.POST:
                form = VehicleForm(request.POST)
                form.instance.owner = request.user
                form.save()
            elif 'delete' in request.POST:
                pk = request.POST.get('delete')
                print(f'pk: {pk}')
                vehicle = Vehicle.objects.get(id=pk)
                vehicle.delete()

            return redirect('vehicles')
    else:
        # vehicles owned by the user
        if filter_value in ['True', 'False']:
            filter_value = filter_value == 'True'
            vehicles = Vehicle.objects.filter(owner=request.user, status=filter_value)
        else:
            # Empty value = 'All'
            vehicles = Vehicle.objects.filter(owner=request.user)
        
        context = {
            "username": request.user,
            "form": form,
            "vehicles": vehicles,
        }

    return render(request, 'rides/vehicles.html', context)
