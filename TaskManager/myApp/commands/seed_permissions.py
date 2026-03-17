from ..models import Role, Permission, RolePermission


def seed_permissions():
    permissions = [
        'create_task',
        'view_task',
        'update_task',
        'delete_task',
        'assign_task',
        'change_task_status'
    ]

    roles = [
        'Manager',
        'Member'
    ]

    role_permissions = {
        'Manager': [
            'create_task',
            'view_task',
            'update_task',
            'delete_task',
            'assign_task',
            'change_task_status'],
        'Member': [
            'create_task',
            'view_task',
            'change_task_status'
        ]
    }
    for permission in permissions:
        Permission.objects.get_or_create(name=permission, codename=permission)

    for role in roles:
        Role.objects.get_or_create(name=role)

    for role_name, permission_list in role_permissions.items():
        role = Role.objects.get(name=role_name)
        for permission_name in permission_list:
            permission_obj= Permission.objects.get(codename=permission_name)
            RolePermission.objects.get_or_create(role=role, permission=permission_obj)
