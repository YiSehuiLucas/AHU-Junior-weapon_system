# Generated by Django 5.1.4 on 2024-12-12 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app00_Reg_Log", "0004_alter_users_last_login"),
    ]

    operations = [
        migrations.AlterField(
            model_name="users",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
    ]
