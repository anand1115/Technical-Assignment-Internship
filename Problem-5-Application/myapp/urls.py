from django.urls import path
from .views import *

app_name="myapp"

urlpatterns=[
	path("",MyView.as_view(),name="Home"),
	path('login/',LoginView.as_view(),name="login"),
    path('signup/',SignupView.as_view(),name="signup"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('api/',calculate_api.as_view(),name="calculate"),
]