import re
from django import http
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import book,address
from django.views.generic import ListView
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv

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
                    messages.info(request,'User already exists')
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
        try:
            usr=User.objects.get(username=username)
        except:
            messages.info(request,'User doesnot exist please register')
            return redirect('/login')    


        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('useraddressbook:home')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/login')    

    else:
        
        return render(request,'useraddressbook/login.html')

def logout(request):
    auth.logout(request)      
    return redirect('/login')

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
        qs=book.objects.filter(user=request.user,bookname=bookname)
        if qs.exists():
            messages.info(request,'Book already exists')
            return render(request,"useraddressbook/newbook.html")

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
        qs=address.objects.filter(book=bookobj,phone=number)
        if qs.exists():
            messages.info(request,'Number already there')
            return render(request,"useraddressbook/newaddress.html")
        addressobj=address.objects.create(book=bookobj,name=name,phone=number)
        addressobj.save()
        return redirect('/'f"bookdetail/{slug}")
    else:
        return render(request,"useraddressbook/newaddress.html",{'book':slug})  

def dlt_book(request,slug):
    bookobj=get_object_or_404(book,id=slug)
    bookobj.delete()
    return redirect('useraddressbook:home')      

def dlt_address(request,int,slug):
    addressobj=get_object_or_404(address,id=slug)
    addressobj.delete() 
    return redirect('/'f"bookdetail/{int}")     


def update_address(request,int,slug):
    if request.method=="POST":
        name=request.POST['name']
        number=request.POST['number']
        qs=address.objects.filter(book=int,phone=number)
        addressobj=get_object_or_404(address,id=slug)
        if qs.exists():
            messages.info(request,'Number already there')
            return render(request,"useraddressbook/updateaddress.html",{'object':addressobj,'book':int})
        
        addressobj.name=name
        addressobj.phone=number
        addressobj.save()
        return redirect('/'f"bookdetail/{int}") 
    else:
        addressobj=get_object_or_404(address,id=slug)
        return render(request,"useraddressbook/updateaddress.html",{'object':addressobj,'book':int})  
     


def book_pdf(request,slug):   
    template_path='useraddressbook/bookpdf.html'
    bookobj=get_object_or_404(book,id=slug)
    addls=address.objects.filter(book=slug) 
    context={
        'book':bookobj,
        'object_list':addls
    }
    #create django response object and specify content_type as pdf
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition']='attachment; filename="book.pdf"'
    #find the template and render it
    template=get_template(template_path)
    html = template.render(context)

    #create pdf
    pisa_status=pisa.CreatePDF(html,dest=response)
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+html+'<pre>')
    return response    

          







