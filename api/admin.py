from django.contrib import admin
from api.models import User, ClassRoom, Assignment, Submission

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Instructor, Student, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('firstname', 'lastname')}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser',)}),
        #    'groups', 'user_permissions')}),
        (_('User Category'), {'fields': ('is_student', 'is_instructor')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'firstname', 'lastname',
                    'is_staff', 'is_instructor', 'is_student',)
    search_fields = ('email', 'firstname', 'lastname')
    ordering = ('pk',)


admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(ClassRoom)
admin.site.register(Assignment)
admin.site.register(Submission)
