from datetime import datetime
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# import models
from .models import UserPoint, PointsHistory, PointsSetting
# Register your models here.

class PointsSettingAdmin(admin.ModelAdmin):
    list_display = ('earning_points_rate', 'redemption_rate')
    # There should only be one record that saves the configurations of the application of the points, 
    # so we remove the permissions to add and delete records in the admin.
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class PointsHistoryAdmin(admin.ModelAdmin):
    def order_id(self, obj):
        if obj.id_order:
            return obj.id_order.id
    list_display = ['points', 'event', 'order_id', 'date', 'user_points']

    readonly_fields = ('event',)


class UserPointAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Check if the request comes from the admin panel
        if request.user.is_staff:
            try:
                previous_object = UserPoint.objects.get(id=obj.id)
            except UserPoint.DoesNotExist:
                previous_object = None
            
            if previous_object:
                previous_points = previous_object.points
                current_points = obj.points

                modified_points = current_points - previous_points
                PointsHistory.objects.create(
                    points=modified_points,
                    event=_('Adjusted Points'),
                    id_order=None,
                    date=datetime.now(),
                    user_points=obj
                )
        
        super().save_model(request, obj, form, change)

admin.site.register(UserPoint, UserPointAdmin)
admin.site.register(PointsHistory, PointsHistoryAdmin)
admin.site.register(PointsSetting, PointsSettingAdmin)
