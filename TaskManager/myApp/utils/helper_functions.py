from django.http import JsonResponse

from TaskManager.myApp.utils.permission_check import user_has_permission


def get_user_data(request,allowed_methods):
    if request.method not in allowed_methods:
        return JsonResponse({'error':'Method not allowed'},status=405)
    return None

def require_permission(user,permission_codename):
    if not user_has_permission(user, permission_codename):
        return JsonResponse({'error':'Permission denied'},status=403)
    return None

def validate_request(request,permission_codename,allowed_methods):
    if request.method not in allowed_methods:
        return JsonResponse({'error':'Method not allowed'},status=405)
    elif not user_has_permission(request.user,permission_codename):
        return JsonResponse({'error':'Permission denied'},status=403)
    return None
