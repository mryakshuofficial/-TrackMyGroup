from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Users, Group, GroupMember, StudentLocation
from Notice.models import Notice
from django.http import JsonResponse
from django.utils.timezone import localtime

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')

        Users.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            password=password
        )

        return redirect('/')  # redirect to home after register

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = Users.objects.filter(email=email, password=password).first()

        if user:
            request.session['user_id'] = user.id   # create session
            request.session['user_name'] = user.name
            return redirect('/dashboard/')
        else:
            return HttpResponse("Invalid Email or Password")

    return render(request, 'login.html')


def dashboard(request):
    if 'user_id' in request.session:
        name = request.session.get('user_name')
        notices = Notice.objects.filter(is_active=True).order_by('-created_at')
        return render(request, 'dashboard.html', {'name': name, 'notices': notices})
    else:
        return redirect('/login/')
    
def logout(request):
    request.session.flush()
    return redirect('/login/')




def create_group(request):
    if 'user_id' not in request.session:
        return redirect('/login/')

    if request.method == "POST":
        group_name = request.POST.get('group_name')
        host_id = request.session.get('user_id')
        host_user = Users.objects.get(id=host_id)

        Group.objects.create(name=group_name, host=host_user)

        return HttpResponse(f"Group '{group_name}' created successfully!")

    return render(request, 'create_group.html')

def join_group(request):
    if 'user_id' not in request.session:
        return redirect('/login/')

    student_id = request.session.get('user_id')
    student = Users.objects.get(id=student_id)
    groups = Group.objects.all()  # existing groups

    if request.method == "POST":
        group_id = request.POST.get('group_id')
        location_permission = request.POST.get('location_permission') == 'on'

        group = Group.objects.get(id=group_id)

        # Check if already member
        exists = GroupMember.objects.filter(group=group, user=student).first()
        if not exists:
            GroupMember.objects.create(
                group=group,
                user=student,
                location_permission=location_permission
            )
        return HttpResponse(f"You joined group '{group.name}' successfully!")

    return render(request, 'join_group.html', {'groups': groups})

def group_map(request, group_id):
    if 'user_id' not in request.session:
        return redirect('/login/')

    group = Group.objects.get(id=group_id)
    # members = GroupMember.objects.filter(group=group, location_permission=True)
    members = StudentLocation.objects.filter(group=group)

    # Search functionality
    query = request.GET.get('q')
    if query:
        members = members.filter(
            user__name__icontains=query
        ) | members.filter(
            user__email__icontains=query
        ) | members.filter(
            user__mobile__icontains=query
        )

    # Get latest location for each member
    locations = []
    for m in members:
        loc = StudentLocation.objects.filter(user=m.user, group=group).last()
        if loc:
            locations.append(loc)

    # return render(request, 'group_map.html', {'group': group, 'locations': locations})
    return render(request, 'group_map.html', {'group': group, 'members': members})

def group_locations_api(request, group_id):
    group = Group.objects.get(id=group_id)
    members = StudentLocation.objects.filter(group=group)
    locations = []

    for m in members:
        locations.append({
            "name": m.user.name,
            "lat": float(m.latitude),
            "lng": float(m.longitude),
            "battery": m.battery_level,
            "updated": localtime(m.last_updated).strftime("%d-%m-%Y %I:%M %p")
        })

    return JsonResponse({"locations": locations})