# Generated by Django 5.1.4 on 2024-12-12 02:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Factory",
            fields=[
                ("factory_id", models.AutoField(primary_key=True, serialize=False)),
                ("factory_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "user_name",
                    models.CharField(
                        max_length=20, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("user_pwd", models.CharField(max_length=128)),
                (
                    "last_login",
                    models.DateTimeField(
                        default="<function now at 0x103572fc0>",
                        verbose_name="data_publish",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                ("warehouse_id", models.AutoField(primary_key=True, serialize=False)),
                ("warehouse_name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Weapon",
            fields=[
                ("weapon_id", models.AutoField(primary_key=True, serialize=False)),
                ("weapon_type", models.CharField(max_length=255)),
                ("weapon_price", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Admin",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "admin_name",
                    models.CharField(
                        max_length=20, primary_key=True, serialize=False, unique=True
                    ),
                ),
                (
                    "factory",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app00_Reg_Log.factory",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("order_id", models.AutoField(primary_key=True, serialize=False)),
                ("order_date", models.DateTimeField(blank=True, null=True)),
                (
                    "statement",
                    models.CharField(
                        blank=True,
                        choices=[("已处理", "已处理"), ("未处理", "未处理")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app00_Reg_Log.warehouse",
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app00_Reg_Log.weapon",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WarehouseWeapon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "warehouse",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app00_Reg_Log.warehouse",
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app00_Reg_Log.weapon",
                    ),
                ),
            ],
            options={
                "unique_together": {("warehouse", "weapon")},
            },
        ),
        migrations.CreateModel(
            name="FactoryWeapon",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "factory",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app00_Reg_Log.factory",
                    ),
                ),
                (
                    "weapon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app00_Reg_Log.weapon",
                    ),
                ),
            ],
            options={
                "unique_together": {("factory", "weapon")},
            },
        ),
    ]
