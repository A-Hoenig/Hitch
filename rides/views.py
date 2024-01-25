from django.shortcuts import render, HttpResponse, get_object_or_404, reverse, redirect, HttpResponseRedirect
from django.utils import timezone
from datetime import timedelta, datetime
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from rides.models import CustomUser, Vehicle, Trip, Region, Message, Hitch_Request, Location
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from collections import defaultdict
from django.contrib.auth.decorators import login_required
from rides.forms import UserForm, VehicleForm, TripForm, RegionFilterForm, MessageForm, LocationForm
from datetime import date
from itertools import chain
from operator import attrgetter

# -------------------------------------------------------

def rides_view(request):
    #  ********************************************************************
    #  ************************ GENERAL SETUP  ****************************
    #  ********************************************************************

    # INITIALIZE MESSAGE FORM FOR HITCH REQUEST MODAL 
    message_form = MessageForm()
    
    # HANDLE REGION SETTING FOR ALL USERS
    region_filter_form = RegionFilterForm(request.GET or None)
    region = Region.objects.first()
    if region_filter_form.is_valid():
        selected_region = region_filter_form.cleaned_data.get('selected_region')
        if selected_region:
            region = selected_region

    # GET ALL APPLICABLE TRIPS AND FILTER
    trips = Trip.objects.filter(depart_date__gte=timezone.now().date(),
    region=region).order_by("depart_date")

    # INITIALIZE LISTS
    hitch_seats_list = []
    hitch_groups=[]
    pending_hitch_groups = []  # list of hitch request per ride
    hitch_seats = 1  # at least one hitcher seat avail

    # CREATE LIST OF HITCHERS FOR EACH TRIP AND TO TRIP INSTANCE
    for trip in trips:

        # get average driver rating from DB
        driver = trip.driver
        # attach to trip
        if driver is not None:
            trip.average_driver_rating = round(trip.driver.average_driver_rating)
        else:
            trip.average_driver_rating = 0

        # find any hitchers already approved by driver and create list - per trip
        approved_hitch_requests = Hitch_Request.objects.filter(trip=trip, pax_approved=True)
        approved_hitchers = [hr.hitcher for hr in approved_hitch_requests]
        trip.hitch_group = approved_hitchers
        trip.remaining_seats = trip.max_hitch - len(approved_hitchers)

        # get pending hitchrequests - not approved - per trip
        all_hitch_requests = Hitch_Request.objects.filter(trip=trip)
        pending_hitchers = [hr.hitcher for hr in all_hitch_requests if hr.hitcher not in approved_hitchers]
        trip.pending_hitchers = pending_hitchers
        
    #SET UP UNIVERSAL CONTEXT
    context = {
            "username": request.user,
            'region': region,
            'region_filter_form': region_filter_form,
            'message_form': message_form,
        }
        
    #  ********************************************************************
    #  ************************ HANDLE POST REQUESTS **********************
    #  ********************************************************************
     
    if request.method == "POST":
        print('*********************** POST REQUEST ******************')
    
        # User clicked hitch a ride.
        if 'ride_trip_id' in request.POST:
            trip_id = request.POST.get('ride_trip_id')
            trip = Trip.objects.get(id=trip_id)
            message = request.POST.get('message')
            hitcher = request.user
            driver = trip.driver
            
            # create message instance and store in message Model
            message = Message(sender=hitcher, receiver=driver, content=message, trip_id=trip_id)
            message.save()

            # create hitchrequest linked to trip and store in Hitch_Request Model
            print('building hitch request')
            hitch_request = Hitch_Request(
                trip=trip,
                hitcher=hitcher,
                region=trip.region,
                depart=trip.depart,
                destination=trip.destination,
                depart_date=trip.depart_date,
                depart_time=trip.depart_time,
                purpose=trip.purpose,
                smoking=trip.vehicle.smoking,
                is_public = False
                )
            hitch_request.save()
            messages.success(request, f'Hitch Request successfully submitted to {trip.driver}. The Driver will get back to you')
            
        else:
            # A DRIVER WANTS TO CREATE A NEW RIDE TO ADD TO THE LIST
            print('*** USER WANTS TO OFFER/CREATE A NEW RIDE ***')
            form = TripForm(request.POST, user=request.user)
            
            if form.is_valid():
                new_trip = form.save(commit=False)
                new_trip.driver = request.user 
                new_trip.save()
                messages.success(request, f'New trip to {new_trip.destination.city} created successfully! Thanks for sharing!')
                return HttpResponseRedirect(request.path_info)
            else:
                form = TripForm(initial=initial_data, user=request.user)
                #add POST specific context
                context['form'] = form 
                return render(request, 'rides.html', context)

        # print(f'post context : {context}')
        return HttpResponseRedirect(request.path_info, context) 

    
    else:
        #  ********************************************************************
        #  ************************ HANDLE GET REQUESTS ***********************
        #  ********************************************************************
        print('*********************** GET REQUEST *******************')
        
        if request.user.is_authenticated:
            form = TripForm(user=request.user)

        else:
            form = TripForm()

        context['trips']= trips
        context['form'] = form
      
        return render(request, 'rides/rides.html', context)

    

