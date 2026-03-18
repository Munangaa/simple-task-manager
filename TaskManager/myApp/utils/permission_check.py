from ..models import RolePermission


def user_has_permission(user,permission_codename):
    role_permissions = RolePermission.objects.filter(
        role = user.user_role,
        permission__codename = permission_codename
    )
    return  role_permissions.exists()