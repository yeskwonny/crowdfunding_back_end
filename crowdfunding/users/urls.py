from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.CustomUserList.as_view()),
  path('users/<int:pk>', views.CustomUserDetail.as_view()),
  path('user/id/<int:pk>/',views.CustomUserDetailByID.as_view())
  
]
