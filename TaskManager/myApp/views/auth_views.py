import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import User, Role
from ..utils.helper_functions import validate_request


@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(View):
    def post(self, request):

        try:
            data = json.loads(request.body)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'invalid Json'}, status=400)

        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        # role = data.get('user_role')
        role = Role.objects.get(name="Member")

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User(username=username, email=email, user_role=role)
        user.set_password(password)
        user.save()

        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'username': user.username,
                'email': user.email,
                'role': user.user_role.name

            },

        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def post(self, request):
        # if request.method !='GET':
        #     return JsonResponse({'error':'Method should be 'GET'})
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
