from django.urls import path

from .views.auth_views import UserRegisterView, UserLoginView, PasswordResetView, PasswordResetConfirmView
from .views.task_views import TaskListView, TaskDetailListView
from .views.user_views import UserListView, UserTaskView, UserDetailView, UpdateTaskStatusView, AssignTaskView

urlpatterns = [
    path('tasks/', TaskListView.as_view()),
    path('tasks/<int:task_id>/', TaskDetailListView.as_view()),

    path('users/', UserListView.as_view()),
    path('users/<int:user_id>/', UserDetailView.as_view()),
    path('users/<int:task_id>/tasks/', UserTaskView.as_view()),
    path('users/<int:user_id>/tasks/<int:task_id>/assign/', AssignTaskView.as_view()),
    path('users/<int:task_id>/update/', UpdateTaskStatusView.as_view()),
    # path('tasks/create/', create_task),
    path('register/',UserRegisterView.as_view()),
    path('login/',UserLoginView.as_view()),
    path('forgot-password/', PasswordResetView.as_view()),
    path('reset-password/<str:token>/', PasswordResetConfirmView.as_view()),


    # path('tasks/<int:id>',get_task),
    # path('tasks/<int:id>/update/', update_task),
    # path('tasks/<int:id>/delete/',delete_task),
    # path('tasks/<int:id>/disable/',soft_delete_task),

    # path('users/',user_list),
    # path("users/create/", user_register),
    # path("users/<int:id>", get_user_profile),
    # path("users/<int:id>/update", get_user_profile),
    # path('tasks/<int:id>/disable/',soft_delete_user),

]
