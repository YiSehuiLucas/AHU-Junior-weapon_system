# Generated by Django 5.1.4 on 2024-12-12 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app00_Reg_Log", "0006_weapon_name_weapon_src"),
    ]

    operations = [
        migrations.AlterField(
            model_name="weapon",
            name="src",
            field=models.CharField(max_length=1023),
        ),
    ]