from gettext import install
from msilib.schema import InstallUISequence
from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from .forms import CreateUser
from .models import Student, Attendace, Userinfo
@login_required(login_url='loginpage')
def home(request):

    return render(request,'base/home.html/',{})
# homenisauna
@login_required(login_url='loginpage')
def attend(request):
    if request.method=="POST":
        suser=(request.POST.get("studentid"))
        try:
            user=Student.objects.get(Lecturer=request.user,studentid=suser)
            obj=Attendace.objects.create(teacheroperate=request.user,student=user)
            obj.save()
            messages.success(request, 'Succesfully added student to present')
            # user=Student.objects.get(studentid=suser)
        except:
            messages.error(request, 'This Student ID is does not exist!')
        
       

        
        # user=Student.objects.get(Lecturer=request.user,studentid=suser)
        

        
        #   
        # return redirect("home")
    context={}
    return render(request,'base/attendclass.html/',context)

def loginPage(request):
    if request.method=="POST":
        username=request.POST.get("username").lower()
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except: 
            messages.error(request, 'Either Username or Password is invalid or maybe does not exist')

        user=authenticate(request, username=username,password= password)
        if user is not None:
            login(request,user)
            return redirect('home')
    context={}

    return render(request,'base/loginpage.html/',context)


def userout(request):
    logout(request)
    return redirect('loginpage')

def registerPage(request):
    form=CreateUser()
    if request.method=="POST":
        form=CreateUser(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Bad Credential, please try again!')
    context={'form': form}
    return render(request,'base/registerpage.html/',context)   

@login_required(login_url='loginpage')
def records(request):
    cuser=Attendace.objects.filter(teacheroperate=request.user)

    context={'obj2':cuser} 
    return render(request,"base/records.html",context)


@login_required(login_url='loginpage')
def mystudent(request):
    obj=Student.objects.filter(Lecturer=request.user)
    context={'m':obj}
    return render(request,"base/mystudent.html",context)

@login_required(login_url='loginpage')
def addstudent(request):
    if request.method=="POST":
        studentid=request.POST.get("studentid")
        fname=request.POST.get("firstname")
        lname=request.POST.get("lastname")
        status=request.POST.get("status")
        mobile=request.POST.get("MobileNumber")
        obj=Student.objects.create(
            Lecturer=request.user,
            studentid=studentid,
            firstname=fname,
            lastname=lname,
            ustatus=status,
            mobilenum=mobile
            )
        obj.save()
        messages.error(request, 'Adding student is Successful,add ')
    context={}
    return render(request,"base/addstudent.html",context)   

@login_required(login_url='loginpage')
def managerec(request):
    obj=Student.objects.filter(Lecturer=request.user)
    context={
        'obj':obj
    }
    return render(request,"base/manage.html",context)

@login_required(login_url='loginpage')
def studentedit(request,pk):
    page='editpage'
    obj=Student.objects.get(id=pk)

    if request.method=="POST":
        obj.studentid=request.POST.get('studentid')
        obj.firstname=request.POST.get('firstname')
        obj.lastname=request.POST.get('lastname')
        obj.ustatus=request.POST.get('status')
        obj.mobilenum=request.POST.get('mobilenumber')
        obj.save();
        return redirect('manage')
    context={
        'obj':obj,
        'page':page
    }
    return render(request,"base/crudstudent.html",context)

@login_required(login_url='loginpage')
def studentdel(request,pk):
    obj=Student.objects.get(id=pk)
    if request.method=="POST":
        obj.delete()
        return redirect('manage')
    context={
        'obj':obj
    }
    return render(request,"base/crudstudent.html",context)

@login_required(login_url='loginpage')
def myinfo(request):
    
    try:
        obj=Userinfo.objects.get(teacherinfo=request.user) 
        
    except:
        return redirect('updateinfo')

    obj=Userinfo.objects.get(teacherinfo=request.user)  
   
    context={
        'obj':obj
    }
    
    return render(request,"base/myinfo.html",context)

def updatemyinfo(request):
    
    if request.method=="POST":
        fname=request.POST.get("firstname")
        lname=request.POST.get("lastname")
        status=request.POST.get("status")
        mobile=request.POST.get("mobilenumber")
        useraddress=request.POST.get("address")
        obj=Userinfo.objects.create(
            teacherinfo=request.user,
            firstname=fname,
            lastname=lname,
            status=status,
            mobilenum=mobile,
            address=useraddress
            )
        obj.save()
    context={}
    return render(request,"base/updatemyinfo.html",context)
