import json
import secrets
from  django.core.mail import  send_mail
from django.contrib.auth import  get_user_model
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import User, Role
from ..utils.helper_functions import validate_request
reset_tokens = {}
tokens = {}
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
        try:
            role = Role.objects.get(name="Member")
        except Role.DoesNotExist:
            return JsonResponse({'error':'Default role not found'},status=500)

        # user = User(username=username,email=email,user_role=role)
        # user.set_password(password)
        # user.save()
        # role = data.get('user_role')
        #

        if not username or not password:
            return JsonResponse({'error': 'Username and password required'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'email already exists'}, status=400)

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
        # return JsonResponse({'message': 'Successful login'})

        token = secrets.token_hex(32)
        tokens[token] = user.id

        return JsonResponse({
            'message':'succesful login',
            'token':token,
            'user_id':user.id,
            'username':user.username,
            'role':user.user_role.name if user.user_role else 'Member',
            'email':user.email,
        })
@method_decorator(csrf_exempt, 'dispatch')
class PasswordResetView(View):
    def post(self,request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        email = data.get('email')
        if not email:
            return JsonResponse({'error': 'Email required'}, status=400)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            # Don't reveal if email exists or not for security
            return JsonResponse({'message': 'If this email exists you will receive a reset link'})

            # Generate reset token
        token = secrets.token_hex(32)
        reset_tokens[token] = user.id

        reset_link = f'http://192.168.1.22:8000/taskmanager/reset-password/{token}/'
        send_mail(
            subject='Task-It Password Reset',
            message=f'Click this link to reset your password: {reset_link}',
            from_email='noreply.taskitapp@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'If this email exists you will receive a reset link'})

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetConfirmView(View):
    def post(self, request, token):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        new_password = data.get('new_password')
        if not new_password:
            return JsonResponse({'error': 'New password required'}, status=400)

        # Check token is valid
        user_id = reset_tokens.get(token)
        if not user_id:
            return JsonResponse({'error': 'Invalid or expired token'}, status=400)

        # Update password
        User = get_user_model()
        user = User.objects.get(id=user_id)
        user.set_password(new_password)
        user.save()

        # Delete used token
        del reset_tokens[token]

        return JsonResponse({'message': 'Password reset successful'})



