from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect, HttpResponseRedirect
from django.utils import timezone
from django.views.generic import ListView
from rides.models import CustomUser, Vehicle, Trip, Region, Message, Hitch_Request, Location
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rides.forms import UserForm, VehicleForm, TripForm, RegionFilterForm, MessageForm, LocationForm
from datetime import date
from itertools import chain
from operator import attrgetter

# -------------------------------------------------------
def rides_view(request):
    
    if request.method == "POST":
        
        # check if posting for hitch or for a ride
        if 'ride_trip_id' in request.POST:
            #user clicked a hitch ride button for specific ride
            trip_id = request.POST.get('ride_trip_id')
            trip = Trip.objects.get(id=trip_id)
            message_content = request.POST.get('message')
            hitcher = request.user
            driver = trip.driver
            
            # create message instance and store in message DB
            message = Message(sender=hitcher, receiver=driver, message=message_content, trip_id=trip_id)
            message.save()
            
            # create hitchrequest and store in message DB
            hitch_request = Hitch_Request(
                trip=trip,
                hitcher=hitcher,
                region=trip.region,
                depart=trip.depart,
                destination=trip.destination,
                depart_date=trip.depart_date,
                depart_time=trip.depart_time,
                is_public = False
                )

            hitch_request.save()
            messages.success(request, 'Hitch Request successfully submitted! The Driver will get back to you')
            
        else:    
            # driver wants to create a new trip
            form = TripForm(request.POST)
            form.instance.driver = request.user
            region_form = RegionFilterForm(request.GET)
            selected_region = Region.objects.first()

            if region_form.is_valid():
                selected_region = region_form.cleaned_data.get('region')
               
            if form.is_valid():
                new_trip = form.save(commit=False)
                new_trip.driver = request.user
                new_trip.region = selected_region
                new_trip.save()

                messages.success(request, 'New trip created successfully! Thanks for sharing!')
            else:
                error_messages = form.errors.as_data()
                print(form.errors)
                messages.error(request, 'Sorry, something went wrong')
            
        return HttpResponseRedirect(request.path_info) 

    else:
        user = request.user
        form = TripForm(user=user)
        region_filter_form = RegionFilterForm(request.GET or None)
        message_form = MessageForm()
        
        # Set Default for Vehicles:
        vehicles = Vehicle.objects.filter(owner=user)
        default_vehicle = None
        if vehicles.exists():
            default_vehicle = vehicles.first().id

        #now build form
        form = TripForm(user=user, initial={'vehicle': default_vehicle})

        # Filter trips by selected region and departure_date
        trips = Trip.objects.filter(depart_date__gte=timezone.now().date()).order_by("depart_date")
        region = Region.objects.first()
        

        # Create a list of forms for each trip instance
        forms = [TripForm(instance=trip) for trip in trips]


        # also remember the avaialble hitch seats per trip
        average_driver_ratings = []
        hitch_seats_list = []
        hitch_groups = []
        # minimum value in case no trip in loop
        hitch_seats = 1

        for trip in trips:
            driver = trip.driver
            average_driver_ratings.append(round(trip.driver.average_driver_rating))
            
            # get the driver allowed hitch seats from trip model
            hitch_seats = trip.max_hitch
            hitch_seats_list.append(hitch_seats)

            # get any attached hitchers to this trip
            approved_hitch_requests = Hitch_Request.objects.filter(trip=trip, pax_approved=True)
            hitchers = [hr.hitcher.username for hr in approved_hitch_requests]
            remaining_hitch_seats = hitch_seats - len(hitchers)
            hitch_group = hitchers + ['----' for _ in range(remaining_hitch_seats)]
            hitch_groups.append(hitch_group)

        #only allow vehicles and locations of the logged in user
        has_vehicles = Vehicle.objects.filter(owner=request.user).exists()
        has_locations = Location.objects.filter(input_by=request.user).exists()

        context = {
            "username": request.user,
            "form": form,
            'region': region,
            "region_filter_form": region_filter_form,
            "message_form": message_form,
            "trips": zip(trips, forms, average_driver_ratings, hitch_groups),
            "has_vehicles": has_vehicles,
            "has_locations": has_locations,
            "default_vehicle": default_vehicle,
        }

        return render(request, 'rides/rides.html', context)



