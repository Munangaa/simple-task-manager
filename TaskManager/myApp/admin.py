from django.contrib import admin


from .models import Task, User, Role, Permission, States, RolePermission

# Register your models here.
admin.site.register(Task)
admin.site.register(User)
admin.site.register(States)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(RolePermission)