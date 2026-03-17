import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import User, Task, States
from ..utils.helper_functions import validate_request


def get_user_profile(request, user_id):

    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})
    user = get_object_or_404(User, id=user_id)
    return JsonResponse({'user': {
        "username": user.username,
        "email": user.email,
        "role": user.user_role

    }
    }, status=200)


def user_update(request, user_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Should be a PUT or PATCH method'}, status=405)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Json'}, status=400)

    user = get_object_or_404(User, id=user_id)
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if username:
        user.username = username
    if email:
        user.email = email
    if role:
        user.user_role = role
    if password:
        user.set_password(password)
    user.save()

    return JsonResponse({
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.user_role
        }
    }, status=200)


def user_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})
    users = User.objects.all()
    data = [{
        'username': user.username,
        'role': user.user_role
    }
        for user in users
    ]

    return JsonResponse({"users": data})


def soft_delete_user(request, user_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    user = get_object_or_404(User, id=user_id)
    user.is_deleted = True
    user.save()
    return JsonResponse({
        'message': 'User deleted'

    })

def user_tasks(request, user_id):
    error = validate_request(request,'view_task',['GET'])
    if error:
        return error

    user = get_object_or_404(User,id=user_id)
    tasks = Task.objects.filter(
        assigned_to = user,
        is_deleted = False
    )
    data = [{
        'id':task.id,
        'title':task.title,
        'status':task.status.name
    } for task in tasks]
    return JsonResponse({
        'user':user.id,
        'tasks':data
    })

def assign_tasks(request, user_id, task_id):
    error = validate_request(request, 'assign_task', ['PATCH'])
    if error:
        return error
    task = get_object_or_404(Task, id=task_id,is_deleted=False)
    user = get_object_or_404(User,id=user_id)
    task.assigned_to = user
    task.save()

    return JsonResponse({
        'message': 'Task assigned successfully',
        'task': {
            'id': task.id,
            'assigned_to': user.id
        }
    })


def update_status(request, task_id):
    error = validate_request(request, 'change_task_status', ['PATCH'])
    if error:
        return error

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({})

    status_name = data.get('status')
    task = get_object_or_404(Task, id=task_id,is_deleted=False)

    if not status_name:
        return JsonResponse({'error': 'Status is required'}, status=400)
    status =get_object_or_404(States,name=status_name)
        # status = States.objects.get(name=status_name)
    task.status = status
    task.save()

    return JsonResponse({
        'message': 'Task status successfully updated',
        'task': {
            "id": task.id,
            "status": task.status.name,

        }
    })