# -------------------------------------------------------
def hitches(request):
    form = TripForm()
    region_filter_form = RegionFilterForm(request.GET or None)


    # Filter trips by selected region and departure_date
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

    def calculate_rating(rating):
        if rating is None:
            return 0  
        return int(round(rating))

    for trip in trips:
        driver = trip.driver
        driver_ratings = calculate_rating(trip.driver.average_driver_rating)
        
        average_ratings.append(driver_ratings)

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
    region_filter_form = RegionFilterForm(request.GET or None)
    user_id = request.user.id
    
    trips = Trip.objects.filter(driver=user_id)
    hitches = Hitch_Request.objects.filter(hitcher=user_id)
    vehicles = Vehicle.objects.filter(owner=request.user)
    
    if region_filter_form.is_valid():
        selected_region = region_filter_form.cleaned_data['selected_region']
        trips = trips.filter(region=selected_region)
        hitches = hitches.filter(region=selected_region)

    combined_list = list(chain(hitches, trips))
    

    # Add an is_ride attribute to each instance
    for instance in combined_list:
        instance.is_ride = isinstance(instance, Trip)

    sorted_list = sorted(combined_list, key=attrgetter('depart_date')) 



    for instance in sorted_list:
        # Check if the instance is a Trip
        if isinstance(instance, Trip):
            instance_type = 'Ride'
        else:
            instance_type = 'Hitch'# Print the details
        print(f"ID: {instance.id}, Type: {instance_type}, Departs: {instance.depart.name}")


       
    detailed_sorted_list = []
    
    
    if request.method == "POST":
        print('......PROCESSING POST .....')
        # get trip or hitch ID from button value
        pk = request.POST.get('edit') or request.POST.get('delete')
        instance = next((item for item in combined_list if item.id == int(pk)), None)
        
        if instance is not None:
            if instance.is_ride:
                type = 'ride'
            else:
                type = 'hitch'
         
        
        if 'edit' in request.POST:
            print(f'you want to edit {type}: {pk}')
            
            # form = TripForm(request.POST)
            # form.instance.owner = request.user
            # if form.is_valid():
            #     form.save()
            #     messages.success(request, 'Trip updated successfully!')

            return redirect('user_trips') 

        elif 'delete' in request.POST:
            print(f'you want to delete {type}: {pk}')

            # in here need to differentiate between trip and hitch... tbd...
            # pk = request.POST.get('delete')
            # trip = Trip.objects.get(id=pk)
            # trip.delete()
            # messages.success(request, 'Trip deleted sucessfully!')

            return redirect('user_trips') 


    else:
        print('......PROCESSING GET .....')

        def calculate_rating(rating):
            if rating is None:
                return 0  
            return int(round(rating))

        for s in sorted_list:
            if isinstance(s, Trip):
                driver = s.driver
                rating = calculate_rating(s.driver.average_driver_rating)
                hitchers = [hr.hitcher for hr in s.hitch_requests.all()]
                hitchers_ratings_list = [(hr.hitcher, round(hr.hitcher.average_hitcher_rating)) for hr in s.hitch_requests.all()]
            elif isinstance(s, Hitch_Request):
                driver = s.trip.driver
                rating = calculate_rating(s.trip.driver.average_driver_rating)
                hitchers_ratings_list = []


            detailed_sorted_list.append((s, driver, rating, hitchers_ratings_list))

    context = {
        "username": request.user,
        "region_filter_form": region_filter_form,
        "trips": trips,
        "hitches": hitches,
        "detailed_sorted_list": detailed_sorted_list
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
    form = LocationForm()
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
            form = LocationForm(request.POST)
            
            form.instance.input_by = request.user
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Location added successfully!')
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            location = Location.objects.get(id=pk)
            location.delete()
            messages.success(request, 'Location deleted successfully!')
        elif 'update' in request.POST:
            pk = request.POST.get('update')
            
            location = Location.objects.get(id=pk)
            post_data = request.POST.copy()
            form = LocationForm(request.POST, instance=location)

            if form.is_valid():
                form.save()
                messages.success(request, 'Location updated successfully!')

        return redirect('locations')

    else:
        form = LocationForm()
        # favorite user locations
        if filter_value in ['True', 'False']:
            filter_value = filter_value == 'True'
            locations = Location.objects.filter(input_by=request.user).order_by('name')
        else:
            # Empty value = 'All'
            locations = Location.objects.filter(input_by=request.user).order_by('name')
            
        # Create a list of forms for each location instance
        forms = [LocationForm(instance=location) for location in locations]

        context = {
            "username": request.user,
            "form": form,
            "locations": zip(locations, forms),
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

