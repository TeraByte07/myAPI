from django.urls import path
from user_app.api.views import registration_view, logout_view, AuthorRequestView, AuthorApprovalView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),    
    path("register/", registration_view, name="register"),
    path('request-author/', AuthorRequestView.as_view(), name='request-author'),
    path('approve-author/<int:pk>/', AuthorApprovalView.as_view(), name='approve-author'),
    path("logout/", logout_view, name="logout"),
]
