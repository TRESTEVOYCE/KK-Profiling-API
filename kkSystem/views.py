from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import EventForm, KKAddressForm, LoginForm, ProfilingInformationsForm ,YouthStatusForm, YouthStatus, MemberUpdateForm
from django.contrib.auth.decorators import login_required
from kkprofiling_api.models import ProfilingInformations,YouthStatus
from events_api.models import Event
from sk_members_api.models import Member
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.contrib import messages
from django.db.models import Count, Q

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page.
        else:
            form = LoginForm(request.POST)
            return render(request, 'login_page/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
        return render(request, 'login_page/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('loginn')


def home_view(request):
    # 1. Fetch exact matching summary counts from your database
    stats = ProfilingInformations.objects.aggregate(
        total=Count('id'),
        
        # Classification matching your model's YouthClassificationChoices internal database tags
        isy=Count('id', filter=Q(youth_statuses__youth_classification='in_school_youth')),
        osy=Count('id', filter=Q(youth_statuses__youth_classification='out_of_school_youth')),
        working=Count('id', filter=Q(youth_statuses__youth_classification='working_youth')),
        
        # Sex metrics matching your SexChoices
        male=Count('id', filter=Q(sex='male')),
        female=Count('id', filter=Q(sex='female')),
        
        # Target SK age groups
        age_15_18=Count('id', filter=Q(age__gte=15, age__lte=18)),
        age_19_24=Count('id', filter=Q(age__gte=19, age__lte=24)),
        age_25_30=Count('id', filter=Q(age__gte=25, age__lte=30)),
    )

    total_count = stats['total'] or 0

    # 2. Safely calculate percentages based on real database records
    student_pct = round((stats['isy'] / total_count * 100), 1) if total_count > 0 else 0
    working_pct = round((stats['working'] / total_count * 100), 1) if total_count > 0 else 0
    osy_pct = round((stats['osy'] / total_count * 100), 1) if total_count > 0 else 0

    # 3. Dynamically determine the true peak age bracket string from the query results
    age_map = {
        '15-18': stats['age_15_18'],
        '19-24': stats['age_19_24'],
        '25-30': stats['age_25_30']
    }
    
    # Safely select maximum bracket or fallback if database is empty
    peak_age_bracket = max(age_map, key=age_map.get) if total_count > 0 else "N/A"

    context = {
        'stats': stats,
        'student_pct': student_pct,
        'working_pct': working_pct,
        'osy_pct': osy_pct,
        'peak_age_bracket': peak_age_bracket,
    }
    
    return render(request, 'pages/home.html', context)


def search_youth_profiles(request):
    if not request.user.is_authenticated:
        return redirect('loginn')
    
    query = request.GET.get('q', '')
    results = ProfilingInformations.objects.filter(name__icontains=query)  # Simple search by name
    return render(request, 'pages/youth_profiles.html', {'results': results, 'query': query})

def filter_youth_profiles(request):
    if not request.user.is_authenticated:
        return redirect('loginn')

    query = request.GET.get('q', '')

    results = YouthStatus.objects.all()

    if query:
        results = results.filter(
            youth_classification__icontains=query
        )

    return render(request, 'pages/youth_profiles.html', {
        'results': results,
        'query': query
    })


def youth_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('loginn')
    profiles = ProfilingInformations.objects.select_related('addresses', 'youth_statuses').all()
    context = {
        'profiles': profiles,
    }
    
    return render(request, 'pages/youth_profiles.html', context)

def create_youth_profile_view(request):
    if request.method == 'POST':
        info_form = ProfilingInformationsForm(request.POST)
        address_form = KKAddressForm(request.POST)
        status_form = YouthStatusForm(request.POST)

        # Validate all forms concurrently before allowing persistence operations
        if info_form.is_valid() and address_form.is_valid() and status_form.is_valid():
            # 1. Save core information dataset
            profile_info = info_form.save()
            
            # 2. Bind relational models to the profile identity instance if required by architecture
            address = address_form.save(commit=False)
            address.save()
            status = status_form.save(commit=False)
            status.save()
            messages.success(request, "Youth registration profile successfully documented.")
            return redirect('youth-profiles')
    else:
        info_form = ProfilingInformationsForm()
        address_form = KKAddressForm()
        status_form = YouthStatusForm()

    context = {
        'info_form': info_form,
        'address_form': address_form,
        'status_form': status_form,
    }
    return render(request, 'pages/add_new_youth.html', context)

def events_view(request):
    if not request.user.is_authenticated:
        return redirect('loginn')
    
    # Fetch all events, ordering by newest added first
    all_events = Event.objects.all().order_by('-date_added')
    
    # Set up pagination: 6 items per page
    paginator = Paginator(all_events, 6) 
    page_number = request.GET.get('page')
    
    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        # If page variable is not an integer, default to the first page
        events = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        events = paginator.page(paginator.num_pages)

    context = {
        'events': events,  # This now contains only the sliced items for the current page
    }
    return render(request, 'pages/events.html', context)


def event_detail_view(request, event_id):
    if not request.user.is_authenticated:
        return redirect('loginn')
        
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'pages/view_events.html', {'event': event})

def add_event_view(request):
    if not request.user.is_authenticated:
        return redirect('loginn')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm()

    return render(request, 'pages/add_event.html', {'form': form})


def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('loginn')
    return render(request, 'pages/settings.html')

def organization_view(request):
    # Fetch all current council members from the database
    members_queryset = Member.objects.all()
    
    # Map them into a clean dictionary by position choice string for instant lookups
    # e.g., {'SK Chairperson': member_obj, 'SK Secretary': member_obj}
    council = {member.position: member for member in members_queryset}
    
    return render(request, 'pages/organizational.html', {'council': council})

def update_position_view(request, role):
    # Convert role identifiers from your URLs to match your model database choices
    role_mapping = {
        'chairperson': 'SK Chairperson',
        'secretary': 'SK Secretary',
        'treasurer': 'SK Treasurer',
        'kagawad-1': 'SK Councilor 1',
        'kagawad-2': 'SK Councilor 2',
        'kagawad-3': 'SK Councilor 3',
        'kagawad-4': 'SK Councilor 4',
        'kagawad-5': 'SK Councilor 5',
        'kagawad-6': 'SK Councilor 6',
        'kagawad-7': 'SK Councilor 7',
    }
    
    db_position = role_mapping.get(role, 'SK Chairperson')
    
    member = Member.objects.filter(position=db_position).first()
    
    if request.method == 'POST':
        form = MemberUpdateForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            # If it was an empty seat, assign the position text cleanly on save
            new_instance = form.save(commit=False)
            new_instance.position = db_position
            new_instance.save()
            return redirect('organization_chart_view_name')
    else:
        form = MemberUpdateForm(instance=member)
        
    return render(request, 'pages/update_member.html', {
        'form': form,
        'position_label': db_position,
        'member': member
    })

def edit_youth_profile_view(request, profile_id):
    profile = get_object_or_404(ProfilingInformations, id=profile_id)
    address = getattr(profile, 'addresses', None)
    status = getattr(profile, 'youth_statuses', None)

    if request.method == 'POST':
        info_form = ProfilingInformationsForm(request.POST, instance=profile)
        address_form = KKAddressForm(request.POST, instance=address)
        status_form = YouthStatusForm(request.POST, instance=status)

        if info_form.is_valid() and address_form.is_valid() and status_form.is_valid():
            info_form.save()
            address_form.save()
            status_form.save()
            messages.success(request, "Youth profile successfully updated.")
            return redirect('youth-profile')
    else:
        info_form = ProfilingInformationsForm(instance=profile)
        address_form = KKAddressForm(instance=address)
        status_form = YouthStatusForm(instance=status)

    context = {
        'info_form': info_form,
        'address_form': address_form,
        'status_form': status_form,
        'profile': profile
    }
    return render(request, 'pages/add_new_youth.html', context)

def delete_youth_profile_view(request, profile_id):
    profile = get_object_or_404(ProfilingInformations, id=profile_id)

    if request.method == 'POST':
        profile.delete()
        messages.success(request, f"Profile for {profile.first_name} {profile.last_name} was successfully deleted.")
        return redirect('youth-profile')

    # IF A GET REQUEST HITS THIS URL, REDIRECT SAFELY INSTEAD OF CRASHING
    messages.warning(request, "Invalid request method for deleting a profile.")
    return redirect('youth-profile')

