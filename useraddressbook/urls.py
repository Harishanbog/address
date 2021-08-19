from django.urls import path
from .views import signup,login,home,create_address,update,list,delete_address

app_name="useraddressbook"
urlpatterns=[
    path('',signup,name="signup"),
    path('login/',login,name="login"),
    path('home/',home,name="home"),
    path('create/',create_address,name="create_address"),
    path('update/',update,name="update"),
    path('views/',list.as_view(),name="views"),
    path('delete_address/<slug>',delete_address,name="delete_address")
]