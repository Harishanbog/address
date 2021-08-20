from django.urls import path
from .views import signup,login,home,list,bookdetail,newbook,newaddress,dlt_book,dlt_address,update_address

app_name="useraddressbook"
urlpatterns=[
    path('',signup,name="signup"),
    path('login/',login,name="login"),
    path('home/',home.as_view(),name="home"),
    path('views/',list.as_view(),name="views"),
    path('bookdetail/<slug>',bookdetail,name="bookdetail"),
    path('newbook/',newbook,name="newbook"),
    path('newaddress/<slug>',newaddress,name="newaddress"),
    path('dlt_book/<slug>',dlt_book,name="dlt_book"),
    path('dlt_address/<slug>',dlt_address,name="dlt_address"),
    path('update_address/<slug>',update_address,name="update_address"),


]