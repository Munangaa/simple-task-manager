import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import User

@csrf_exempt
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
    if request.method !='POST':
        return JsonResponse({'error':'Method should be GET'})
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid json'}, status=405)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'message': 'Please ensure you input the credentials'})

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Wrong credentials'})
    return JsonResponse({'message': 'Successful login'})
