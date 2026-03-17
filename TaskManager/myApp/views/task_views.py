import json


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import Task, States, User
from ..utils.helper_functions import validate_request
from ..utils.permission_check import user_has_permission


class TaskListView(View):
    @csrf_exempt
    def get(self, request):
        error = validate_request(request, 'view_task', ['GET'])
        if error:
            return error

        tasks = Task.objects.all()

        data = [{
            'title': task.title,
            'status': task.status.name
        }
            for task in tasks
        ]

        return JsonResponse({"tasks": data})

    @csrf_exempt
    def post(self, request):
        error = validate_request(request, 'create_task', ['POST'])
        if error:
            return error
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        title = data.get('title')
        description = data.get('description')
        status_name = data.get('status', 'Pending')

        status = States.objects.get(name=status_name)

        task = Task.objects.create(title=title, description=description, status=status)
        return JsonResponse({'Message': "Task created successfully", 'task_id': task.id}, status=201)


class TaskDetailListView(View):
    def get_object(self):
        task_id = self.kwargs['task_id']
        return get_object_or_404(Task,id=task_id,is_deleted=False)

    @csrf_exempt
    def get(self, request):
        error = validate_request(request, 'view_task', ['GET'])
        if error:
            return error
        task = self.get_object()

        return JsonResponse({
            'task': {
                'title': task.title,
                'status': task.status
            }
        })

    @csrf_exempt
    def patch(self, request):
        error = validate_request(request, 'update_task', ['PUT', 'PATCH'])
        if error:
            return error

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json'})

        title = data.get('title')
        status = data.get('status')
        description = data.get('description')

        task = self.get_object()
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

    @csrf_exempt
    def delete(self, request):
        error = validate_request(request, 'delete_task', ['DELETE'])
        if error:
            return error


        task = self.get_object()
        task.is_deleted = True
        task.save()
        return JsonResponse({
            'message': 'Task deleted'

        })


