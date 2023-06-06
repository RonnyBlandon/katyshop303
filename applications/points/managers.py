from datetime import datetime
from django.db import models

class PointManager(models.Manager):
    """ procedures for Points """
    def get_point_setting(self):
        try:
            point_setting = self.get()
            return point_setting
        except self.model.DoesNotExist:
            return None
        

class UserPointManager(models.Manager):
    """ procedures for User Points """
    def get_user_points(self, id_user):
        try:
            user_points = self.get(id_user=id_user)
            return user_points
        except self.model.DoesNotExist as err:
            print('Object not found: ', err)
            return None
        
    def add_points_to_user(self, valor, point_rate, id_user):
        user_points = UserPointManager.get_user_points(self, id_user=id_user)
        points = round(valor * point_rate)
        user_points.points += points
        user_points.save()
        return user_points

        
    def deduct_points_to_user(self, valor, point_rate, id_user):
        user_points = UserPointManager.get_user_points(self, id_user=id_user)
        points = round(valor * point_rate)
        user_points.points -= points
        user_points.save()
        return user_points


class PointsHistoryMaager(models.Manager):
    """ procedures for User PointsHistory """
    def points_added(self, valor, point_rate, event, order, user_points):
        points = valor * point_rate
        user_points_history = self.create(
            points = round(points),
            event=event,
            id_order = order,
            date=datetime.now(),
            user_points=user_points
        )

        return user_points_history
    
    def points_deducted(self, valor, point_rate, event, order, user_points):
        points = valor * point_rate
        user_points_history = self.create(
            points = round(points * -1), 
            event=event,
            id_order = order,
            date=datetime.now(),
            user_points=user_points
        )

        return user_points_history
