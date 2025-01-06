from django.shortcuts import render,redirect,get_object_or_404
from Department.models import Department,Role
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

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
    
# def Deletedepartment(request, did):
#     dept = Department.objects.get(dept_id = did)
#     dept.status=False
#     print(dept)
#     print(dept.status)
#     dept.save()
#     return redirect('/')

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