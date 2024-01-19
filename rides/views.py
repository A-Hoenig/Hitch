from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView
from rides.models import CustomUser, Vehicle, Trip, Region, Message, Hitch_Request
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rides.forms import UserForm, VehicleForm, TripForm, RegionFilterForm, MessageForm
from datetime import date
from itertools import chain
from operator import attrgetter

# -------------------------------------------------------
def rides_view(request):
    
    if request.method == "POST":
        # log ride request and message
        message_content = request.POST.get('message')
        trip_id = request.POST.get('ride_trip_id')
        
        trip = Trip.objects.get(id=trip_id)
        driver = trip.driver
        hitcher = request.user

        # create message insance and stor in message DB
        message = Message(sender=hitcher, receiver=driver, message=message_content, trip_id=trip_id)
        message.save()

        #create request instance and link to trip
        hitch_request = Hitch_Request(
            trip=trip,
            hitcher=hitcher,
            region=trip.region,
            depart=trip.depart,
            destination=trip.destination,
            depart_date=trip.trip_date,
            depart_time=trip.depart_time,
            )
        
        hitch_request.save()

        messages.success(request, 'Request successfully submitted! The Driver will get back to you')
        
        return HttpResponseRedirect(request.path_info) 

    else:
        form = TripForm()
        region_filter_form = RegionFilterForm(request.GET or None)
        message_form = MessageForm()

        # Filter trips by selected region and trip_date
        trips = Trip.objects.filter(depart_date__gte=timezone.now().date()).order_by("depart_date")

        if region_filter_form.is_valid():
            selected_region = region_filter_form.cleaned_data['selected_region']
            trips = trips.filter(region=selected_region)

        # Create a list of forms for each trip instance
        forms = [TripForm(instance=trip) for trip in trips]

        # Calculate the average rating for the driver for each trip
        # also remember the avaialble hitch seats per trip
        average_ratings = []
        hitch_seats_list = []
        hitch_groups = []
        # minimum value in case no trip in loop
        hitch_seats = 1

        for trip in trips:
            driver = trip.driver
            driver_ratings = driver.driver_rating_set.all()
            total_ratings = sum(rating.star_rating for rating in driver_ratings)
            num_ratings = len(driver_ratings)
            average_rating = round(total_ratings / num_ratings) if num_ratings > 0 else 0
            average_ratings.append(average_rating)

            # get the driver allowed hitch seats from trip model
            hitch_seats = trip.max_hitch
            hitch_seats_list.append(hitch_seats)

            # get any attached hitchers to this trip
            approved_hitch_requests = Hitch_Request.objects.filter(trip=trip, pax_approved=True)
            hitchers = [hr.hitcher.username for hr in approved_hitch_requests]
            remaining_hitch_seats = hitch_seats - len(hitchers)
            hitch_group = hitchers + ['----' for _ in range(remaining_hitch_seats)]
            hitch_groups.append(hitch_group)

        context = {
            "username": request.user,
            "form": form,
            "region_filter_form": region_filter_form,
            "message_form": message_form,
            "trips": zip(trips, forms, average_ratings, hitch_groups),
            "average_ratings": average_ratings,
            
        }

        return render(request, 'rides/rides.html', context)



# -------------------------------------------------------
def hitches(request):
    form = TripForm()
    region_filter_form = RegionFilterForm(request.GET or None)


    # Filter trips by selected region and trip_date
    trips = Trip.objects.filter(depart_date__gte=timezone.now().date()).order_by("depart_date")

    if region_filter_form.is_valid():
        selected_region = region_filter_form.cleaned_data['selected_region']
        trips = trips.filter(region=selected_region)

    # Create a list of forms for each trip instance
    forms = [TripForm(instance=trip) for trip in trips]

    # Calculate the average rating for the driver for each trip
    # also remember the avaialble hitch seats per trip
    average_ratings = []
    hitch_seats_list = []
    # minimum value in case no trip in loop
    hitch_seats = 1

    for trip in trips:
        driver = trip.driver
        driver_ratings = driver.driver_rating_set.all()
        total_ratings = sum(rating.star_rating for rating in driver_ratings)
        num_ratings = len(driver_ratings)
        average_rating = round(total_ratings / num_ratings) if num_ratings > 0 else 0
        average_ratings.append(average_rating)

        # get the driver allowed hitch seats from trip model
        hitch_seats = trip.max_hitch
        hitch_seats_list.append(hitch_seats)

    # get any attached hitchers to this trip
    

    context = {
        "username": request.user,
        "form": form,
        "trips": zip(trips, forms, average_ratings, hitch_seats_list),
        "region_filter_form": region_filter_form,
        "average_ratings": average_ratings,
        "hitcher_slots": range(hitch_seats),
    }

    return render(request, 'rides/hitches.html', context)



# -------------------------------------------------------
def about(request):
    context = {
        "username": request.user,

    }
    return render(request, 'rides/about.html', context)



