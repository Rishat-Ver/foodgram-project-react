from django.contrib import admin
from users.models import Follow, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'password',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class FolowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')
    search_fields = ('user', 'author')
