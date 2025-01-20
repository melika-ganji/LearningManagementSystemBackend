from django.contrib import admin
from accounts.models import CustomUser, AdminProfile, ProfessorProfile, StudentProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('phone_number',)
    ordering = ('id',)


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_name', 'username', 'phone_number')
    search_fields = ('name', 'last_name', 'username')
    ordering = ('id',)


@admin.register(ProfessorProfile)
class ProfessorProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'specialty', 'contact_number')
    search_fields = ('name', 'specialty')
    ordering = ('id',)


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'student_id', 'contact_number')
    search_fields = ('name', 'student_id')
    ordering = ('id',)
