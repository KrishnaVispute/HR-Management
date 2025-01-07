from django.shortcuts import render,redirect,get_object_or_404
from Department.models import Department,Role,Users
from django.contrib.auth.hashers import make_password

# Create your views here.
def home(request):
    data=Department.objects.filter(status=True)
    context={}
    context['department']= data
    return render(request,'viewdepartment.html',context)

def modifyDepart(request):
    # Only get active departments
    data = Department.objects.filter(status=True)
    context = {}
    context['department']= data
    return render(request, 'index.html', context)

def createDepartment(request):
    if request.method == 'GET':
        return render(request,'createdepartment.html')
    else:
        n = request.POST['dept_name']
        d = request.POST['description']
        dept = Department.objects.create(dept_name=n, description =d)
        dept.save()
        return redirect('/')
    
def Deletedepartment(request, did):
    dept = Department.objects.get(dept_id = did)
    dept.status=False
    print(dept)
    print(dept.status)
    dept.save()
    return redirect('/')

def updateDepartment(request, did):
    if request.method == "GET":
        d = Department.objects.filter(dept_id=did) 
        context = {}
        context['dept'] = d 
        return render(request,'updatedepartment.html',context)
    else:
        dep = Department.objects.filter(dept_id = did)
        n = request.POST['dept_name']
        d = request.POST['description']
        dep.update(dept_name=n, description =d)
        return redirect('/')
    
# Roles

def viewRole(request):
    data=Role.objects.filter(status=True)
    context={}
    context['roles']=data
    return render(request,'viewrole.html',context)


def addRole(request):
    print(request.method)
    if request.method=='GET':
        return render(request,'addrole.html')
    else:
        #capture data from form
        n = request.POST['role_name']
        d = request.POST['description']
        print(n,d)

        #add the data in db
        r=Role.objects.create(role_name=n,description=d)
        r.save()
        # return render(request,'index.html')
        # return render(request,'index.html',context)
        return redirect('/viewrole')

def Deleterole(request, rid):
    # Get the department object
    role = Role.objects.get(role_id=rid)
    # Update the status to False (inactive)
    role.status = False
    print(role.status)
    role.save()  # Save the updated status to the database
    return redirect('/viewrole')

def Updaterole(request,rid):
    r=Role.objects.get(role_id=rid) 
    if request.method=='GET':
        context={}
        context['role']=r # used with GET method
        return render(request,'updaterole.html',context)
    else:
        ur=Role.objects.filter(role_id=rid)
        n=request.POST['role_name']
        d=request.POST['description']
        ur.update(role_name=n,description=d)
        return redirect('/viewrole')
    
#employee

def view_employees(request):
    employees = Users.objects.all()
    return render(request, 'view_employees.html', {'employees': employees})

def add_employee(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        departments = Department.objects.filter(status=True)
        users = Users.objects.all()
        return render(request, 'addemployee.html', {
            'roles': roles,
            'departments': departments,
            'users': users
        })
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        
        role_id = request.POST.get('role')
        department_id = request.POST.get('department')
        reporting_manager_id = request.POST.get('reporting_manager')  # This can be empty

        role = Role.objects.get(role_id=role_id)
        department = Department.objects.get(dept_id=department_id)
        
        # Handle empty reporting_manager by setting it to None if not provided
        reporting_manager = None
        if reporting_manager_id:
            reporting_manager = Users.objects.get(id=reporting_manager_id)

        date_of_joining = request.POST['date_of_joining']
        username = request.POST['username']
        password = make_password(request.POST['password'])

        Users.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            role=role,
            department=department,
            reporting_manager=reporting_manager,  # This can be None
            date_of_joining=date_of_joining,
            username=username,
            password=password
        )

        return redirect('/viewemployees')



def update_employee(request, employee_id):
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
    employee = get_object_or_404(Users, id=employee_id)
    employee.delete()
    return redirect('/viewemployees')