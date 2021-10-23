from django.urls import path,include
from rest_framework import routers

from . import views
from .views import (
    registration,
    LoginAPI,
)


router = routers.DefaultRouter()
router.register('create-library-book', views.createLibraryBook) 

urlpatterns = [
    path('register', registration, name="register"),
    path('login', LoginAPI, name="login"),
    path('', include(router.urls))
]