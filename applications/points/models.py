from django.db import models
# Import models
from applications.user.models import User
from applications.order.models import Order
# Import Managers
from .managers import PointManager, PointsHistoryMaager, UserPointManager

# Create your models here.
class UserPoint(models.Model):
    points = models.IntegerField('Puntos', default=0)
    id_user = models.OneToOneField(User, verbose_name="Puntos del usuario", on_delete=models.CASCADE, related_name='user_points')

    objects = UserPointManager()

    def __str__(self):
        return str(self.id) +' '+ str(self.points) +' '+str(self.id_user)


class PointsHistory(models.Model):
    points = models.IntegerField('Puntos')
    event = models.CharField('Evento', max_length=40)
    id_order = models.ForeignKey(Order, verbose_name='Id de la orden', null=True, on_delete=models.CASCADE)
    date = models.DateTimeField('Fecha')
    user_points = models.ForeignKey(UserPoint, verbose_name="Puntos del Usuario", on_delete=models.CASCADE, related_name='points_history')

    objects = PointsHistoryMaager()

    def __str__(self):
        return str(self.id) +' '+ str(self.points) +' '+ self.event


class PointsSetting(models.Model):
    earning_points_rate = models.IntegerField('Tasa de puntos por dolar', default=1)
    redemption_rate = models.IntegerField('Tasa de Canjeo por dolar', default=35)

    objects = PointManager()

    def __str__(self):
        return str(self.earning_points_rate) +' '+ str(self.redemption_rate)