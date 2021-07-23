from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserNew
    list_display = ['username', 'is_student', 'is_teacher']
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('is_student', 'is_teacher')}),
    )

admin.site.register(Major)
admin.site.register(Year)
admin.site.register(Post)
admin.site.register(Subject)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Join_Room)


admin.site.register(UserNew, CustomUserAdmin)

class ClassRoomAdmin(admin.ModelAdmin):
	list_display = ('name','major','year','subject','teacher','start','can_join','password',)

admin.site.register(ClassRoom,ClassRoomAdmin)