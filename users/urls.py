from django.urls import path
from .views import SignUpView, MyProfileView

urlpatterns = [
    path('signup/',
         SignUpView.as_view(), name='signup'),
    path('myprofile/',
         MyProfileView.as_view(), name='myprofile')
]
