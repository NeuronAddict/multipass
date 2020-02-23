# Generated by Django 3.0.3 on 2020-02-21 21:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200221_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='domain',
        ),
        migrations.AddField(
            model_name='offset',
            name='domain',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.Domain'),
            preserve_default=False,
        ),
    ]
