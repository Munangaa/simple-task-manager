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

        user_id = request.GET.get('user_id')
        if user_id:
            tasks = Task.objects.filter(assigned_to=user_id, is_deleted=False)
        else:
            tasks = Task.objects.filter(is_deleted=False)
        data = [{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'is_completed': task.status.status_type == 'DONE',
            'priority': task.priority,
            'status': task.status.status_type,
            'assigned_to': task.assigned_to.id if task.assigned_to else None,
            'created_by': task.created_by.id if task.created_by else None,
            # 'priority': task.priority if hasattr(task, 'priority') else 'low',
        }
            for task in tasks
        ]

        return JsonResponse(data, safe=False)

    def post(self, request):

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        title = data.get('title')
        description = data.get('description')
        priority = data.get('priority', 'LOW')
        due_date = data.get('due_date')
        assigned_to_id = data.get('assigned_to')

        if not title:
            return JsonResponse({'error': 'Title required'}, status=400)

        status = get_object_or_404(States, status_type='PENDING')

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
             'is_completed': task.status.status_type == 'DONE',
             'status': task.status.status_type,
             'assigned_to': task.assigned_to.id if task.assigned_to else None,
             }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class TaskDetailListView(View):
    def get_object(self, task_id):

        return get_object_or_404(Task, id=task_id, is_deleted=False)

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'description':task.description,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'is_completed': task.status.status_type == 'DONE',
            'priority': task.priority,
            'status': task.status.status_type,
            'assigned_to': task.assigned_to.id if task.assigned_to else None,


        })

    def patch(self, request, task_id):


        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json'})

        task = get_object_or_404(Task, id=task_id)

        title = data.get('title')
        is_completed = data.get('is_completed')
        description = data.get('description')

        if title:
            task.title = title

        if description:
            task.description = description

        if is_completed is not None:
            status_type = 'DONE' if is_completed else 'PENDING'
            status = get_object_or_404(States, status_type=status_type)
            task.status = status

        task.save()

        return JsonResponse({
            'message': 'Task successfully updated',
            "id": task.id,
            "title": task.title,
            "description": task.description,
            'is_completed': task.status.status_type == 'DONE',
            "status": task.status.status_type,
        }, status=200)

    def delete(self, request, task_id):

        task = get_object_or_404(Task, id=task_id)
        task.is_deleted = True
        task.save()
        return JsonResponse({
            'message': 'Task deleted'

        })
