from django.contrib import admin
# Import models
from .models import User, Address, Country, State
# Register your models here.

class User_Admin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'last_name',
        'email',
        'is_active',
        'created',
        'modified',
    )

    readonly_fields = ('password', 'created', 'modified')
    # We added a search engine by name, surname and email
    search_fields = ['name', 'last_name', 'email']
    list_filter = ('is_active',)

admin.site.register(User, User_Admin)
admin.site.register(Address)
admin.site.register(Country)
admin.site.register(State)