# -------------------------------------------------------
@login_required
def user_trips(request):
    if request.method == "POST:":
        pass
    else:
        region_filter_form = RegionFilterForm(request.GET or None)
        user_id = request.user.id
        
        trips = Trip.objects.filter(driver=user_id)
        hitches = Hitch_Request.objects.filter(hitcher=user_id)
        

        if region_filter_form.is_valid():
            selected_region = region_filter_form.cleaned_data['selected_region']
            trips = trips.filter(region=selected_region)
            hitches = hitches.filter(region=selected_region)

        combined_list = list(chain(hitches, trips))

        # Add a is_ride attribute to each instance
        for instance in combined_list:
            instance.is_ride = isinstance(instance, Trip)

        sorted_list = sorted(combined_list, key=attrgetter('depart_date')) 
       

    context = {
        "username": request.user,
        "region_filter_form": region_filter_form,
        "trips": trips,
        "hitches": hitches,
        "sorted_list": sorted_list,
    }
    return render(request, 'rides/user_trips.html', context)



# -------------------------------------------------------
@login_required
def profile(request):
    
    # Check if the user has a Date of Birth set
    if request.user.DOB:
        today = date.today()
        born = request.user.DOB
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        age = None

    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Data updated sucessfully!')
            return redirect('user_profile')
    else:
        form = UserForm(instance=request.user)

    context = {
            "username": request.user,
            "form": form,
            "age": age,
    }
    return render(request, 'rides/user_profile.html', context)





# -------------------------------------------------------
@login_required
def locations(request):
    form = VehicleForm()
    filter_value = request.GET.get('status')
    # Check if the user has a Date of Birth set
    if request.user.DOB:
        today = date.today()
        born = request.user.DOB
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        age = None

    if request.method == "POST":
        if 'save' in request.POST:
            form = VehicleForm(request.POST)
            form.instance.owner = request.user
            if form.is_valid():
                form.save()
                messages.success(request, 'Vehicle added successfully!')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            vehicle = Vehicle.objects.get(id=pk)
            vehicle.delete()
            messages.success(request, 'Vehicle deleted sucessfully!')
        elif 'update' in request.POST:
            pk = request.POST.get('update')
            # print(f'....starting update for {pk}')
            vehicle = Vehicle.objects.get(id=pk)
            post_data = request.POST.copy()
            form = VehicleForm(request.POST, instance=vehicle)

            if form.is_valid():
                form.save()
                messages.success(request, 'Vehicle updated sucessfully!')

        return redirect('vehicles')

    else:
        form = VehicleForm()
        # vehicles owned by the user
        if filter_value in ['True', 'False']:
            filter_value = filter_value == 'True'
            vehicles = Vehicle.objects.filter(owner=request.user, status=filter_value).order_by('make')
        else:
            # Empty value = 'All'
            vehicles = Vehicle.objects.filter(owner=request.user).order_by('make')
            
        # Create a list of forms for each vehicle instance
        forms = [VehicleForm(instance=vehicle) for vehicle in vehicles]

        context = {
            "username": request.user,
            "form": form,
            "vehicles": zip(vehicles, forms),
            "age": age,
        }

    return render(request, 'rides/locations.html', context)



# -------------------------------------------------------
@login_required
def vehicles(request):
    form = VehicleForm()
    filter_value = request.GET.get('status')
    # Check if the user has a Date of Birth set
    if request.user.DOB:
        today = date.today()
        born = request.user.DOB
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    else:
        age = None

    if request.method == "POST":
        if 'save' in request.POST:
            form = VehicleForm(request.POST)
            form.instance.owner = request.user
            if form.is_valid():
                form.save()
                messages.success(request, 'Vehicle added successfully!')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            vehicle = Vehicle.objects.get(id=pk)
            vehicle.delete()
            messages.success(request, 'Vehicle deleted sucessfully!')
        elif 'update' in request.POST:
            pk = request.POST.get('update')
            # print(f'....starting update for {pk}')
            vehicle = Vehicle.objects.get(id=pk)
            post_data = request.POST.copy()
            form = VehicleForm(request.POST, instance=vehicle)

            if form.is_valid():
                form.save()
                messages.success(request, 'Vehicle updated sucessfully!')

        return redirect('vehicles')

    else:
        form = VehicleForm()
        # vehicles owned by the user
        if filter_value in ['True', 'False']:
            filter_value = filter_value == 'True'
            vehicles = Vehicle.objects.filter(owner=request.user, status=filter_value).order_by('make')
        else:
            # Empty value = 'All'
            vehicles = Vehicle.objects.filter(owner=request.user).order_by('make')
            
        # Create a list of forms for each vehicle instance
        forms = [VehicleForm(instance=vehicle) for vehicle in vehicles]

        context = {
            "username": request.user,
            "form": form,
            "vehicles": zip(vehicles, forms),
            "age": age,
        }

    return render(request, 'rides/vehicles.html', context)

