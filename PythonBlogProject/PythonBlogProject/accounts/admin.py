from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile Details'
    fk_name = 'user'


class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_skills')

    @admin.display(description='Skills')
    def get_skills(self, instance):
        if hasattr(instance, 'profile'):
            return instance.profile.skills
        return '-'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'interests', 'created_at')
    search_fields = ('user__username', 'user__email', 'skills', 'interests', 'bio')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