# -------------------------------------------------------
@login_required
def hitches(request):
    # no user authentication check as page only when logged in

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


def calculate_rating(rating):
        if rating is None:
            return 0  
        return int(round(rating))

# -------------------------------------------------------
def about(request):
    context = {
        "username": request.user,
    }
    return render(request, 'rides/about.html', context)

# -------------------------------------------------------
@login_required
def message_center(request):
    user_messages = Message.objects.filter(Q(sender=request.user)| Q(receiver=request.user)).order_by('trip__depart_date','date_created')
    
    # use dict to group Trips / add individual messages
    trips = defaultdict(list)
    for message in user_messages:
        trip_id = message.trip.id
        trips[trip_id].append(message)
    
    context = {
        'username': request.user,
        'trips': trips.values(),
    }
    return render(request, 'rides/message_center.html', context)



# -------------------------------------------------------
@login_required
def user_trips(request):
    # no user authentication check as page only when logged in
    user_id = request.user.id

    trips = Trip.objects.filter(driver=user_id)
    hitches = Hitch_Request.objects.filter(hitcher=user_id)
    vehicles = Vehicle.objects.filter(owner=request.user)
    
    region_filter_form = RegionFilterForm(request.GET or None)
    if region_filter_form.is_valid():
        selected_region = region_filter_form.cleaned_data['selected_region']
        trips = trips.filter(region=selected_region)
        hitches = hitches.filter(region=selected_region)

    combined_list = list(chain(hitches, trips))

    # Add an is_ride attribute to each instance
    for instance in combined_list:
        instance.is_ride = isinstance(instance, Trip)

    sorted_list = sorted(combined_list, key=attrgetter('depart_date'))
    detailed_sorted_list = []  

    if request.method == "POST":
        print('********************PROCESSING POST******************')

        if 'edit' in request.POST:
            print('you are in edit')
            pk = request.POST.get('edit')
            print(pk)
            # get trip type from button trip-type attribute
            trip_type = request.POST.get(f'tripTypeName_{pk}')
            
            if trip_type == 'True':

                print(f'you want to edit ride {pk}')

            else:
                
                print(f'you want to edit hitch {pk}')

            return redirect('user_trips') 

        elif 'delete' in request.POST:
            print('you are in delete')
            pk = request.POST.get('delete')
            print(pk)
            trip_type = request.POST.get(f'tripTypeName_{pk}')
            print(f'you want to delete {trip_type}: {pk}')
            
            if trip_type == 'True':
                #true = ride
                trip = Trip.objects.get(id=pk)
                # trip.delete()
                print(f'**********This would delete RIDE {pk}')
                messages.success(request, 'Sorry not implemented yet for trips')

                return redirect('user_trips') 

            elif trip_type == 'False':
                #hitch
                hitch = Hitch_Request.objects.get(id=pk)
                print(f'***********This would delete HITCH {pk}')
                messages.success(request, 'Your Hitch request was deleted successfully!')
                
                # send notification to Driver
                
                # **** NEED TO GET TRIP OBJECT FOR MESSAGE_SENDER
                message_text = "This hitcher cancelled his request"
                # message = Message(sender=user_id, receiver=hitch.hitcher, message=message_text)
                
                hitch.delete()
                # message.save()

                return redirect('user_trips') 

        elif 'confirm' in request.POST:
                # confirm only for hitches
                print('you are in confirm')
                tripPk=request.POST.get('confirm').split('_')
                # pks = request.POST.get(f'hitcherNameID_{tripPk}')
                pk_trip = tripPk[0]
                pk_hitcher = tripPk[1]
                trip = Trip.objects.get(id=pk_trip)
                hitch = Hitch_Request.objects.get(trip=pk_trip, hitcher=pk_hitcher)

                print(f'You want to link hitch{hitch.id} to trip{trip.id}')
                
                hitch.pax_approved = True
                hitch.save()
                message_content = f'Hello {hitch.hitcher.first_name}! {trip.driver} just approved your HitchRequest!'
                message = Message(trip=trip, sender=trip.driver, receiver=hitch.hitcher, content=message_content)
                message.save()
                messages.success(request, f'You approved {hitch.hitcher}. An automated message was sent to let {hitch.hitcher} know.')

                return redirect('user_trips')

        elif 'message' in request.POST:
            # hitcher to driver
                print('you are in message')
                # get trip PK and hitcherPK from Form Button
                tripPk=request.POST.get('message_trip_id').split('_')
                pk_trip = tripPk[0]
                pk_hitcher = tripPk[1]
                trip = Trip.objects.get(id=pk_trip)
                hitch = Hitch_Request.objects.get(trip=pk_trip, hitcher=pk_hitcher)
                
                message_form = MessageForm(request.POST)
                if message_form.is_valid():
                    message_content = message_form.cleaned_data['message']
                    message = Message(trip=trip, sender=trip.driver, receiver=hitch.hitcher, content=message_content)
                    message.save()
                    messages.success(request, 'Your message was sent!')

                return redirect('user_trips') 
        
    else:
        print('......PROCESSING GET .....')
        message_form = MessageForm()

        def calculate_rating(rating):
            if rating is None:
                return 0  
            return int(round(rating))

        for s in sorted_list:
            hitchers_ratings_list = []  # remove if it goes bad
                        
            if isinstance(s, Trip):
                driver = s.driver
                rating = calculate_rating(s.driver.average_driver_rating)

                # hitchers = [hr.hitcher for hr in s.hitch_requests.all()]
                all_hitch_requests = s.hitch_requests.all() # remove if it goes bad
                # hitchers_ratings_list = [(hr.hitcher, round(hr.hitcher.average_hitcher_rating)) for hr in s.hitch_requests.all()]
                
                for hr in all_hitch_requests:
                    hitcher = hr.hitcher
                    hitcher.is_approved = hr.pax_approved
                    hitchers_ratings_list.append((hitcher, round(hitcher.average_hitcher_rating)))  #delete if bad
                    

            # elif isinstance(s, Hitch_Request):
            #     driver = s.trip.driver
            #     rating = calculate_rating(s.trip.driver.average_driver_rating)
            #     hitchers_ratings_list = []
            elif isinstance(s, Hitch_Request):  # remove if it goes bad
                driver = s.trip.driver  # remove if it goes bad
                rating = calculate_rating(s.trip.driver.average_driver_rating)  # remove if it goes bad
                hitchers_ratings_list = []  # remove if it goes bad
                

            # detailed_sorted_list.append((s, driver, rating, hitchers_ratings_list))
            detailed_sorted_list.append((s, driver, rating, hitchers_ratings_list))  # remove if it goes bad

    context = {
        "username": request.user,
        "region_filter_form": region_filter_form,
        "message_form": message_form,
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
            print(f'**************** pk is {pk}*****************')
            location = Location.objects.get(id=pk)
            print(location)
            location.delete()
            # messages.success(request, 'Location deleted successfully!')
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
