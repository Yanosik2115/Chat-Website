from django.urls import path
from . import views

urlpatterns = [
    path("", views.lobby),
    path("room/", views.room),
    path("get_token/", views.getToken, name="getToken"),
    path("create_member/", views.createMember, name="createUser"),
    path("get_member/", views.getMember, name="getMember"),
    path('delete_member/', views.deleteMember, name='deleteMember')
]
