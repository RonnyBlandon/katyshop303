from django.contrib import admin
# Import models
from .models import User, Address, Country, State
# Register your models here.

class AddressAdmin(admin.StackedInline):
    model = Address
    extra = 0
    max_num = 1


class User_Admin(admin.ModelAdmin):
    inlines = [AddressAdmin,]

    list_display = (
        'id',
        'name',
        'last_name',
        'email',
        'is_active',
        'created',
        'modified',
    )

    exclude = ('groups', 'user_permissions',)
    readonly_fields = ('password', 'created', 'modified')
    # We added a search engine by name, surname and email
    search_fields = ['name', 'last_name', 'email']
    list_filter = ('is_active',)

admin.site.register(User, User_Admin)
admin.site.register(Country)
admin.site.register(State)
