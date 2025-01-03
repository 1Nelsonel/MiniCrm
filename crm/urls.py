from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadAPIView, ContactAPIView, NoteAPIView, ReminderAPIView, UserLoginAPIView, UserLogoutAPIView, UserRegisterAPIView

urlpatterns = [
    # Authentication
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("register/", UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", UserLogoutAPIView.as_view(), name="user_logout"),

    # API
    path('leads/', LeadAPIView.as_view()),
    path('leads/<int:pk>/', LeadAPIView.as_view()),
    path('contacts/', ContactAPIView.as_view()),
    path('contacts/<int:pk>/', ContactAPIView.as_view()),
    path('notes/', NoteAPIView.as_view()),
    path('notes/<int:pk>/', NoteAPIView.as_view()),
    path('reminders/', ReminderAPIView.as_view()),
    path('reminders/<int:pk>/', ReminderAPIView.as_view()),
]