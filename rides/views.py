from django.shortcuts import render, HttpResponse
from rides.models import CustomUser
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


def vehicles(request):
    form = VehicleForm()
    context = {
            "username": request.user,
            "form": form,
        }

    return render(request, 'rides/vehicles.html', context)
