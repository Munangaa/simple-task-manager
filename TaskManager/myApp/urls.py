from django.urls import  path

from .views import task_list, create_task, get_task, update_task, delete_task, soft_delete_task, \
    user_register, get_user_profile, user_list, soft_delete_user

urlpatterns = [
    path('tasks/',task_list),
    path('tasks/create/', create_task),
    path('tasks/<int:id>',get_task),
    path('tasks/<int:id>/update/', update_task),
    path('tasks/<int:id>/delete/',delete_task),
    path('tasks/<int:id>/disable/',soft_delete_task),

    path('users/',user_list),
    path("users/create/", user_register),
    path("users/<int:id>", get_user_profile),
    path("users/<int:id>/update", get_user_profile),
    path('tasks/<int:id>/disable/',soft_delete_user),


]