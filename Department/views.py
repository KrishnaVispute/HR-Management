from django.shortcuts import render,redirect,get_object_or_404
from Department.models import Department,Role,Users
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from random import randint

# Create your views here.
# Utility function to check if the user is admin
def is_admin(user):
    try:
        print(f"User role: {user.role.role_name}")  # Debugging log
        # print(request.session.items())  # This will print the session data
        return user.role.role_name == 'Admin'  # Ensure 'role_name' is correctly matching
    except AttributeError:
        # print(request.session.items())  # This will print the session data
        return False
    
def home(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    context={'is_authenticated': bool(user),
        'user': user,
        'role': user.role.role_name if user and user.role else 'No Role Assigned',
        }
    return render(request,'index.html',context)

# View departments (only active)
def viewDepart(request):
    data = Department.objects.filter(status=True)
    context = {}
    context['department']= data
    return render(request, 'viewdepartment.html', context)

def modifyDepart(request):
    # Only get active departments
    data = Department.objects.filter(status=True)
    context = {}
    context['department']= data
    return render(request, 'modifydepartment.html', context)

def createDepartment(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    if request.method == 'GET':
        return render(request,'createdepartment.html')
    else:
        n = request.POST['dept_name']
        d = request.POST['description']
        dept = Department.objects.create(dept_name=n, description =d)
        dept.save()
        return redirect('/modifydepartment')
    
def Deletedepartment(request, did):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    dept = Department.objects.get(dept_id = did)
    dept.status=False
    dept.save()
    return redirect('/modifydepartment')

def updateDepartment(request, did):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    d = Department.objects.get(dept_id=did)
    if request.method == 'GET':
        context = {'department': d}
        return render(request, 'updatedepartment.html', context)
    else:
        n = request.POST['dept_name']
        d.description = request.POST['description']
        d.depart_name = n
        d.save()
        return redirect('/modifydepartment')
    
# Roles

def viewRole(request):
    data=Role.objects.filter(status=True)
    context={}
    context['roles']=data
    return render(request,'viewrole.html',context)


def addRole(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    if request.method=='GET':
        return render(request,'addrole.html')
    else:
        #capture data from form
        n = request.POST['role_name']
        d = request.POST['description']
        r=Role.objects.create(role_name=n,description=d)
        return redirect('/viewrole')

def Deleterole(request, rid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')
    
    # Get the department object
    role = Role.objects.get(role_id=rid)
    # Update the status to False (inactive)
    role.status = False
    role.save()  # Save the updated status to the database
    return redirect('/viewrole')

def Updaterole(request,rid):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    r=Role.objects.get(role_id=rid) 
    if request.method=='GET':
        context={}
        context['role']=r # used with GET method
        return render(request,'updaterole.html',context)
    else:
        n = request.POST['role_name']
        r.description = request.POST['description']
        r.role_name = n
        r.save()
        return redirect('/viewrole')

#employee

def view_employees(request):
    employees = Users.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

def add_employee(request):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    if request.method == 'GET':
        roles = Role.objects.all()
        departments = Department.objects.filter(status=True)
        return render(request, 'addemployee.html', {
            'roles': roles,
            'departments': departments
        })
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        role_id = request.POST.get('role')
        department_id = request.POST.get('department')
        date_of_joining = request.POST['date_of_joining']
        username = request.POST['username']
        password = request.POST['password']

        role = Role.objects.get(role_id=role_id)
        department = Department.objects.get(dept_id=department_id)

        try:
            Users.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                role=role,
                department=department,
                date_of_joining=date_of_joining,
                username=username,
                password=make_password(password)
            )
            return redirect('/viewemployees')
        except IntegrityError:
            messages.error(request, f"Username '{username}' is already taken. Please choose another one.")
            return render(request, 'addemployee.html', {
                'roles': Role.objects.all(),
                'departments': Department.objects.filter(status=True),
                'username_error': True
            })



def update_employee(request, employee_id):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    employee = get_object_or_404(Users, id=employee_id)
    if request.method == 'POST':
        employee.first_name = request.POST['first_name']
        employee.last_name = request.POST['last_name']
        employee.email = request.POST['email']
        employee.mobile = request.POST['mobile']
        employee.role = Role.objects.get(role_id=request.POST['role'])
        employee.department = Department.objects.get(dept_id=request.POST['department'])
        employee.reporting_manager = Users.objects.get(id=request.POST['reporting_manager'])
        employee.date_of_joining = request.POST['date_of_joining']
        employee.save()
        return redirect('/viewemployees')
    else:
        roles = Role.objects.all()
        departments = Department.objects.filter(status=True)
        users = Users.objects.all()
        return render(request, 'update_delete_employee.html', {
            'employee': employee,
            'roles': roles,
            'departments': departments,
            'users': users
        })

def delete_employee(request, employee_id):
    user = Users.objects.get(username=request.user.username) if request.user.is_authenticated else None
    if not user or not is_admin(user):
        messages.error(request, 'You do not have permission to perform this action.')
        return redirect('/')

    employee = get_object_or_404(Users, id=employee_id)
    employee.delete()
    return redirect('/viewemployees')

# User Login:

# Dictionary to temporarily store OTPs
otp_storage = {}

def login_view(request):
    next_url = request.GET.get('next', '/')  # Retrieve next URL parameter if available
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = Users.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect(next_url)  # Redirect to original page
            else:
                messages.error(request, 'Invalid password.')
        except Users.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('/login/')


# Password reset request
def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = Users.objects.get(email=email)
            otp = randint(100000, 999999)
            otp_storage[email] = otp

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP is {otp}',
                'dcharlie919@gmail.com',  # Replace with your email
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your registered email.')
            return redirect('/validateotp/')
        except Users.DoesNotExist:
            messages.error(request, 'Email not registered.')
    return render(request, 'reset_password_request.html')

# OTP validation
def validate_otp(request):
    if request.method == 'POST':
        email = request.POST['email']
        entered_otp = request.POST['otp']
        if otp_storage.get(email) == int(entered_otp):
            return redirect(f'/resetpassword/?email={email}')
        else:
            messages.error(request, 'Invalid OTP.')
    return render(request, 'validate_otp.html')

# Reset password
def reset_password(request):
    email = request.GET.get('email')
    if request.method == 'POST':
        new_password = request.POST['password']
        user = Users.objects.get(email=email)
        user.password = make_password(new_password)
        user.save()
        messages.success(request, 'Password reset successful. Please login.')
        return redirect('/login/')
    return render(request, 'reset_password.html', {'email': email})