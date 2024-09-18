from django.urls import path
from .views import HomePageVew, RegisterPageVew, LoginPageVew

urlpatterns = [
    path('', HomePageVew.as_view(), name="home"),
    path('register/', RegisterPageVew.as_view(), name="register"),
    path('login/', LoginPageVew.as_view(), name="login")
]