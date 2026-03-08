import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Task, User


def task_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})
    tasks = Task.objects.all()
    data = [{
        'title': task.title,
        'status': task.status
    }
        for task in tasks
    ]

    return JsonResponse({"tasks": data})


def get_task(request, task_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})

    task = get_object_or_404(Task, id=task_id)

    return JsonResponse({
        'task':{
            'title':task.title,
            'status':task.status
        }
    })


def create_task(request):
    if request.method != 'POST':
        return JsonResponse({
            'error': 'Method not allowed'
        })
    data = json.loads(request.body)
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'Pending')

    task = Task.objects.create(title=title, description=description, status=status)
    return JsonResponse({'Message': "Task created successfully", 'task_id': task.id}, status=201)


def update_task(request, task_id):
    if request.method not in ['PUT', 'PATCH']:
        return JsonResponse({'error': 'Invalid method'})
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid Json'})

    title = data.get('title')
    status = data.get('status')
    description = data.get('description')

    task = get_object_or_404(Task, id=task_id)
    if title:
        task.title = title
    if status:
        task.status = status
    if description:
        task.description = description
    task.save()

    return JsonResponse({
        'message': 'Task successfully updated',
        'task': {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,

        }
    }, status=201)


def soft_delete_task(request, task_id):
    if request.method != 'DELETE':
        return JsonResponse({'error':'Method not allowed'},status=405)
    task = get_object_or_404(Task,id=task_id)
    task.is_deleted(True)
    task.save()
    return JsonResponse({
        'message':'Task deleted'

    })

def delete_task(request,task_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'},status=405)
    task = get_object_or_404(Task,id=task_id)
    task.delete()
    return JsonResponse({
        'message':'Task deleted'

    })


def user_register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'invalid Json'}, status=400)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = data.get('role')

    if not username or not password:
        return JsonResponse({'error': 'Username and password required'})
    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username already exists'}, status=400)

    user = User(username=username, email=email, role=role)
    user.set_password(password)
    user.save()

    return JsonResponse({
        'message': 'User created successfully',
        'user': {
            'username': user.username,
            'email': user.email,
            'role': role

        },

    }, status=201)


def user_login(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid json'}, status=405)
    username = data.username('username')
    password = data.password('password')

    if not username or not password:
        return JsonResponse({'message': 'Please ensure you input the credentials'})

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Wrong credentials'})
    return JsonResponse({'message': 'Successful login'})


def get_user_profile(request, user_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})
    user = get_object_or_404(User,id=user_id)
    return JsonResponse({'user':{
        "username": user.username,
        "email": user.email,
        "role": user.role

    }
    },status=200)


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
        user.role = role
    if password:
        user.set_password(password)
    user.save()

    return JsonResponse({
        "message": "User updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    }, status=200)

def user_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'})
    users = User.objects.all()
    data = [{
        'username': user.username,
        'role':user.role
    }
        for user in users
    ]

    return JsonResponse({"users": data})

def soft_delete_user(request,user_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    user = get_object_or_404(User, id=user_id)
    user.is_deleted(True)
    user.save()
    return JsonResponse({
        'message': 'User deleted'

    })


