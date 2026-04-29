import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..models import Task, States
from ..utils.helper_functions import validate_request


@method_decorator(csrf_exempt, name='dispatch')
class TaskListView(View):

    def get(self, request):
        # error = validate_request(request, 'view_task', ['GET'])
        # if error:
        #     return error
        user_id = request.GET.get('user_id')
        if user_id:
            tasks = Task.objects.filter(assigned_to = user_id,is_deleted = False)
        else:
            tasks = Task.objects.filter(is_deleted=False)

        # tasks = Task.objects.all()

        # tasks = Task.objects.filter(assigned_to = user_id)

        data = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'is_completed': task.status.status_type == 'COMPLETED',
        'priority':task.priority,
        'status':task.status.status_type,
        'assigned_to': task.assigned_to.id if task.assigned_to else None,
        'created_by': task.created_by.id if task.created_by else None,
        # 'priority': task.priority if hasattr(task, 'priority') else 'low',
        }
            for task in tasks
        ]

        return JsonResponse(data,safe=False)

    def post(self, request):
        # error = validate_request(request, 'create_task', ['POST'])
        # if error:
        #     return error
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority','LOW')
        due_date = data.get('due_date')
        assigned_to_id = data.get('assigned_to')

        if not title:
            return JsonResponse({'error':'Title required'},status=400)


        status = get_object_or_404(States,status_type = 'PENDING')

        # status_type = data.get('status', 'PENDING').upper()
        # status = get_object_or_404(States, status_type = status_type)

        task = Task.objects.create(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            assigned_to_id=assigned_to_id
        )
        return JsonResponse(
            {'Message': "Task created successfully",
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'status': task.status.status_type,
        'assigned_to': task.assigned_to.id if task.assigned_to else None,
             }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailListView(View):
    def get_object(self, task_id):
        # task_id = self.kwargs['task_id']
        return get_object_or_404(Task, id=task_id, is_deleted=False)

    def get(self, request, task_id):
        # error = validate_request(request, 'view_task', ['GET'])
        # if error:
        #     return error
        task = get_object_or_404(Task, id=task_id)

        return JsonResponse({
            'task': {
                'title': task.title,
                'status': task.status.name
            }
        })

    def patch(self, request, task_id):
        # error = validate_request(request, 'update_task', ['PUT', 'PATCH'])
        # if error:
        #     return error

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

    def delete(self, request, task_id):
        # error = validate_request(request, 'delete_task', ['DELETE'])
        # if error:
        #     return error

        task = get_object_or_404(Task, id=task_id)
        task.is_deleted = True
        task.save()
        return JsonResponse({
            'message': 'Task deleted'

        })
