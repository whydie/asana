from django.urls import path

from .views import (
    UserListCreate, UserRetrieve,
    TaskListCreate, TaskRetrieveUpdateDestroy,
    ProjectListCreate, ProjectRetrieveUpdateDestroy
)

urlpatterns = [
    path('api/users/', UserListCreate.as_view(), name="users"),
    path('api/users/<int:pk>/', UserRetrieve.as_view(), name="user"),

    path('api/tasks/', TaskListCreate.as_view(), name="tasks"),
    path('api/tasks/<int:pk>/', TaskRetrieveUpdateDestroy.as_view(), name="task"),

    path('api/projects/', ProjectListCreate.as_view(), name="projects"),
    path('api/projects/<int:pk>/', ProjectRetrieveUpdateDestroy.as_view(), name="project"),
]
