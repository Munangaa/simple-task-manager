from django.urls import  path

from .views.auth_views import user_register
from .views.task_views import TaskListView,TaskDetailListView
from .views.user_views import user_list, get_user_profile, soft_delete_user

urlpatterns = [
    path('tasks/',TaskListView.as_view()),
    path('tasks/<int:task_id>/',TaskDetailListView.as_view()),
    # path('tasks/create/', create_task),
    # path('tasks/<int:id>',get_task),
    # path('tasks/<int:id>/update/', update_task),
    # path('tasks/<int:id>/delete/',delete_task),
    # path('tasks/<int:id>/disable/',soft_delete_task),

    path('users/',user_list),
    path("users/create/", user_register),
    path("users/<int:id>", get_user_profile),
    path("users/<int:id>/update", get_user_profile),
    path('tasks/<int:id>/disable/',soft_delete_user),


]