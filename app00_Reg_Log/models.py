import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.forms import forms
# 工厂表
class Factory(models.Model):
    factory_id = models.AutoField(primary_key=True)
    factory_name = models.CharField(max_length=255)

    def __str__(self):
        return self.factory_name

# 武器表
class Weapon(models.Model):
    weapon_id = models.AutoField(primary_key=True)
    weapon_type = models.CharField(max_length=255)
    weapon_price = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=255)
    src = models.CharField(max_length=5000)

    def __str__(self):
        return self.weapon_type

# 仓库表
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=255)

    def __str__(self):
        return self.warehouse_name

# 工厂武器关系表
class FactoryWeapon(models.Model):
    factory = models.ForeignKey(Factory, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('factory', 'weapon'),)

# 仓库武器关系表
class WarehouseWeapon(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    weapon = models.ForeignKey(Weapon, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('warehouse', 'weapon'),)

# 用户表 (假设已经有用户模型，外键引用的 `username` 字段在这里定义为外部用户模型的一部分)
from django.contrib.auth.models import User

# 订单表
class Order(models.Model):
    STATUS_CHOICES = (
        ('已处理', '已处理'),
        ('未处理', '未处理'),
    )

    order_id = models.AutoField(primary_key=True)
    weapon = models.ForeignKey(Weapon, null=True, blank=True, on_delete=models.SET_NULL)
    order_date = models.DateTimeField(null=True, blank=True)
    statement = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    warehouse = models.ForeignKey(Warehouse, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Order {self.order_id}"
class UserManager(BaseUserManager):
    def create_user(self, user_name, user_pwd):
        if not user_name:
            raise ValueError('The User must have a username')
        user = self.model(user_name=user_name)
        user.set_password(user_pwd)
        user.save(using=self._db)
        return user

    def create_admin(self, admin_name, admin_pwd, factory=None):
        if not admin_name:
            raise ValueError('The Admin must have a username')
        admin = self.model(admin_name=admin_name, factory=factory)
        admin.set_password(admin_pwd)
        admin.save(using=self._db)
        return admin

from django.utils.timezone import now
class Users(AbstractBaseUser):
    user_name = models.CharField(max_length=20, unique=True, primary_key=True)
    user_pwd = models.CharField(max_length=128)  # Use Django's hashed password system
    # last_login = models.DateTimeField('data_publish', default=str(now))
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = []

    def check_password1(self, raw_password):
        user = self.check_password(raw_password)
        return user

    def __str__(self):
        return self.user_name

class Admin(AbstractBaseUser):
    admin_name = models.CharField(max_length=20, unique=True, primary_key=True)
    # admin_pwd = models.CharField(max_length=128)  # Use Django's hashed password system
    factory = models.ForeignKey(Factory, null=True, blank=True, on_delete=models.SET_NULL)

    objects = UserManager()

    USERNAME_FIELD = 'admin_name'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.admin_name

