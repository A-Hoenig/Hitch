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
        
        if 'save' in request.POST:
            form = VehicleForm(request.POST)
            form.instance.owner = request.user
            if form.is_valid():
                form.save()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            vehicle = Vehicle.objects.get(id=pk)
            vehicle.delete()
        elif 'update' in request.POST:
            print('....starting update')
            pk = request.POST.get('update')
            vehicle = Vehicle.objects.get(id=pk)
            post_data = request.POST.copy()

            if 'type' in post_data:
                # Exclude non-editable fields from cleaned_data during validation
                form = VehicleForm(post_data, instance=vehicle)
                form.fields['type'].required = False
                form.fields['engine'].required = False
                form.fields['max_pax'].required = False
            else:
                # For new entries, use the form without excluding fields
                form = VehicleForm(request.POST, instance=vehicle)
            
            print(form.is_valid())
            print(form.errors)
            
            if form.is_valid():
                print('form saving...')
                form.save()

        return redirect('vehicles')
    else:
        form = VehicleForm()
        # vehicles owned by the user
        if filter_value in ['True', 'False']:
            filter_value = filter_value == 'True'
            vehicles = Vehicle.objects.filter(owner=request.user, status=filter_value)
        else:
            # Empty value = 'All'
            vehicles = Vehicle.objects.filter(owner=request.user)
            
        # Create a list of forms for each vehicle instance
        forms = [VehicleForm(instance=vehicle) for vehicle in vehicles]

        context = {
            "username": request.user,
            "form": form,
            "vehicles": zip(vehicles, forms),
        }

    return render(request, 'rides/vehicles.html', context)

