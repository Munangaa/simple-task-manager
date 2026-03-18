import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import User, Task, States, Role
from ..utils.helper_functions import validate_request


@method_decorator(csrf_exempt, name='dispatch')
class UserListView(View):
    # get_user_profile

    # user_list
    def get(self, request):
        # error = validate_request(request, 'view_users', ['GET'])
        # if error:
        #     return error
        users = User.objects.filter(is_deleted=False)
        data = [{
            'username': user.username,
            'role': user.user_role.name
        }
            for user in users
        ]

        return JsonResponse({"users": data})


@method_decorator(csrf_exempt, name='dispatch')
class UserDetailView(View):
    def get(self, request, user_id):
        # error = validate_request(request, 'view_user', ['GET'])
        # if error:
        #     return error
        user = get_object_or_404(User, id=user_id)

        return JsonResponse({
            'user': {
                "username": user.username,
                "email": user.email,
                "role": user.user_role.name

            }
        }, status=200)

        #  user_update

    def put(self, request, user_id):
        # error = validate_request(request, 'update_user', ['PATCH', 'PUT'])
        # if error:
        #     return error
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json'}, status=400)

        user = get_object_or_404(User, id=user_id)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_name = data.get('role')

        if username:
            user.username = username
        if email:
            user.email = email
        if role_name:
            role = get_object_or_404(Role, name=role_name)
            user.user_role = role
        if password:
            user.set_password(password)
        user.save()

        return JsonResponse({
            "message": "User updated successfully",

        }, status=200)

    def delete(self, request, user_id):
        # error = validate_request(request, 'delete_user', ['DELETE'])
        # if error:
        #     return error
        user = get_object_or_404(User, id=user_id)

        user.is_deleted = True
        user.save()
        return JsonResponse({
            'message': 'User deleted'

        })


@method_decorator(csrf_exempt, name='dispatch')
class UserTaskView(View):
    def get_object(self, task_id):
        # task_id = self.kwargs['task_id']
        return get_object_or_404(Task, id=task_id, is_deleted=False)

    # user_tasks
    def get(self, request, user_id):
        # error = validate_request(request, 'view_task', ['GET'])
        # if error:
        #     return error

        user = get_object_or_404(User, id=user_id)
        tasks = Task.objects.filter(
            assigned_to=user,
            is_deleted=False
        )
        data = [{
            'id': task.id,
            'title': task.title,
            'status': task.status.name
        } for task in tasks]
        return JsonResponse({
            'user': user.id,
            'tasks': data
        })


@method_decorator(csrf_exempt, name='dispatch')
class AssignTaskView(View):
    def patch(self, request, user_id, task_id):
        # error = validate_request(request, 'assign_task', ['PATCH'])
        # if error:
        #     return error
        task = get_object_or_404(Task, id=task_id, is_deleted=False)
        user = get_object_or_404(User, id=user_id)
        task.assigned_to = user
        task.save()

        return JsonResponse({
            'message': 'Task assigned successfully',
        })


@method_decorator(csrf_exempt, name='dispatch')
class UpdateTaskStatusView(View):
    def patch(self, request, task_id):
        # error = validate_request(request, 'change_task_status', ['PATCH'])
        # if error:
        #     return error

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=404)
        status_name = data.get('status')
        if not status_name:
            return JsonResponse({'error': 'Status required'}, status=400)
        status = get_object_or_404(States, name=status_name)
        task = get_object_or_404(Task, id=task_id)

        task.status = status
        task.save()

        return JsonResponse({
            'message': 'Task status successfully updated',
        })
