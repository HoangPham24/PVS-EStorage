from django.contrib import admin
from users.models import *
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportActionModelAdmin

from .forms import AdminUserChangeForm, AdminUserCreationForm

# Register your models here.


class UserAdmin(ImportExportActionModelAdmin):

    add_form = AdminUserCreationForm
    form = AdminUserChangeForm
    list_display = ["email", "is_staff","is_active",'is_admin']
    model = User
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Password', {'fields': ('password',)}),
        ('dates',{'fields':('last_login',)}),
        ('Permissions', {'fields': ('is_admin','is_staff','is_active','is_superuser','user_permissions','groups')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_admin','is_staff','is_active','is_superuser','user_permissions','groups')}
        ),
    )
    ordering = ["email",]
    search_fields = ("email",)

# Staff Admin
from import_export import resources
class StaffAdminResource(resources.ModelResource):
    class Meta:
        model = StaffProfile
        import_id_fields = ('user', )
        
    
class StaffAdmin(ImportExportActionModelAdmin):
    list_display = ['user', 'department', 'contract', 'position']
    resource_class = StaffAdminResource 

    
    

class DepartmentAdmin(ImportExportActionModelAdmin):
    model = Department
    list_display = ["name"]      
    
# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(StaffProfile, StaffAdmin)
admin.site.register(Department, DepartmentAdmin)



