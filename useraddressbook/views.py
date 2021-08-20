import re
from django import http
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import book,address
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
            return redirect('useraddressbook:home')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')    

    else:
        
        return render(request,'useraddressbook/login.html')

 

class home(LoginRequiredMixin,ListView):
    login_url="/login"
    model=book
    template_name="useraddressbook/home.html"
    def get_queryset(self):
        return book.objects.filter(user=self.request.user)

            

 

 
class list(ListView):
    template_name="useraddressbook/views.html"
    model=address

 

def bookdetail(request,slug):
    book=address.objects.filter(book=slug)    
    context={
        'object_list':book,
        'book':slug
    }
    return render(request,"useraddressbook/bookdetail.html",context)


def newbook(request):
    if request.method=="POST":
        bookname=request.POST['bookname']
        bookobj=book.objects.create(user=request.user,bookname=bookname)
        bookobj.save()
        return redirect('useraddressbook:home')
    else:
        return render(request,"useraddressbook/newbook.html")

def newaddress(request,slug):
    if request.method=="POST":
        name=request.POST['name']
        number=request.POST['number']
        bookobj=book.objects.get(user=request.user,id=slug) 
        addressobj=address.objects.create(book=bookobj,name=name,phone=number)
        addressobj.save()
        return redirect('/'f"bookdetail/{slug}")
    else:
        return render(request,"useraddressbook/newaddress.html")  

def dlt_book(request,slug):
    bookobj=get_object_or_404(book,id=slug)
    bookobj.delete()
    return redirect('useraddressbook:home')      

def dlt_address(request,slug):
    addressobj=get_object_or_404(address,id=slug)
    addressobj.delete() 
    return redirect('useraddressbook:home')     


def update_address(request,slug):
    if request.method=="POST":
        name=request.POST['name']
        number=request.POST['number']
        addressobj=get_object_or_404(address,id=slug)
        addressobj.name=name
        addressobj.number=number
        addressobj.save()
        return redirect('useraddressbook:home')  
    else:
        addressobj=get_object_or_404(address,id=slug)
        return render(request,"useraddressbook/updateaddress.html",{'object':addressobj})  
     

          







