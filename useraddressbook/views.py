from django import http
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import address
from django.views.generic import ListView

# Create your views here.
def signup(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']

        if password1==password2:    
                if User.objects.filter(email=email).exists(): 
                    messages.info(request,'Email Taken')
                    return redirect('/')
                else:
                    user=User.objects.create_user(username=email,first_name=first_name,last_name=last_name,password=password1,email=email)
                    user.save()
                    return render(request,"useraddressbook/login.html")    
            
    else:
        return render(request,"useraddressbook/index.html")


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        usr=User.objects.get(username=username)
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request,'useraddressbook/home.html',{'user':usr})

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')    

    else:
        
        return render(request,'useraddressbook/login.html')

def home(request):
    if request.method=="POST":
        if request.POST['type']=='create':
            usr=request.POST['user']
            return render(request,"useraddressbook/create.html",{'user':usr})
        if request.POST['type']=='create':
            usr=request.POST['user']
            addressusr=address.objects.get(user=usr)
            return render(request,"useraddressbook/update.html",{'user':usr,'address_usr':addressusr})
            
    else:
        return render(request,"useraddressbook/home.html")

def create_address(request):
    if request.method=="POST":
        name=request.POST['name']
        number=request.POST['number']
        user=request.POST['user']
        usr=User.objects.get(username=user)

        addres=address.objects.create(user=usr,name=name,phone=number)
        addres.save()
        return HttpResponse("user created")
    else:
        return render(request,"useraddressbook/create.html")  

def update(request):
    if request.method=="POST":
        name=request.POST['name']
        number=request.POST['number']
        user=request.POST['user']
        usr=User.objects.get(username=user)

        addres=address.objects.create(user=usr,name=name,phone=number)
        addres.save()
        return HttpResponse("details changed")

class list(ListView):
    template_name="useraddressbook/views.html"
    model=address


def delete_address(request,slug):
    print("hi")
    addres=address.objects.get(name=slug)
    addres.delete()
    
    return redirect('useraddressbook:home')


          







